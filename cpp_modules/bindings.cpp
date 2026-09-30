#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "fast_diff.hpp"

namespace py = pybind11;

PYBIND11_MODULE(fast_diff_extension, m, py::mod_gil_not_used()) {
    m.doc() = "Fast Diff implemented in C++";

    m.def(
        "check_webpage_diff_lines",
        &check_webpage_diff_lines,
        "Computes added and removed signatures between two snapshots",
        py::arg("old_page_signatures"),
        py::arg("new_page_signatures")
    );
    py::class_<DiffResult>(m, "DiffResult")
        .def_readonly("added", &DiffResult::added)
        .def_readonly("removed", &DiffResult::removed);
}
