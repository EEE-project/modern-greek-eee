#!/usr/bin/env python3
"""
Unit tests for Greek noun declension validation.

Tests cover noun declension in simple and article modes.

Simple Mode: Tests bare noun forms (6 cases)
- Singular: Nominative, Accusative, Genitive
- Plural: Nominative, Accusative, Genitive

Article Mode: Tests nouns with articles (9 forms total)
- Definite article (ο/η/το) + 6 cases
- Indefinite article (ένας/μία/ένα) + 3 singular cases
"""

from unittest.mock import Mock
from modern_greek_eee.greek_utils import check_noun_test


def make_form(word, values):
    """Helper to create mock form_array object."""
    form = Mock()
    form.value = values
    form.test_word = word
    return form


# =============================================================================
# Masculine Nouns (-ος type)
# Example: ο άνθρωπος (the man)
# =============================================================================

def test_masculine_os_simple_all_correct():
    """Masculine -ος noun in simple mode (all 6 cases correct)."""
    # ο άνθρωπος
    form = make_form('άνθρωπος', [
        'άνθρωπος',  # Sg. Nom.
        'άνθρωπο',   # Sg. Acc.
        'ανθρώπου',  # Sg. Gen.
        'άνθρωποι',  # Pl. Nom.
        'ανθρώπους', # Pl. Acc.
        'ανθρώπων'   # Pl. Gen.
    ])
    ok = check_noun_test('άνθρωπος', form, mode='simple')
    assert ok == True, "Should pass with all correct forms"


def test_masculine_os_simple_wrong_accusative():
    """Masculine -ος noun: wrong accusative form."""
    form = make_form('άνθρωπος', [
        'άνθρωπος',  # Sg. Nom.
        'wrong',     # Sg. Acc. - WRONG
        'ανθρώπου',  # Sg. Gen.
        'άνθρωποι',  # Pl. Nom.
        'ανθρώπους', # Pl. Acc.
        'ανθρώπων'   # Pl. Gen.
    ])
    ok = check_noun_test('άνθρωπος', form, mode='simple')
    assert ok == False, "Should fail with wrong accusative"


def test_masculine_os_case_insensitive():
    """Masculine -ος noun: Case-insensitive matching."""
    form = make_form('άνθρωπος', [
        'Άνθρωπος',  # Uppercase
        'Άνθρωπο',
        'Ανθρώπου',
        'Άνθρωποι',
        'Ανθρώπους',
        'Ανθρώπων'
    ])
    ok = check_noun_test('άνθρωπος', form, mode='simple')
    assert ok == True, "Should handle uppercase"


# =============================================================================
# Feminine Nouns (-η type)
# Example: η ώρα (the hour)
# =============================================================================

def test_feminine_i_simple_all_correct():
    """Feminine -η/-ας noun in simple mode."""
    # η ώρα
    form = make_form('ώρα', [
        'ώρα',       # Sg. Nom.
        'ώρα',       # Sg. Acc.
        'ώρας',      # Sg. Gen.
        'ώρες',      # Pl. Nom.
        'ώρες',      # Pl. Acc.
        'ωρών'       # Pl. Gen.
    ])
    ok = check_noun_test('ώρα', form, mode='simple')
    assert ok == True, "Should pass"


def test_feminine_i_simple_wrong_genitive():
    """Feminine -η noun: wrong genitive form."""
    form = make_form('ώρα', [
        'ώρα',       # Sg. Nom.
        'ώρα',       # Sg. Acc.
        'wrong',     # Sg. Gen. - WRONG
        'ώρες',      # Pl. Nom.
        'ώρες',      # Pl. Acc.
        'ωρών'       # Pl. Gen.
    ])
    ok = check_noun_test('ώρα', form, mode='simple')
    assert ok == False, "Should fail with wrong genitive"


# =============================================================================
# Neuter Nouns (-ο type)
# Example: το παιδί (the child)
# =============================================================================

def test_neuter_o_simple_all_correct():
    """Neuter -ο/-ι noun in simple mode."""
    # το παιδί
    form = make_form('παιδί', [
        'παιδί',     # Sg. Nom.
        'παιδί',     # Sg. Acc.
        'παιδιού',   # Sg. Gen.
        'παιδιά',    # Pl. Nom.
        'παιδιά',    # Pl. Acc.
        'παιδιών'    # Pl. Gen.
    ])
    ok = check_noun_test('παιδί', form, mode='simple')
    assert ok == True, "Should pass"


def test_neuter_o_simple_partial_input():
    """Neuter noun: Partial input should fail."""
    form = make_form('παιδί', [
        'παιδί',     # Sg. Nom.
        '',          # Sg. Acc. - EMPTY
        'παιδιού',   # Sg. Gen.
        'παιδιά',    # Pl. Nom.
        'παιδιά',    # Pl. Acc.
        'παιδιών'    # Pl. Gen.
    ])
    ok = check_noun_test('παιδί', form, mode='simple')
    assert ok == False, "Should fail with empty field"


# =============================================================================
# Article Mode Tests
# =============================================================================

