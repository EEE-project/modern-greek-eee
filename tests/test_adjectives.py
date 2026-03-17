#!/usr/bin/env python3
"""
Unit tests for Greek adjective declension validation.

Tests cover 7 main adjective types in Modern Greek:

1. Type καλός (-ός / -ή / -ό)
   Most common type
   Example: καλός (good) → καλή (fem) → καλό (neut)

2. Type τεμπέλης (-ης / -α / -ικο)
   Character adjectives
   Example: τεμπέλης (lazy) → τεμπέλα (fem) → τεμπέλικο (neut)

3. Type ωραίος (-αιος / -α / -ο)
   Similar to καλός but with -αιος
   Example: ωραίος (beautiful) → ωραία (fem) → ωραίο (neut)

4. Type βαθύς (-ύς / -ιά / -ύ)
   Irregular stem changes (more literary)
   Example: βαθύς (deep) → βαθιά (fem) → βαθύ (neut)

5. Type συνεχής (-ής / -ής / -ές)
   Same form for masculine and feminine
   Example: συνεχής (continuous) → συνεχής (fem) → συνεχές (neut)

6. Type κουρασμένος (-μένος / -μένη / -μένο)
   Past participles used as adjectives (very common)
   Example: κουρασμένος (tired) → κουρασμένη (fem) → κουρασμένο (neut)

7. Type μπλε (invariable)
   Borrowed words, don't change for gender
   Example: μπλε (blue) → μπλε (fem) → μπλε (neut)
"""

from unittest.mock import Mock
from modern_greek_eee.greek_utils import check_adjective_test


def make_form(word, values):
    """Helper to create mock form_array object."""
    form = Mock()
    form.value = values
    form.adj_word = word
    return form


# =============================================================================
# Type 1: καλός (-ός / -ή / -ό) - Most common
# =============================================================================

def test_type_kalos_all_correct():
    """Type καλός: All three forms correct."""
    form = make_form('καλός', ['καλός', 'καλή', 'καλό'])
    ok, msg = check_adjective_test('καλός', form)
    assert ok == True, f"Should pass with correct forms. Error: {msg}"


def test_type_kalos_wrong_feminine():
    """Type καλός: Wrong feminine form."""
    form = make_form('καλός', ['καλός', 'wrong', 'καλό'])
    ok, msg = check_adjective_test('καλός', form)
    assert ok == False
    assert 'feminine' in msg
    assert 'entered **"wrong"**' in msg
    assert 'καλή' in msg


def test_type_kalos_case_insensitive():
    """Type καλός: Case-insensitive matching (e.g., Android autocomplete)."""
    form = make_form('καλός', ['Καλός', 'Καλή', 'Καλό'])
    ok, msg = check_adjective_test('καλός', form)
    assert ok == True, f"Should handle uppercase. Error: {msg}"


def test_type_kalos_partial_input():
    """Type καλός: Partial input (only masculine) should not pass."""
    form = make_form('καλός', ['καλός', '', ''])
    ok, msg = check_adjective_test('καλός', form)
    assert ok == False, "Should not pass with empty fields"
    assert msg == '', "Should have no error message for correct partial input"


# =============================================================================
# Type 2: τεμπέλης (-ης / -α / -ικο) - Character adjectives
# =============================================================================

def test_type_tempeli_all_correct():
    """Type τεμπέλης: All three forms correct."""
    form = make_form('τεμπέλης', ['τεμπέλης', 'τεμπέλα', 'τεμπέλικο'])
    ok, msg = check_adjective_test('τεμπέλης', form)
    assert ok == True, f"Should pass. Error: {msg}"


def test_type_tempeli_wrong_neuter():
    """Type τεμπέλης: Wrong neuter form."""
    form = make_form('τεμπέλης', ['τεμπέλης', 'τεμπέλα', 'wrong'])
    ok, msg = check_adjective_test('τεμπέλης', form)
    assert ok == False
    assert 'neuter' in msg
    assert 'τεμπέλικο' in msg


def test_type_ziliarís_all_correct():
    """Type ζηλιάρης: Another -ης adjective."""
    form = make_form('ζηλιάρης', ['ζηλιάρης', 'ζηλιάρα', 'ζηλιάρικο'])
    ok, msg = check_adjective_test('ζηλιάρης', form)
    assert ok == True, f"Should pass. Error: {msg}"


# =============================================================================
# Type 3: ωραίος (-αιος / -α / -ο) - Similar to καλός
# =============================================================================

def test_type_oraios_all_correct():
    """Type ωραίος: All three forms correct."""
    form = make_form('ωραίος', ['ωραίος', 'ωραία', 'ωραίο'])
    ok, msg = check_adjective_test('ωραίος', form)
    assert ok == True, f"Should pass. Error: {msg}"


def test_type_oraios_wrong_feminine():
    """Type ωραίος: Wrong feminine form (e.g., using -η instead of -α)."""
    form = make_form('ωραίος', ['ωραίος', 'wrong', 'ωραίο'])
    ok, msg = check_adjective_test('ωραίος', form)
    assert ok == False
    assert 'feminine' in msg
    assert 'ωραία' in msg


# =============================================================================
# Type 4: βαθύς (-ύς / -ιά / -ύ) - Irregular stem changes
# =============================================================================

