# 2025-2 GEWR002-15 General Writing

This is a repository for archiving the test code used in 2025-2 GEWR002-15 General Writing Team 3's report assignment.

## Report Assignment Team 3 - Coding Task Test Code Repository

`run_tests.py` grades the solve code per criteria specified in `INST.md`, powered by the pytest package. Usage is as follows:
- `python run_tests.py <path-to-solve-code-file>`
- run_tests.py imports the solve code by path dynamically as if importing a module. Thus, the argument should be provided without the extension.
- `example_solve` is only for reference; it is made to be ignored by common AI agents, as you can see from `.aiexclude` and `.cursorignore`. If your agent/service/extension uses different path, mimic this behavior.
- `.aiexclude`, `.cursorignore`, and `.gitignore` include (and thus ignore) `localtest` directory and `localtest.*.txt` which would be the graded score result files' name for modules inside `localtest`. You can create the directory and perform local tests inside of it without being tracked by git or read by AI agents.

Mock assignment and grading criteria are provided in `INST.md`.