def test_masculine_with_definite_article():
    """Masculine noun with definite article (ο/του/τον/οι/τους/των)."""
    form = make_form('ο άνθρωπος', [
        'ο άνθρωπος',      # Def. Sg. Nom.
        'τον άνθρωπο',     # Def. Sg. Acc.
        'του ανθρώπου',    # Def. Sg. Gen.
        'οι άνθρωποι',     # Def. Pl. Nom.
        'τους ανθρώπους',  # Def. Pl. Acc.
        'των ανθρώπων',    # Def. Pl. Gen.
        'ένας άνθρωπος',   # Indef. Sg. Nom.
        'έναν άνθρωπο',    # Indef. Sg. Acc.
        'ενός ανθρώπου'    # Indef. Sg. Gen.
    ])
    ok = check_noun_test('ο άνθρωπος', form, mode='article')
    assert ok == True, "Should pass with all correct article forms"


def test_feminine_with_definite_article():
    """Feminine noun with definite article (η/της/την/οι/τις/των)."""
    form = make_form('η ώρα', [
        'η ώρα',           # Def. Sg. Nom.
        'την ώρα',         # Def. Sg. Acc.
        'της ώρας',        # Def. Sg. Gen.
        'οι ώρες',         # Def. Pl. Nom.
        'τις ώρες',        # Def. Pl. Acc.
        'των ωρών',        # Def. Pl. Gen.
        'μία ώρα',         # Indef. Sg. Nom.
        'μία ώρα',         # Indef. Sg. Acc.
        'μίας ώρας'        # Indef. Sg. Gen.
    ])
    ok = check_noun_test('η ώρα', form, mode='article')
    assert ok == True, "Should pass"


def test_neuter_with_definite_article():
    """Neuter noun with definite article (το/του/το/τα/τα/των)."""
    form = make_form('το παιδί', [
        'το παιδί',         # Def. Sg. Nom. (το)
        'του παιδί',        # Def. Sg. Acc. (του - accusative is same as genitive article for neuter)
        'το παιδιού',       # Def. Sg. Gen. (το - genitive article is same as nominative for neuter)
        'τα παιδιά',        # Def. Pl. Nom.
        'τα παιδιά',        # Def. Pl. Acc.
        'των παιδιών',      # Def. Pl. Gen.
        'ένα παιδί',        # Indef. Sg. Nom.
        'ένα παιδί',        # Indef. Sg. Acc.
        'ενός παιδιού'      # Indef. Sg. Gen.
    ])
    ok = check_noun_test('το παιδί', form, mode='article')
    assert ok == True, "Should pass"


def test_article_mode_wrong_genitive():
    """Article mode: Wrong genitive form."""
    form = make_form('ο άνθρωπος', [
        'ο άνθρωπος',      # Def. Sg. Nom.
        'τον άνθρωπο',     # Def. Sg. Acc.
        'wrong',           # Def. Sg. Gen. - WRONG
        'οι άνθρωποι',     # Def. Pl. Nom.
        'τους ανθρώπους',  # Def. Pl. Acc.
        'των ανθρώπων',    # Def. Pl. Gen.
        'ένας άνθρωπος',   # Indef. Sg. Nom.
        'έναν άνθρωπο',    # Indef. Sg. Acc.
        'ενός ανθρώπου'    # Indef. Sg. Gen.
    ])
    ok = check_noun_test('ο άνθρωπος', form, mode='article')
    assert ok == False, "Should fail with wrong genitive"


# =============================================================================
# General behavior tests
# =============================================================================

def test_empty_form():
    """All fields empty should fail."""
    form = make_form('άνθρωπος', ['', '', '', '', '', ''])
    ok = check_noun_test('άνθρωπος', form, mode='simple')
    assert ok == False, "Should fail with all empty fields"


def test_wrong_word_stored():
    """Wrong word stored in form should fail."""
    form = make_form('wrong_word', [
        'άνθρωπος', 'άνθρωπο', 'ανθρώπου',
        'άνθρωποι', 'ανθρώπους', 'ανθρώπων'
    ])
    form.test_word = 'different_word'
    ok = check_noun_test('άνθρωπος', form, mode='simple')
    assert ok == False, "Should fail when word doesn't match"


def test_none_form():
    """None form_array should fail."""
    ok = check_noun_test('άνθρωπος', None, mode='simple')
    assert ok == False, "Should fail with None form"


if __name__ == '__main__':
    import sys

    test_functions = [
        # Masculine -ος
        test_masculine_os_simple_all_correct,
        test_masculine_os_simple_wrong_accusative,
        test_masculine_os_case_insensitive,

        # Feminine -η
        test_feminine_i_simple_all_correct,
        test_feminine_i_simple_wrong_genitive,

        # Neuter -ο
        test_neuter_o_simple_all_correct,
        test_neuter_o_simple_partial_input,

        # Article mode
        test_masculine_with_definite_article,
        test_feminine_with_definite_article,
        test_neuter_with_definite_article,
        test_article_mode_wrong_genitive,

        # General
        test_empty_form,
        test_wrong_word_stored,
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
