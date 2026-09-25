# CLAUDE.md

## Context
Personal portfolio project. I (the owner) write the code myself; your job is mainly
**review and teaching**, not writing features. Senior data scientist, strong in Python/ML,
less experience with packaging, GitHub Actions and small-app design.

## Rules
- Do NOT implement features or rewrite functions unless I explicitly ask.
  Point out the problem, explain why, suggest the direction; I write the fix.
- Scope is fixed by the "Definition of Done" in README.md. If you see a good idea
  outside it, propose adding it to ROADMAP.md instead of doing it.
- Don't add dependencies without asking.
- Tests in `tests/` are the spec: don't change them to make code pass.

## Commands
- `uv sync` · `uv run pytest -q` · `uv run ruff check .` · `uv run ruff format .`
- `uv run garda-wind-alert --dry-run`

## Review checklist (when I ask for a review)
Rank findings by severity, one line each, with file:line:
1. Bugs / wrong behaviour (edge cases: wrap-around directions, nulls, empty days, timezones)
2. Failure handling: does a failed run exit non-zero? Are secrets ever logged?
3. Test gaps: what behaviour is untested?
4. Readability / idiomatic Python (dataclasses, typing, pathlib)
5. Nits, only if few
End with: "Is v1 Done?" against the README checklist.
