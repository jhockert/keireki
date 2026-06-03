# AGENTS.md

This file gives coding agents the project conventions needed to make useful,
safe changes in this repository.

## Project Overview

Keireki is a Python 3.12 CLI package that renders Japanese 履歴書 and
職務経歴書 PDFs from structured YAML.

Important paths:

- `src/keireki/`: application code
- `src/keireki/templates/`: Jinja2 document templates
- `src/keireki/static/style.css`: print CSS
- `examples/profile.yaml`: fictional public sample profile
- `examples/assets/`: fictional public sample assets
- `private/`: ignored personal data and photos
- `.agents/skills/`: portable Agent Skills for profile generation/review

## Commands

Use these checks before finishing code changes:

```bash
uv run pytest
uv run ruff check .
uv run mypy src
```

To test document generation:

```bash
uv run keireki generate examples/profile.yaml --output-dir dist --debug-html
```

## Agent Skills

Project-local skills live under `.agents/skills/`:

- `profile-yaml-generator`: use for interviewing a user, extracting resume
  facts from pasted text or documents, and producing Keireki-compatible YAML.
- `profile-reviewer`: use for reviewing Japanese resume content, generated
  PDFs, recruiter/company readiness, and wording or convention risks.

Keep skill references generic for developers, engineers, and technical
professionals. Do not add personal resume details to skill files.

## Privacy Rules

- Do not commit real resume data, addresses, phone numbers, emails, photos, or
  generated personal PDFs.
- Keep personal profiles and photos under `private/`; this directory is ignored
  by Git.
- `examples/` and `tests/fixtures/` must stay fictional.

## Implementation Notes

- Keep the YAML schema in `src/keireki/models.py` and
  `.agents/skills/profile-yaml-generator/references/keireki-schema.md` aligned.
- Validation warnings should be practical and tunable through constants in
  `src/keireki/validation.py`.
- Keep output Japanese-only unless explicitly changing project scope.
- Do not add AI generation, Word output, or Excel output without an explicit
  scope change.
