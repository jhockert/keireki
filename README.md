# Keireki

[![CI](https://github.com/jhockert/keireki/actions/workflows/ci.yml/badge.svg)](https://github.com/jhockert/keireki/actions/workflows/ci.yml)

Generate Japanese 履歴書 and 職務経歴書 PDFs from structured YAML.

Keireki is a small Python CLI for keeping resume data in YAML and rendering
Japanese PDF documents with repeatable templates.

> Status: early project. The public sample data is fictional.

## Requirements

- Python 3.12 or newer
- [uv](https://docs.astral.sh/uv/)
- WeasyPrint system dependencies
- Japanese fonts such as Noto Sans CJK JP

The Docker workflow below installs the PDF/font dependencies for you.

## Usage

```bash
uv sync
uv run keireki generate examples/profile.yaml
```

Outputs:

```text
dist/
├── rirekisho.pdf
└── shokumukeirekisho.pdf
```

Optional flags:

```bash
uv run keireki generate examples/profile.yaml --output-dir dist
uv run keireki generate examples/profile.yaml --debug-html
```

Use `--debug-html` when tuning templates or typography.

## Profile Data

The sample profile in `examples/profile.yaml` is fictional. Start from it and create
your own private profile file:

```bash
mkdir -p private/assets
cp examples/profile.yaml private/profile.yaml
uv run keireki generate private/profile.yaml
```

The `private/` directory is ignored by Git by default, so personal resumes, addresses,
phone numbers, and photos do not accidentally get committed.

If you want `private/` to track changes you can make it a separate private Git repository:

```bash
cd private
git init
git remote add origin git@github.com:your-user/keireki-private.git
git add .
git commit -m "Back up private profile data"
git push -u origin main
```

See [docs/profile-yaml.md](docs/profile-yaml.md) for the complete profile YAML
schema and all supported settings.

Photos are optional. If `person.photo_path` is set, the image is rendered in the
履歴書 photo area. If it is blank, the template shows the traditional photo
placeholder text.

Use `preferences.request_notes` for the 履歴書 本人希望記入欄 text.

## Development

```bash
uv sync
uv run pytest
uv run ruff check .
uv run mypy src
```

To verify PDF generation locally:

```bash
uv run keireki generate examples/profile.yaml --output-dir dist --debug-html
```

## Docker

```bash
docker build -t keireki .
docker run --rm -v "$PWD:/app" keireki generate examples/profile.yaml
```

The Docker image installs Noto CJK fonts and WeasyPrint system dependencies for
reproducible PDF generation.

## Project Scope

Keireki is intentionally Japanese-only and PDF-only. It does not generate, tailor,
or rewrite resume content. The YAML remains the source of truth.

## Agent Skills

This repository includes portable Agent Skills under `.agents/skills/`, following
the `SKILL.md` directory format:

- `.agents/skills/profile-yaml-generator`: interview a user and turn resume
  materials into Keireki-compatible `profile.yaml`.
- `.agents/skills/profile-reviewer`: review generated Japanese resume materials as
  a recruiter or hiring manager for technical candidates.

## AI Assistance

This project was generated with AI assistance and reviewed by the maintainer. The
code, templates, and examples should be treated like any other open-source code:
review changes, run tests, and verify generated documents before use.

## License

MIT License. See `LICENSE`.

## Repository Hygiene

Before publishing or pushing changes, run:

```bash
uv run pytest
uv run ruff check .
uv run mypy src
```

Do not commit generated PDFs from `dist/` or personal files from `private/`.
