"""
Unit Tests
==========

Purpose: Test individual functions and classes in isolation.
These tests verify that each component works correctly on its own.

Run with:
  pytest tests/unit/ -v
  pytest tests/unit/ -m unit

Notes:
  - All external dependencies are mocked
  - Tests are fast and deterministic
  - Focus on edge cases and error handling
"""

import pytest
pytest.skip("Skipped in API-only mode (legacy package imports)", allow_module_level=True)

from pydantic import ValidationError

# from API Service_agent.models.search_criteria import SearchCriteria
# from API Service_agent.models.contact_info import ContactInfo
# from API Service_agent.models.Result import Result


@pytest.mark.unit
def test_search_criteria_requires_non_empty_title():
    with pytest.raises(ValidationError):
        SearchCriteria(title="   ")


@pytest.mark.unit
def test_search_criteria_limit_bounds():
    with pytest.raises(ValidationError):
        SearchCriteria(title="Engineer", limit=0)
    with pytest.raises(ValidationError):
        SearchCriteria(title="Engineer", limit=6001)
    ok = SearchCriteria(title="Engineer", limit=100)
    assert ok.limit == 100


@pytest.mark.unit
def test_contact_info_validates_email_and_linkedin():
    ci = ContactInfo(email="user@example.com")
    assert ci.email == "user@example.com"

    with pytest.raises(ValidationError):
        ContactInfo(email="not-an-email")


@pytest.mark.unit
def test_Result_accepts_contact_info():
    p = Result(name="Ada Lovelace", contact=ContactInfo(email="ada@example.com"))
    assert p.name == "Ada Lovelace"
    assert p.contact and p.contact.email == "ada@example.com"
