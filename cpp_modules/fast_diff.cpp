#include "fast_diff.hpp"
#include <unordered_set>

// Returns difference between two vectors of signatures (flattened DOM Tree, ex. 'div.card > span.price: 500 zł' )
DiffResult check_webpage_diff_lines(const std::vector<std::string>& old_page_signatures, const std::vector<std::string>& new_page_signatures) {
    DiffResult lines_diff;
    std::unordered_set<std::string> old_page_signatures_set(old_page_signatures.begin(), old_page_signatures.end());;
    std::unordered_set<std::string> new_page_signatures_set(new_page_signatures.begin(), new_page_signatures.end());;

    for (const auto& sig : new_page_signatures) {
        if (sig == "") continue;
        if (!old_page_signatures_set.contains(sig)) {
            lines_diff.added.push_back(sig);
        }
    }

    for (const auto& sig : old_page_signatures) {
        if (sig == "") continue;
        if (!new_page_signatures_set.contains(sig)) {
            lines_diff.removed.push_back(sig);
        }
    }

    return lines_diff;
}
