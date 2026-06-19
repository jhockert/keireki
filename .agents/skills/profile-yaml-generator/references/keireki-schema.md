# Keireki YAML Reference

Use this reference when creating `profile.yaml` for the Keireki project.
The canonical public schema reference is `docs/profile-yaml.md`; keep this file
aligned with it when fields change.

## Top-Level Shape

```yaml
document:
  generated_at: "2026-06-03"
  language: ja

person:
  name:
    kanji: ""
    kana: ""
  birth_date: "YYYY-MM-DD"
  gender: ""
  photo_path: ""
  address:
    postal_code: ""
    prefecture: ""
    city: ""
    street: ""
  contact:
    email: ""
    phone: ""
    linkedin: ""
    github: ""
    website: ""

preferences:
  headline: ""
  tagline: ""
  desired_roles: []
  desired_areas: []
  relocation: ""
  visa_support: ""
  work_style: ""
  management_preference: ""
  japanese_communication: ""
  request_notes: ""

summary: >
  ...

technical_highlights: []

skills:
  - category: ""
    items: []

work_experience:
  - company: ""
    role: ""
    employment_type: ""
    start: "YYYY-MM"
    end: present
    overview: >
      ...
    responsibilities: []
    achievements: []
    technologies: []

education:
  - school: ""
    start: "YYYY-MM"
    end: "YYYY-MM"
    description: ""

certifications:
  - name: ""
    date: "YYYY-MM"

languages:
  - name: ""
    level: ""

self_pr: >
  ...
```

## Required or Important Fields

- `document.generated_at`: required date.
- `person.name.kanji`, `person.name.kana`: required. For foreign names, katakana is acceptable in both if no kanji name exists.
- `person.birth_date`: required.
- At least one contact method: email or phone.
- `work_experience`: at least one entry.
- `education`: at least one entry.
- Each work entry needs company, role, employment type, start/end, and responsibilities.

## Dates

- Use quoted strings.
- Full dates: `"YYYY-MM-DD"`.
- Month dates: `"YYYY-MM"`.
- Current job end: `present`.
- Avoid YAML bare dates because parsers may convert them to native date objects.

## Content Style

- Keep `summary` around 2-4 concise Japanese sentences.
- Use `technical_highlights` for 3-6 high-signal achievements, scale, or architecture scope that should be visible before detailed career history.
- Use `preferences.headline` and `preferences.tagline` for concise 職務経歴書 header `職種` / `専門領域` lines when helpful for technical screening.
- Use `preferences.request_notes` for 履歴書の本人希望記入欄. Keep it conservative and factual, such as desired role family, location/start-date discussion, or visa/logistics notes when relevant.
- Recent roles should be more detailed than older roles.
- Use achievements for the newest/relevant roles.
- Keep technologies, tools, methods, standards, and programming languages in their normal industry form.
- Use Japanese labels for generic categories when natural: `開発`, `設計`, `テスト`, `品質管理`, `インフラ`, `自動化`, `監視`, `文書化`, `技術リード`, `プロジェクト管理`.

## Common Japanese Phrasing

- Visa support, when applicable: `ビザサポート希望。実務経験および保有資格に基づき、在留資格要件を満たす見込みです。`
- Internal Japanese communication: `日本語での社内コミュニケーションに対応可能です。`
- English business communication: `英語での会議・文書作成・技術調整に対応可能です。`
- Hands-on technical preference: `設計・改善・実装を担うハンズオンの技術職を希望します。`
- Management preference: `ピープルマネジメントよりも、専門性を活かした技術貢献を希望します。`
- Rirekisho request notes: `職種・勤務地・勤務条件につきましては、相談の上で決定させていただければ幸いです。`
