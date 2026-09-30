#include <gtest/gtest.h>
#include "fast_diff.hpp"
#include <string>
#include <vector>

TEST(FastDiffTest, two_files) {
    std::string a("a");
    std::string b("b");
    DiffResult lines_diff;
    lines_diff.added = {"b"};
    lines_diff.removed = {"a"};
    // ASSERT_EQ(check_webpage_diff_lines({a}, {b}), lines_diff);
}

TEST(FastDiffTest, IdenticalInputsYieldEmptyDiff) {
    std::string html = "<div>\n  <p>Hello World</p>\n</div>";
    auto diff = check_webpage_diff_lines({html}, {html});

    EXPECT_TRUE(diff.added.empty());
    EXPECT_TRUE(diff.removed.empty());
}

TEST(FastDiffTest, HandlesEmptyStrings) {
    auto both_empty = check_webpage_diff_lines({""}, {""});
    EXPECT_TRUE(both_empty.added.empty());
    EXPECT_TRUE(both_empty.removed.empty());

    auto added_only = check_webpage_diff_lines({""}, {"<p>New Content</p>"});
    ASSERT_EQ(added_only.added.size(), 1);
    EXPECT_EQ(added_only.added[0], "<p>New Content</p>");
    EXPECT_TRUE(added_only.removed.empty());

    auto removed_only = check_webpage_diff_lines({"<p>Old Content</p>"}, {""});
    EXPECT_TRUE(removed_only.added.empty());
    ASSERT_EQ(removed_only.removed.size(), 1);
    EXPECT_EQ(removed_only.removed[0], "<p>Old Content</p>");
}
