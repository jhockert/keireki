---
name: profile-yaml-generator
description: Create Keireki-compatible profile.yaml files for developers, engineers, and technical professionals by interviewing users and extracting information from pasted text, existing resumes, PDFs, DOCX files, or partial YAML. Use when the user wants help generating, completing, translating, validating, or refining structured YAML input for Japanese 履歴書 and 職務経歴書 generation, especially when missing details or ambiguous resume history require follow-up questions.
---

# Profile YAML Generator

## Goal

Produce a truthful, well-structured Keireki `profile.yaml` from user interviews and source artifacts such as PDFs, pasted resumes, DOCX templates, existing YAML, or notes. Prefer explicit facts from sources, ask for high-impact missing information, and avoid inventing personal details.

## Core Workflow

1. **Ground in artifacts first**
   - Inspect any provided files, pasted text, existing YAML, or repository schema before asking questions.
   - For PDFs, extract text with `pdftotext -layout` when available; render pages for visual checks if layout matters.
   - For DOCX, inspect document text by reading `word/document.xml` from the zip if normal conversion tools are unavailable.
   - If working inside a Keireki repo, inspect `src/keireki/models.py`, templates, and `examples/profile.yaml` for the active schema.

2. **Build a fact inventory**
   - Separate confirmed facts, inferred-but-likely facts, and missing facts.
   - Preserve original dates and job titles when uncertain; note conflicts for the interview.
   - Treat names, addresses, phone numbers, birth dates, certificates, and visa status as sensitive facts. Never guess them.

3. **Interview only for meaningful gaps**
   - Ask concise questions after artifact review.
   - Group questions by purpose: identity/contact, desired roles, work history, education/certificates, languages, self PR.
   - Prefer concrete choices when possible, but allow free-form answers for personal history.
   - Do not ask for facts already present in the artifacts unless there is a conflict.

4. **Draft Japanese content**
   - Keep Japanese business style: clear, factual, modest, and specific.
   - Translate generic role/content labels into Japanese while preserving normal tech/product names.
   - Keep established product/tool/language names in their normal form, such as Linux, AWS, Azure, Kubernetes, Python, Java, C++, JavaScript, React, PostgreSQL, MATLAB, SolidWorks, AutoCAD, PLC, or Jira.
   - Avoid overstating language ability. Use phrases like `社内コミュニケーションに対応可能` when the user is comfortable internally but not fully customer-facing.

5. **Generate YAML**
   - Use quoted strings for all dates: `"YYYY-MM-DD"` or `"YYYY-MM"`.
   - Use `present` only for current work-experience end dates.
   - Keep source data richer than rendered output when useful, but avoid stuffing irrelevant detail.
   - If a photo is available, put it in a project-owned private or examples asset path and set `person.photo_path`.

6. **Validate and iterate**
   - Run the project generator when available, e.g. `uv run keireki generate <profile.yaml> --output-dir <tmpdir> --debug-html`.
   - Resolve validation errors. Treat warnings as advice; distinguish raw YAML detail warnings from rendered-output problems.
   - Inspect generated PDFs when layout or Japanese submission readiness matters.

## Interview Priorities

Ask for these if missing or conflicting:

- Legal/display name in kanji/kana or katakana, birth date, gender if used, email, phone, address, photo path.
- Desired role family, target industry/domain, relocation intent, visa/support needs, work style, and management preference.
- For each job: company, role, employment type, start/end, overview, responsibilities, achievements, tools/technologies/methods.
- Education: school, start/end, description or major.
- Certifications: exact name, date, whether it was passed, obtained, attended, or completed.
- Languages: practical ability and evidence. Prefer honest labels over inflated fluency.
- Self PR themes: strengths, working style, collaboration, motivation, and target market.

## Japanese Resume Conventions

- 履歴書 should be simple and factual. Do not add GitHub/LinkedIn unless the user explicitly wants it and the template supports it.
- 職務経歴書 can include 希望職種・条件 when useful for recruiters, direct applications, relocation, or visa context.
- Separate `学歴` and `職歴` in traditional 履歴書 history rows.
- For courses without exams, use `受講` or `受講修了`; avoid `合格`, `認定`, or `資格` unless true.
- For Japanese language tests, prefer `日本語能力試験 2級` over `JLPT N2` in Japanese documents.

## Resources

- Read the project canonical `docs/profile-yaml.md` when available, or [Keireki YAML Reference](references/keireki-schema.md) when using the skill outside the Keireki repo.
