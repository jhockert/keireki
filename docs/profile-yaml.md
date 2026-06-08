# Profile YAML Reference

Keireki renders Japanese 履歴書 and 職務経歴書 PDFs from a structured YAML
profile file. The file is usually named `profile.yaml`, but any YAML file passed
to `keireki generate` uses the same schema.

The YAML parser is strict: unknown fields are rejected. Keep dates quoted so YAML
does not convert them into native date objects.

## Complete Shape

```yaml
document:
  generated_at: "YYYY-MM-DD"
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

skills:
  - category: ""
    items: []

work_experience:
  - company: ""
    role: ""
    start: "YYYY-MM"
    end: present
    employment_type: ""
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

## Required Fields

- `document.generated_at`
- `person.name.kanji`
- `person.name.kana`
- `person.birth_date`
- At least one of `person.contact.email` or `person.contact.phone`
- `summary`
- At least one `work_experience` entry
- At least one `education` entry
- For each `work_experience` entry: `company`, `role`, `start`, `end`,
  `employment_type`, and at least one `responsibilities` item

Most other fields may be blank strings or empty lists.

## Dates

Use quoted strings.

- Full date: `"YYYY-MM-DD"`
- Month date: `"YYYY-MM"`
- Current job end: `present`

履歴書 history rows render year and month. 職務経歴書 career-table periods render
Japanese era year and month only, even when exact full dates are stored in YAML.
This lets the source data stay precise while keeping the PDF conventional.

Same-month or same-day job handoffs are allowed. For example, one job may end in
`"2023-09-01"` and the next may start in `"2023-09-01"`.

## Field Reference

### `document`

- `generated_at`: Date shown in document headers.
- `language`: Document language. The current project scope is Japanese; use `ja`.

### `person`

- `name.kanji`: Display name. For foreign names, katakana is acceptable.
- `name.kana`: Furigana/katakana name.
- `birth_date`: Birth date.
- `gender`: Optional gender text for 履歴書.
- `photo_path`: Optional path to a photo. Relative paths are resolved from the
  current working directory. Keep personal photos under `private/assets/`.
- `address.postal_code`: Postal code.
- `address.prefecture`: Prefecture, state, region, or country-level address part.
- `address.city`: City/municipality.
- `address.street`: Street and building.
- `contact.email`: Email address.
- `contact.phone`: Phone number.
- `contact.linkedin`: Stored for profile completeness; not currently rendered.
- `contact.github`: Stored for profile completeness; not currently rendered.
- `contact.website`: Stored for profile completeness; not currently rendered.

### `preferences`

These fields render in 職務経歴書 under `希望職種・条件`, except
`request_notes`, which renders in the 履歴書 本人希望記入欄.

- `desired_roles`: Target role names.
- `desired_areas`: Target technical or business domains.
- `relocation`: Relocation or work-location preference.
- `visa_support`: Visa/status-of-residence notes when relevant.
- `work_style`: Desired seniority or work style.
- `management_preference`: Management versus hands-on preference. Stored for
  profile completeness; not currently rendered directly.
- `japanese_communication`: Practical language/communication note.
- `request_notes`: 履歴書 本人希望記入欄 text. Keep this conservative and factual,
  such as desired role family, location/start-date discussion, or visa/logistics
  notes when relevant.

### `summary`

Short professional summary for the top of the 職務経歴書. Keep it concise,
usually 2-4 Japanese sentences.

### `skills`

Skill groups rendered in 職務経歴書 under `生かせる能力・スキル`.

- `category`: Skill category label.
- `items`: Skills, tools, technologies, methods, or strengths in that category.

### `work_experience`

Work history rendered in both documents.

- `company`: Employer or client/context name. For consulting/client work, a form
  like `Client（Employer経由）` keeps 職務経歴書 clear while 履歴書 can render the
  legal employer.
- `role`: Role/title.
- `start`: Start date.
- `end`: End date or `present`.
- `employment_type`: Employment type, such as `正社員` or `コンサルタント`.
- `overview`: Short role overview.
- `responsibilities`: Responsibilities and scope. The newest roles render the
  first three items in 職務経歴書.
- `achievements`: Results or impact. The newest roles render the first two items.
- `technologies`: Tools and technologies. 職務経歴書 renders the first eight items.

Recent and relevant roles should carry more detail. Older roles can be compact.

### `education`

Education history for 履歴書.

- `school`: School name.
- `start`: Start date.
- `end`: End date.
- `description`: Program, major, completion note, or short description.

### `certifications`

Certifications and courses rendered in both documents.

- `name`: Certification/course name.
- `date`: Acquisition, completion, or attendance date.

For courses without an exam, use wording such as `受講` or `受講修了`.

### `languages`

Languages render in 職務経歴書 under `生かせる能力・スキル`.

- `name`: Language name.
- `level`: Practical level or evidence, such as `日本語能力試験 2級`.

### `self_pr`

Self-PR text rendered in both documents. For 履歴書, keep it compact. The
職務経歴書 may carry slightly richer professional positioning, but it should still
be factual and modest.

## Japanese Wording Examples

```yaml
relocation: 日本への転職・移住を積極的に希望
visa_support: >
  日本人配偶者がおり、在留資格「日本人の配偶者等」に係る申請書類を準備済みです。
  入社時期等は選考時に相談可能です。
work_style: >
  Senior Engineer / Tech Leadとして、設計・改善・実装を担うハンズオンの技術リードを希望します。
japanese_communication: >
  日本語での社内コミュニケーションに対応可能です。英語では会議・文書作成・技術調整に対応可能です。
request_notes: >
  職種・勤務地・勤務条件につきましては、相談の上で決定させていただければ幸いです。
```

## Privacy

Do not put real personal data in `examples/` or `tests/fixtures/`. Keep real
profiles, photos, and generated personal PDFs under `private/`.
