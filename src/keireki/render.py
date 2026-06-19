from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from jinja2 import Environment, PackageLoader, select_autoescape
from pydantic import ValidationError
from weasyprint import HTML

from keireki.dates import (
    format_japanese_era,
    format_japanese_era_month,
    format_period,
    parse_partial_date,
    parse_period_end,
    western_month,
    western_year,
)
from keireki.models import Education, Profile, WorkExperience
from keireki.validation import sorted_work_experience, validate_page_count, validate_profile


class ProfileLoadError(ValueError):
    """Raised when YAML cannot be loaded or parsed as a profile."""


@dataclass(frozen=True)
class GeneratedFiles:
    rirekisho_pdf: Path
    shokumukeirekisho_pdf: Path
    warnings: list[str]


@dataclass
class WorkExperienceGroup:
    company: str
    start: str
    end: str
    items: list[WorkExperience]


def load_profile(path: Path) -> Profile:
    try:
        with path.open("r", encoding="utf-8") as file:
            data: Any = yaml.safe_load(file)
    except OSError as exc:
        raise ProfileLoadError(f"{path}: YAMLを読み込めません。") from exc
    except yaml.YAMLError as exc:
        raise ProfileLoadError(f"{path}: YAMLの形式が不正です。") from exc

    if not isinstance(data, dict):
        raise ProfileLoadError(f"{path}: YAMLのトップレベルはマッピングにしてください。")

    try:
        return Profile.from_yaml_data(data)
    except ValidationError as exc:
        messages = "; ".join(error["msg"] for error in exc.errors())
        raise ProfileLoadError(messages) from exc


def render_documents(
    profile: Profile,
    output_dir: Path,
    debug_html: bool = False,
) -> GeneratedFiles:
    validation = validate_profile(profile)
    if validation.errors:
        raise ProfileLoadError("\n".join(validation.errors))

    output_dir.mkdir(parents=True, exist_ok=True)
    env = _environment()
    context = _context(profile)

    rirekisho_html = env.get_template("rirekisho.html.j2").render(context)
    shokumukeirekisho_html = env.get_template("shokumukeirekisho.html.j2").render(context)

    if debug_html:
        (output_dir / "rirekisho.html").write_text(rirekisho_html, encoding="utf-8")
        (output_dir / "shokumukeirekisho.html").write_text(shokumukeirekisho_html, encoding="utf-8")

    rirekisho_pdf = output_dir / "rirekisho.pdf"
    shokumukeirekisho_pdf = output_dir / "shokumukeirekisho.pdf"

    base_url = str(Path(__file__).parent)
    HTML(string=rirekisho_html, base_url=base_url).write_pdf(rirekisho_pdf)

    shokumukeirekisho_document = HTML(string=shokumukeirekisho_html, base_url=base_url).render()
    warnings = [*validation.warnings]
    validate_page_count(len(shokumukeirekisho_document.pages), warnings)
    shokumukeirekisho_document.write_pdf(shokumukeirekisho_pdf)

    return GeneratedFiles(
        rirekisho_pdf=rirekisho_pdf,
        shokumukeirekisho_pdf=shokumukeirekisho_pdf,
        warnings=warnings,
    )


def _environment() -> Environment:
    env = Environment(
        loader=PackageLoader("keireki", "templates"),
        autoescape=select_autoescape(("html", "xml", "j2")),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters["era"] = format_japanese_era
    env.filters["era_month"] = format_japanese_era_month
    env.filters["period"] = format_period
    env.filters["western_month"] = western_month
    env.filters["western_year"] = western_year
    return env


def _context(profile: Profile) -> dict[str, object]:
    work_experience = sorted_work_experience(profile)
    return {
        "profile": profile,
        "photo_uri": _photo_uri(profile),
        "rirekisho_history": _rirekisho_history(profile),
        "work_experience": work_experience,
        "grouped_work_experience": _group_work_experience(work_experience),
        "recent_work_experience": work_experience[:2],
        "older_work_experience": work_experience[2:],
        "style_path": "static/style.css",
    }


def _photo_uri(profile: Profile) -> str:
    if not profile.person.photo_path:
        return ""

    path = Path(profile.person.photo_path).expanduser()
    if not path.is_absolute():
        path = Path.cwd() / path
    if not path.exists():
        return ""
    return path.as_uri()


def _group_work_experience(work_experience: list[WorkExperience]) -> list[WorkExperienceGroup]:
    groups: list[WorkExperienceGroup] = []
    for work in work_experience:
        company = _shokumukeirekisho_company(work.company)
        group = next((item for item in groups if item.company == company), None)
        if group is None:
            groups.append(
                WorkExperienceGroup(
                    company=company,
                    start=work.start,
                    end=work.end,
                    items=[work],
                )
            )
            continue

        group.items.append(work)
        if parse_partial_date(work.start).sort_date < parse_partial_date(group.start).sort_date:
            group.start = work.start
        if _is_later_end(work.end, group.end):
            group.end = work.end

    return groups


def _is_later_end(candidate: str, current: str) -> bool:
    candidate_end = parse_period_end(candidate)
    current_end = parse_period_end(current)
    if candidate_end is None:
        return True
    if current_end is None:
        return False
    return candidate_end.sort_date > current_end.sort_date


def _rirekisho_history(profile: Profile) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    rows.append({"year": "", "month": "", "text": "学歴"})
    for education in sorted(profile.education, key=lambda item: item.start):
        rows.append(
            {
                "year": western_year(education.start),
                "month": western_month(education.start),
                "text": f"{education.school} 入学",
            }
        )
        rows.append(
            {
                "year": western_year(education.end),
                "month": western_month(education.end),
                "text": _rirekisho_education_completion(education),
            }
        )

    rows.append({"year": "", "month": "", "text": "職歴"})
    for work in sorted(profile.work_experience, key=lambda item: item.start):
        company = _rirekisho_company(work.company)
        rows.append(
            {
                "year": western_year(work.start),
                "month": western_month(work.start),
                "text": f"{company} 入社",
            }
        )
        if work.end.lower() != "present":
            rows.append(
                {
                    "year": western_year(work.end),
                    "month": western_month(work.end),
                    "text": f"{company} 退職",
                }
            )

    rows.append({"year": "", "month": "", "text": "現在に至る"})
    return rows


def _rirekisho_company(company: str) -> str:
    if "経由" in company and "（" in company:
        via = company.split("（", maxsplit=1)[1].split("経由", maxsplit=1)[0]
        return via.rstrip("）・")
    return company.split("（", maxsplit=1)[0]


def _shokumukeirekisho_company(company: str) -> str:
    return company.split("（", maxsplit=1)[0]


def _rirekisho_education_completion(education: Education) -> str:
    description = education.description
    if "高等学校卒業" in description:
        major = description.replace("・高等学校卒業", "").strip()
        if major:
            return f"{education.school} 卒業（{major}）"
        return f"{education.school} 卒業"
    if description:
        return f"{education.school} 修了 {description}"
    return f"{education.school} 修了"
