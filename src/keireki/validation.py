from __future__ import annotations

import re
from dataclasses import dataclass

from keireki.dates import PartialDate, parse_partial_date, parse_period_end
from keireki.models import Profile, WorkExperience

SUMMARY_MIN_CHARS = 40
SUMMARY_MAX_CHARS = 450
MAX_SKILL_ITEMS = 30
MAX_TECHNOLOGIES_PER_ROLE = 16
OLDER_ROLE_DETAIL_ITEMS = 24
ASCII_PUNCTUATION_THRESHOLD = 12


@dataclass(frozen=True)
class ValidationResult:
    errors: list[str]
    warnings: list[str]


def validate_profile(profile: Profile) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []

    _validate_required(profile, errors)
    _validate_periods(profile, errors)
    _validate_certifications(profile, errors)
    _validate_warnings(profile, warnings)

    return ValidationResult(errors=errors, warnings=warnings)


def validate_page_count(page_count: int, warnings: list[str]) -> None:
    if page_count > 2:
        warnings.append(f"職務経歴書が2ページを超えています（{page_count}ページ）。")


def sorted_work_experience(profile: Profile) -> list[WorkExperience]:
    return sorted(
        profile.work_experience,
        key=lambda item: parse_partial_date(item.start).sort_date,
        reverse=True,
    )


def _validate_required(profile: Profile, errors: list[str]) -> None:
    if not profile.document.generated_at:
        errors.append("生成日が入力されていません。")
    if not profile.person.name.kanji or not profile.person.name.kana:
        errors.append("氏名またはフリガナが入力されていません。")
    if not profile.person.contact.email and not profile.person.contact.phone:
        errors.append("連絡先が入力されていません。")
    if not profile.education:
        errors.append("学歴が入力されていません。")
    if not profile.work_experience:
        errors.append("職務経歴が入力されていません。")

    for index, work in enumerate(profile.work_experience, start=1):
        prefix = f"職務経歴 {index}"
        if not work.company:
            errors.append(f"{prefix}: 会社名が入力されていません。")
        if not work.role:
            errors.append(f"{prefix}: 役職名が入力されていません。")
        if not work.employment_type:
            errors.append(f"{prefix}: 雇用形態が入力されていません。")
        if not work.responsibilities:
            errors.append(f"{prefix}: 担当業務が入力されていません。")


def _validate_periods(profile: Profile, errors: list[str]) -> None:
    periods: list[tuple[WorkExperience, PartialDate, PartialDate | None]] = []
    for work in profile.work_experience:
        start = parse_partial_date(work.start)
        end = parse_period_end(work.end)
        if end is not None and end.sort_date < start.sort_date:
            errors.append(f"{work.company}: 終了日が開始日より前です。")
        periods.append((work, start, end))

    current_marker = parse_partial_date("9999-12")
    for index, (work, start, end) in enumerate(periods):
        normalized_end = end or current_marker
        for other, other_start, other_end in periods[index + 1 :]:
            normalized_other_end = other_end or current_marker
            overlaps = (
                start.sort_date < normalized_other_end.sort_date
                and other_start.sort_date < normalized_end.sort_date
            )
            if overlaps:
                errors.append(f"{work.company} と {other.company} の在職期間が重複しています。")


def _validate_certifications(profile: Profile, errors: list[str]) -> None:
    for index, certification in enumerate(profile.certifications, start=1):
        if not certification.name or not certification.date:
            errors.append(f"資格 {index}: 資格名または取得日が不正です。")


def _validate_warnings(profile: Profile, warnings: list[str]) -> None:
    summary_length = len(profile.summary)
    if summary_length < SUMMARY_MIN_CHARS:
        warnings.append("職務要約が短すぎる可能性があります。")
    if summary_length > SUMMARY_MAX_CHARS:
        warnings.append("職務要約が長すぎる可能性があります。")

    skill_count = sum(len(group.items) for group in profile.skills)
    if skill_count > MAX_SKILL_ITEMS:
        warnings.append("スキル項目が多すぎる可能性があります。")

    newest_first = sorted_work_experience(profile)
    if newest_first and not newest_first[0].achievements:
        warnings.append("直近の職務経歴に成果が入力されていません。")

    for index, work in enumerate(newest_first):
        if len(work.technologies) > MAX_TECHNOLOGIES_PER_ROLE:
            warnings.append(f"{work.company}: 技術環境の項目が多すぎる可能性があります。")
        detail_count = len(work.responsibilities) + len(work.achievements) + len(work.technologies)
        if index >= 2 and detail_count > OLDER_ROLE_DETAIL_ITEMS:
            warnings.append(f"{work.company}: 古い職務経歴の詳細が多すぎる可能性があります。")

    japanese_text = " ".join(
        [
            profile.summary,
            profile.self_pr,
            *(work.overview for work in profile.work_experience),
            *(item for work in profile.work_experience for item in work.responsibilities),
            *(item for work in profile.work_experience for item in work.achievements),
        ]
    )
    if len(re.findall(r"[!?,.:;()\[\]{}]", japanese_text)) > ASCII_PUNCTUATION_THRESHOLD:
        warnings.append("日本語本文にASCII句読点が多すぎる可能性があります。")