def test_type_vathis_all_correct():
    """Type βαθύς: All three forms correct (irregular stem changes)."""
    form = make_form('βαθύς', ['βαθύς', 'βαθιά', 'βαθύ'])
    ok, msg = check_adjective_test('βαθύς', form)
    assert ok == True, f"Should pass. Error: {msg}"


def test_type_vathis_wrong_feminine():
    """Type βαθύς: Wrong feminine form."""
    form = make_form('βαθύς', ['βαθύς', 'wrong', 'βαθύ'])
    ok, msg = check_adjective_test('βαθύς', form)
    assert ok == False
    assert 'βαθιά' in msg


# =============================================================================
# Type 5: συνεχής (-ής / -ής / -ές) - Same form for m/f
# =============================================================================

def test_type_synechis_all_correct():
    """Type συνεχής: Masculine and feminine forms are identical."""
    form = make_form('συνεχής', ['συνεχής', 'συνεχής', 'συνεχές'])
    ok, msg = check_adjective_test('συνεχής', form)
    assert ok == True, f"Should pass. Error: {msg}"


def test_type_synechis_wrong_feminine():
    """Type συνεχής: Wrong feminine (should be same as masculine)."""
    form = make_form('συνεχής', ['συνεχής', 'wrong', 'συνεχές'])
    ok, msg = check_adjective_test('συνεχής', form)
    assert ok == False
    assert 'feminine' in msg
    assert 'συνεχής' in msg


# =============================================================================
# Type 6: κουρασμένος (-μένος / -μένη / -μένο) - Past participles
# =============================================================================

def test_type_kurasmenus_all_correct():
    """Type κουρασμένος: Past participle used as adjective."""
    form = make_form('κουρασμένος', ['κουρασμένος', 'κουρασμένη', 'κουρασμένο'])
    ok, msg = check_adjective_test('κουρασμένος', form)
    assert ok == True, f"Should pass. Error: {msg}"


def test_type_kurasmenus_wrong_feminine():
    """Type κουρασμένος: Wrong feminine form."""
    form = make_form('κουρασμένος', ['κουρασμένος', 'wrong', 'κουρασμένο'])
    ok, msg = check_adjective_test('κουρασμένος', form)
    assert ok == False
    assert 'κουρασμένη' in msg


# =============================================================================
# Type 7: μπλε (invariable) - Borrowed words
# =============================================================================

def test_type_ble_all_correct():
    """Type μπλε: Invariable adjective (same form for all genders)."""
    form = make_form('μπλε', ['μπλε', 'μπλε', 'μπλε'])
    ok, msg = check_adjective_test('μπλε', form)
    assert ok == True, f"Should pass. Error: {msg}"


def test_type_ble_wrong_form():
    """Type μπλε: Wrong form for invariable adjective."""
    form = make_form('μπλε', ['μπλε', 'wrong', 'μπλε'])
    ok, msg = check_adjective_test('μπλε', form)
    assert ok == False
    assert 'feminine' in msg


# =============================================================================
# General behavior tests
# =============================================================================

def test_empty_form():
    """All fields empty should fail with specific message."""
    form = make_form('καλός', ['', '', ''])
    ok, msg = check_adjective_test('καλός', form)
    assert ok == False
    assert 'Please fill in at least one gender form' in msg


def test_wrong_form_object():
    """Wrong word stored in form should return False."""
    form = make_form('wrong_word', ['καλός', 'καλή', 'καλό'])
    form.adj_word = 'different_word'
    ok, msg = check_adjective_test('καλός', form)
    assert ok == False and msg == ""


def test_none_form():
    """None form_array should return False."""
    ok, msg = check_adjective_test('καλός', None)
    assert ok == False and msg == ""


if __name__ == '__main__':
    # Run all tests
    import sys

    test_functions = [
        # Type 1: καλός
        test_type_kalos_all_correct,
        test_type_kalos_wrong_feminine,
        test_type_kalos_case_insensitive,
        test_type_kalos_partial_input,

        # Type 2: τεμπέλης
        test_type_tempeli_all_correct,
        test_type_tempeli_wrong_neuter,
        test_type_ziliarís_all_correct,

        # Type 3: ωραίος
        test_type_oraios_all_correct,
        test_type_oraios_wrong_feminine,

        # Type 4: βαθύς
        test_type_vathis_all_correct,
        test_type_vathis_wrong_feminine,

        # Type 5: συνεχής
        test_type_synechis_all_correct,
        test_type_synechis_wrong_feminine,

        # Type 6: κουρασμένος
        test_type_kurasmenus_all_correct,
        test_type_kurasmenus_wrong_feminine,

        # Type 7: μπλε
        test_type_ble_all_correct,
        test_type_ble_wrong_form,

        # General
        test_empty_form,
        test_wrong_form_object,
        test_none_form,
    ]

    passed = 0
    failed = 0

    for test_func in test_functions:
        try:
            test_func()
            print(f"✓ {test_func.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"✗ {test_func.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test_func.__name__}: {type(e).__name__}: {e}")
            failed += 1

    print(f"\n{'='*60}")
    print(f"Results: {passed} passed, {failed} failed out of {len(test_functions)} tests")
    print(f"{'='*60}")

    sys.exit(0 if failed == 0 else 1)
