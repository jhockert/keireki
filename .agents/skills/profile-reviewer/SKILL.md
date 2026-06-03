---
name: profile-reviewer
description: Review Keireki profile.yaml files, generated Japanese 履歴書/職務経歴書 PDFs, or pasted resume content as a Japanese recruiter or hiring manager evaluating developers, engineers, and technical professionals. Use when the user wants candid feedback on resume quality, Japanese hiring conventions, role fit, recruiter/company readiness, missing information, wording risk, relocation/visa positioning when relevant, or final send-readiness.
---

# Profile Reviewer

## Goal

Review Japanese resume materials from the viewpoint of a Japanese recruiter or hiring manager evaluating developers, engineers, and technical professionals. Give practical, prioritized feedback that improves the user's chance of passing screening without exaggerating facts.

## Review Workflow

1. **Inspect artifacts before judging**
   - Read provided YAML, pasted text, PDFs, generated HTML, or templates.
   - For PDFs, render pages visually when layout matters and extract text with `pdftotext -layout` when possible.
   - If inside a Keireki repo, inspect templates and generated files in `dist/` when relevant.

2. **Identify the audience**
   - Distinguish recruiter submission, direct company application, staffing agency, Japanese company, foreign-capital company, or technical hiring manager.
   - If the audience is unknown, review for a general Japanese tech job-search package.

3. **Review in layers**
   - Content fit: target roles, seniority, tools/technologies/methods, language ability, and relocation/visa positioning when relevant.
   - Japanese convention: 履歴書 factual style, 職務経歴書 structure, 学歴/職歴 separation, qualification wording.
   - Evidence strength: achievements, scale, responsibilities, impact, recency.
   - Risk: overstated language ability, unclear visa needs, too much/too little detail, awkward Japanese, missing contact facts.
   - Layout: page count, clipping, readability, scanability, photo/address/contact presentation.

4. **Be candid but actionable**
   - Lead with the verdict: send as-is, send with minor edits, or revise before sending.
   - Prioritize the top 3-5 changes that materially affect screening.
   - Do not nitpick harmless style differences unless the user asks for polish.
   - Do not invent experience or suggest dishonest phrasing.

5. **Ask follow-up questions only when needed**
   - Ask when a missing fact materially changes the advice: visa status, relocation target, Japanese interview ability, target role, salary range, or unexplained job gaps.
   - Otherwise provide recommendations with assumptions.

## Review Standards

- A general-purpose Japanese technical-role submission should usually include both 履歴書 and 職務経歴書.
- 履歴書 should stay standardized, factual, and conservative.
- 職務経歴書 should be readable in 2-3 pages for experienced technical professionals; 2 pages is preferable for recruiter screening.
- Recent and most relevant roles should carry most detail. Older or less relevant roles can be compact.
- Use Japanese for generic labels, but keep normal tech/product names in English.
- State language ability honestly. Prefer scoped claims such as `社内コミュニケーションに対応可能` over broad customer-facing claims if that is more accurate.
- For course attendance without an exam, prefer `受講` or `受講修了`.

## Output Shape

Use this concise structure unless the user asks for deeper review:

1. **Verdict**: one clear paragraph.
2. **High-impact changes**: ordered list.
3. **Optional polish**: low-risk improvements.
4. **Questions**: only if needed.

## Resources

- Read [Japanese Tech Resume Review Guide](references/japanese-tech-resume-review.md) when deeper standards or phrasing guidance is needed.
