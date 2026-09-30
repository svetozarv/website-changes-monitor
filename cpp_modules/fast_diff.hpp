#pragma once
#include <string>
#include <vector>

struct DiffResult {
    std::vector<std::string> added;
    std::vector<std::string> removed;
};

DiffResult check_webpage_diff_lines(const std::vector<std::string>& old_page_signatures, const std::vector<std::string>& new_page_signatures);
