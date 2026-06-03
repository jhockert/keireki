from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date


class DateParseError(ValueError):
    """Raised when a date value cannot be parsed."""


@dataclass(frozen=True, order=True)
class PartialDate:
    year: int
    month: int
    day: int | None = None

    @property
    def sort_date(self) -> date:
        return date(self.year, self.month, self.day or 1)


DATE_RE = re.compile(r"^(?P<year>\d{4})-(?P<month>\d{2})(?:-(?P<day>\d{2}))?$")


def parse_partial_date(value: str | date | PartialDate) -> PartialDate:
    if isinstance(value, PartialDate):
        return value
    if isinstance(value, date):
        return PartialDate(value.year, value.month, value.day)
    if not isinstance(value, str):
        raise DateParseError("date must be a string")

    match = DATE_RE.match(value)
    if not match:
        raise DateParseError(f"invalid date format: {value}")

    year = int(match.group("year"))
    month = int(match.group("month"))
    day_text = match.group("day")
    day = int(day_text) if day_text else None
    try:
        date(year, month, day or 1)
    except ValueError as exc:
        raise DateParseError(f"invalid date value: {value}") from exc
    return PartialDate(year, month, day)


def parse_period_end(value: str | date | PartialDate) -> PartialDate | None:
    if isinstance(value, str) and value.lower() == "present":
        return None
    return parse_partial_date(value)


def format_japanese_era(value: str | date | PartialDate) -> str:
    parsed = parse_partial_date(value)
    era_name, era_year = _era_for(parsed.sort_date)
    year_text = "元" if era_year == 1 else str(era_year)
    if parsed.day is None:
        return f"{era_name}{year_text}年{parsed.month}月"
    return f"{era_name}{year_text}年{parsed.month}月{parsed.day}日"


def format_period(start: str | date | PartialDate, end: str | date | PartialDate) -> str:
    start_text = format_japanese_era(start)
    if isinstance(end, str) and end.lower() == "present":
        end_text = "現在"
    else:
        end_text = format_japanese_era(end)
    return f"{start_text} ～ {end_text}"


def western_year(value: str | date | PartialDate) -> str:
    return str(parse_partial_date(value).year)


def western_month(value: str | date | PartialDate) -> str:
    return str(parse_partial_date(value).month)


def _era_for(value: date) -> tuple[str, int]:
    eras = (
        ("令和", date(2019, 5, 1)),
        ("平成", date(1989, 1, 8)),
        ("昭和", date(1926, 12, 25)),
    )
    for name, starts_at in eras:
        if value >= starts_at:
            return name, value.year - starts_at.year + 1
    raise DateParseError("dates before 昭和 are not supported")
