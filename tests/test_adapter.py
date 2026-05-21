"""Tests for check_verb_forms adapter in greek_utils."""
import pytest
from types import SimpleNamespace
from unittest.mock import patch, MagicMock

from modern_greek_eee.greek_utils import check_verb_forms, PRES_ACT_SLOTS


def _make_submissions(forms):
    return [
        {**slot, "form": form}
        for slot, form in zip(PRES_ACT_SLOTS, forms)
    ]


_FORMS_6 = ["λύω", "λύεις", "λύει", "λύομεν", "λύετε", "λύουσι"]


def test_adapter_el_routes_to_gu():
    subs = _make_submissions(_FORMS_6)
    with patch("modern_greek_eee.greek_utils.check_verb_test", return_value=(True, "")) as mock_cvt:
        check_verb_forms("λύω", subs, "el")
    mock_cvt.assert_called_once()
    _, fa, tense = mock_cvt.call_args[0]
    assert tense == "present"
    assert fa.value == _FORMS_6
    assert fa.verb_word == "λύω"


def test_adapter_el_canonical_order():
    subs = _make_submissions(_FORMS_6)
    with patch("modern_greek_eee.greek_utils.check_verb_test", return_value=(True, "")) as mock_cvt:
        check_verb_forms("λύω", subs, "el")
    _, fa, _ = mock_cvt.call_args[0]
    assert fa.value == _FORMS_6


def test_adapter_grc_routes_per_slot():
    subs = _make_submissions(_FORMS_6)
    mock_ag = MagicMock()
    mock_ag.check_verb.return_value = (True, "")
    with patch.dict("sys.modules", {"ancient_greek_eee": mock_ag}):
        check_verb_forms("λύω", subs, "grc")
    assert mock_ag.check_verb.call_count == 6


def test_adapter_grc_aggregates_results():
    subs = _make_submissions(_FORMS_6)
    mock_ag = MagicMock()
    mock_ag.check_verb.return_value = (True, "")
    with patch.dict("sys.modules", {"ancient_greek_eee": mock_ag}):
        results = check_verb_forms("λύω", subs, "grc")
    assert len(results) == 6
    for r in results:
        assert set(r.keys()) == {"ok", "msg", "slot"}


def test_adapter_uniform_return_type():
    subs = _make_submissions(_FORMS_6)
    mock_ag = MagicMock()
    mock_ag.check_verb.return_value = (False, "wrong")
    with patch("modern_greek_eee.greek_utils.check_verb_test", return_value=(False, "err")):
        el_results = check_verb_forms("λύω", subs, "el")
    with patch.dict("sys.modules", {"ancient_greek_eee": mock_ag}):
        grc_results = check_verb_forms("λύω", subs, "grc")
    for results in (el_results, grc_results):
        assert isinstance(results, list)
        assert all(set(r.keys()) == {"ok", "msg", "slot"} for r in results)


def test_adapter_unknown_language_raises():
    subs = _make_submissions(_FORMS_6)
    with pytest.raises(ValueError, match="Unknown language"):
        check_verb_forms("λύω", subs, "hbo")
