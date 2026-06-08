from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from keireki.dates import DateParseError, parse_partial_date, parse_period_end


class KeirekiModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class Document(KeirekiModel):
    generated_at: str
    language: str = "ja"


class Name(KeirekiModel):
    kanji: str
    kana: str


class Address(KeirekiModel):
    postal_code: str = ""
    prefecture: str = ""
    city: str = ""
    street: str = ""

    @property
    def full(self) -> str:
        return "".join(part for part in (self.prefecture, self.city, self.street) if part)


class Contact(KeirekiModel):
    email: str = ""
    phone: str = ""
    linkedin: str = ""
    github: str = ""
    website: str = ""


class Person(KeirekiModel):
    name: Name
    birth_date: str
    gender: str = ""
    address: Address = Field(default_factory=Address)
    contact: Contact
    photo_path: str = ""


class SkillGroup(KeirekiModel):
    category: str
    items: list[str]


class WorkExperience(KeirekiModel):
    company: str
    role: str
    start: str
    end: str
    employment_type: str
    overview: str = ""
    responsibilities: list[str]
    achievements: list[str] = Field(default_factory=list)
    technologies: list[str] = Field(default_factory=list)

    @field_validator("start")
    @classmethod
    def validate_start(cls, value: str) -> str:
        _validate_partial_date(value)
        return value

    @field_validator("end")
    @classmethod
    def validate_end(cls, value: str) -> str:
        _validate_period_end(value)
        return value


class Education(KeirekiModel):
    school: str
    start: str
    end: str
    description: str = ""

    @field_validator("start")
    @classmethod
    def validate_start(cls, value: str) -> str:
        _validate_partial_date(value)
        return value

    @field_validator("end")
    @classmethod
    def validate_end(cls, value: str) -> str:
        _validate_period_end(value)
        return value


class Certification(KeirekiModel):
    name: str
    date: str

    @field_validator("date")
    @classmethod
    def validate_date(cls, value: str) -> str:
        _validate_partial_date(value)
        return value


class Language(KeirekiModel):
    name: str
    level: str


class Preferences(KeirekiModel):
    desired_roles: list[str] = Field(default_factory=list)
    desired_areas: list[str] = Field(default_factory=list)
    relocation: str = ""
    visa_support: str = ""
    work_style: str = ""
    management_preference: str = ""
    japanese_communication: str = ""
    request_notes: str = ""


class Profile(KeirekiModel):
    document: Document
    person: Person
    preferences: Preferences = Field(default_factory=Preferences)
    summary: str
    skills: list[SkillGroup] = Field(default_factory=list)
    work_experience: list[WorkExperience]
    education: list[Education]
    certifications: list[Certification] = Field(default_factory=list)
    languages: list[Language] = Field(default_factory=list)
    self_pr: str = ""

    @field_validator("document")
    @classmethod
    def validate_document(cls, value: Document) -> Document:
        _validate_partial_date(value.generated_at)
        return value

    @field_validator("person")
    @classmethod
    def validate_person(cls, value: Person) -> Person:
        _validate_partial_date(value.birth_date)
        return value

    @classmethod
    def from_yaml_data(cls, data: dict[str, Any]) -> Profile:
        return cls.model_validate(data)


def _validate_partial_date(value: str) -> None:
    try:
        parse_partial_date(value)
    except DateParseError as exc:
        raise ValueError(str(exc)) from exc


def _validate_period_end(value: str) -> None:
    try:
        parse_period_end(value)
    except DateParseError as exc:
        raise ValueError(str(exc)) from exc
