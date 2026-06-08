import pytest

from keireki.dates import (
    DateParseError,
    format_japanese_era,
    format_japanese_era_month,
    format_period,
    parse_partial_date,
)


def test_format_japanese_era_boundaries() -> None:
    assert format_japanese_era("1926-12-25") == "昭和元年12月25日"
    assert format_japanese_era("1989-01-08") == "平成元年1月8日"
    assert format_japanese_era("2019-05-01") == "令和元年5月1日"


def test_format_month_and_full_date() -> None:
    assert format_japanese_era("2026-01") == "令和8年1月"
    assert format_japanese_era("2026-01-02") == "令和8年1月2日"


def test_format_era_month_omits_day() -> None:
    assert format_japanese_era_month("2026-01") == "令和8年1月"
    assert format_japanese_era_month("2026-01-24") == "令和8年1月"


def test_format_period_present() -> None:
    assert format_period("2026-01", "present") == "令和8年1月 ～ 現在"


def test_invalid_date() -> None:
    with pytest.raises(DateParseError):
        parse_partial_date("2026/01")
