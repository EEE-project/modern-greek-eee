import pytest
from modern_greek_eee.greek_utils import PRES_ACT_SLOTS, has_multiple_voices


def test_pres_act_slots_count():
    assert len(PRES_ACT_SLOTS) == 6


def test_slots_canonical_order():
    expected = [
        ("1", "Sing"), ("2", "Sing"), ("3", "Sing"),
        ("1", "Plur"), ("2", "Plur"), ("3", "Plur"),
    ]
    assert [(s["person"], s["number"]) for s in PRES_ACT_SLOTS] == expected


def test_has_multiple_voices_false():
    assert has_multiple_voices(PRES_ACT_SLOTS) is False


def test_has_multiple_voices_true():
    multi = PRES_ACT_SLOTS + [{"tense": "Aor", "voice": "Pass", "person": "1", "number": "Sing"}]
    assert has_multiple_voices(multi) is True


def test_slot_spec_keys():
    for s in PRES_ACT_SLOTS:
        assert {"tense", "voice", "person", "number"} <= s.keys()
