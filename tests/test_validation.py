from pathlib import Path

import pytest
from pydantic import ValidationError

from keireki.models import Profile
from keireki.render import load_profile
from keireki.validation import validate_page_count, validate_profile

FIXTURES = Path(__file__).parent / "fixtures"


def test_load_valid_profile() -> None:
    profile = load_profile(FIXTURES / "valid_profile.yaml")
    result = validate_profile(profile)
    assert result.errors == []
    assert profile.person.photo_path == "examples/assets/profile.svg"
    assert profile.person.contact.github == "github.com/example"
    assert profile.preferences.desired_roles == ["ソフトウェアエンジニア", "技術リード"]
    assert profile.languages[1].level == "ビジネスレベル"


def test_missing_contact_is_error() -> None:
    profile = load_profile(FIXTURES / "valid_profile.yaml")
    data = profile.model_dump()
    data["person"]["contact"]["email"] = ""
    data["person"]["contact"]["phone"] = ""
    result = validate_profile(Profile.model_validate(data))
    assert "連絡先" in result.errors[0]


def test_missing_required_sections_are_errors() -> None:
    profile = load_profile(FIXTURES / "valid_profile.yaml")
    data = profile.model_dump()
    data["education"] = []
    data["work_experience"] = []
    result = validate_profile(Profile.model_validate(data))
    assert "学歴が入力されていません。" in result.errors
    assert "職務経歴が入力されていません。" in result.errors


def test_invalid_date_rejected_by_model() -> None:
    profile = load_profile(FIXTURES / "valid_profile.yaml")
    data = profile.model_dump()
    data["work_experience"][0]["start"] = "2026/01"
    with pytest.raises(ValidationError):
        Profile.model_validate(data)


def test_end_before_start_is_error() -> None:
    profile = load_profile(FIXTURES / "valid_profile.yaml")
    data = profile.model_dump()
    data["work_experience"][0]["start"] = "2024-01"
    data["work_experience"][0]["end"] = "2023-12"
    result = validate_profile(Profile.model_validate(data))
    assert any("終了日が開始日より前" in error for error in result.errors)


def test_overlapping_jobs_are_errors() -> None:
    profile = load_profile(FIXTURES / "valid_profile.yaml")
    data = profile.model_dump()
    data["work_experience"].append(
        {
            "company": "Other Corp",
            "role": "Engineer",
            "start": "2023-01",
            "end": "2024-01",
            "employment_type": "正社員",
            "overview": "",
            "responsibilities": ["運用"],
            "achievements": [],
            "technologies": [],
        }
    )
    result = validate_profile(Profile.model_validate(data))
    assert any("重複" in error for error in result.errors)


def test_incomplete_work_entry_is_error() -> None:
    profile = load_profile(FIXTURES / "valid_profile.yaml")
    data = profile.model_dump()
    data["work_experience"][0]["company"] = ""
    data["work_experience"][0]["role"] = ""
    data["work_experience"][0]["employment_type"] = ""
    data["work_experience"][0]["responsibilities"] = []
    result = validate_profile(Profile.model_validate(data))
    assert "職務経歴 1: 会社名が入力されていません。" in result.errors
    assert "職務経歴 1: 役職名が入力されていません。" in result.errors
    assert "職務経歴 1: 雇用形態が入力されていません。" in result.errors
    assert "職務経歴 1: 担当業務が入力されていません。" in result.errors


def test_warning_thresholds() -> None:
    profile = load_profile(FIXTURES / "valid_profile.yaml")
    data = profile.model_dump()
    data["summary"] = "短い"
    data["work_experience"][0]["achievements"] = []
    data["work_experience"][0]["technologies"] = [f"tech{i}" for i in range(17)]
    result = validate_profile(Profile.model_validate(data))
    assert any("短すぎる" in warning for warning in result.warnings)
    assert any("成果" in warning for warning in result.warnings)
    assert any("技術環境" in warning for warning in result.warnings)


def test_page_count_warning() -> None:
    warnings: list[str] = []
    validate_page_count(3, warnings)
    assert warnings == ["職務経歴書が2ページを超えています（3ページ）。"]
