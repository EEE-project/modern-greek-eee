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


def make_form(word, values, is_pluralia_tantum=False):
    """Helper to create mock form_array object."""
    form = Mock()
    form.value = values
    form.test_word = word
    form.is_pluralia_tantum = is_pluralia_tantum
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
    """Neuter noun with definite article (το/το/του/τα/τα/των).

    Neuter nouns have the same form for nominative and accusative.
    Article forms: NOM/ACC='το', GEN='του' (PR #2 fix in v2.0.8)
    """
    form = make_form('το παιδί', [
        'το παιδί',         # Def. Sg. Nom. (το)
        'το παιδί',         # Def. Sg. Acc. (το - same as nominative for neuter)
        'του παιδιού',      # Def. Sg. Gen. (του - different from nominative/accusative)
        'τα παιδιά',        # Def. Pl. Nom.
        'τα παιδιά',        # Def. Pl. Acc.
        'των παιδιών',      # Def. Pl. Gen.
        'ένα παιδί',        # Indef. Sg. Nom.
        'ένα παιδί',        # Indef. Sg. Acc.
        'ενός παιδιού'      # Indef. Sg. Gen.
    ])
    ok = check_noun_test('το παιδί', form, mode='article')
    assert ok == True, "Should pass"


def test_common_gender_masculine_article():
    """Common-gender noun used as masculine (ο μηχανικός) — article mode must accept ο forms."""
    form = make_form('ο μηχανικός', [
        'ο μηχανικός',      # Def. Sg. Nom.
        'τον μηχανικό',     # Def. Sg. Acc.
        'του μηχανικού',    # Def. Sg. Gen.
        'οι μηχανικοί',     # Def. Pl. Nom.
        'τους μηχανικούς',  # Def. Pl. Acc.
        'των μηχανικών',    # Def. Pl. Gen.
        'ένας μηχανικός',   # Indef. Sg. Nom.
        'έναν μηχανικό',    # Indef. Sg. Acc.
        'ενός μηχανικού',   # Indef. Sg. Gen.
    ])
    ok = check_noun_test('ο μηχανικός', form, mode='article')
    assert ok == True, "ο μηχανικός: masculine article forms should pass"


def test_common_gender_feminine_article():
    """Common-gender noun used as feminine (η μηχανικός) — article mode must accept η forms."""
    form = make_form('η μηχανικός', [
        'η μηχανικός',      # Def. Sg. Nom.
        'την μηχανικό',     # Def. Sg. Acc.
        'της μηχανικού',    # Def. Sg. Gen.
        'οι μηχανικοί',     # Def. Pl. Nom.
        'τις μηχανικούς',   # Def. Pl. Acc.
        'των μηχανικών',    # Def. Pl. Gen.
        'μια μηχανικός',    # Indef. Sg. Nom.
        'μια μηχανικό',     # Indef. Sg. Acc.
        'μιας μηχανικού',   # Indef. Sg. Gen.
    ])
    ok = check_noun_test('η μηχανικός', form, mode='article')
    assert ok == True, "η μηχανικός: feminine article forms should pass"


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


# =============================================================================
# Nouns with missing gen.pl (library returns {''}) — active_cases must skip it
# =============================================================================

def make_form_with_active_cases(word, values, active_cases, is_pluralia_tantum=False):
    """Helper for forms that carry active_cases (as created by create_noun_test_ui)."""
    form = Mock()
    form.value = values
    form.test_word = word
    form.is_pluralia_tantum = is_pluralia_tantum
    form.active_cases = active_cases
    return form


def test_noun_without_gen_pl_simple_correct():
    """κούτα: 5-field form (pl.gen skipped) with correct values passes."""
    active = [['sg', 'nom'], ['sg', 'acc'], ['sg', 'gen'], ['pl', 'nom'], ['pl', 'acc']]
    form = make_form_with_active_cases('η κούτα', [
        'κούτα', 'κούτα', 'κούτας', 'κούτες', 'κούτες'
    ], active)
    ok = check_noun_test('η κούτα', form, mode='simple')
    assert ok == True, "Should pass without gen.pl field"


def test_noun_without_gen_pl_simple_wrong():
    """κούτα: wrong sg.gen should still fail."""
    active = [['sg', 'nom'], ['sg', 'acc'], ['sg', 'gen'], ['pl', 'nom'], ['pl', 'acc']]
    form = make_form_with_active_cases('η κούτα', [
        'κούτα', 'κούτα', 'wrong', 'κούτες', 'κούτες'
    ], active)
    ok = check_noun_test('η κούτα', form, mode='simple')
    assert ok == False, "Should fail with wrong sg.gen"


def test_nfd_accent_normalization():
    """NFD-encoded input (combining accent) must match NFC library forms."""
    import unicodedata
    from modern_greek_eee.greek_utils import _ci_match
    nfc = 'κούτες'
    nfd = unicodedata.normalize('NFD', nfc)
    assert nfc != nfd, "test pre-condition: NFD and NFC must differ"
    assert _ci_match(nfd, {nfc}), "NFD input must match NFC library form"
    assert _ci_match(nfc, {nfd}), "NFC input must match NFD library form"

    # Also verify via full check_noun_test with a feminine noun (avoids τα special path)
    active = [['sg', 'nom'], ['sg', 'acc'], ['sg', 'gen'], ['pl', 'nom'], ['pl', 'acc']]
    nfd_pl = unicodedata.normalize('NFD', 'κούτες')
    form = make_form_with_active_cases('η κούτα', [
        'κούτα', 'κούτα', 'κούτας', nfd_pl, nfd_pl
    ], active)
    ok = check_noun_test('η κούτα', form, mode='simple')
    assert ok == True, "NFD-encoded plural input should pass noun test"


def test_garsoniera_without_gen_pl():
    """γκαρσονιέρα: 5-field form (pl.gen skipped) with correct values passes."""
    active = [['sg', 'nom'], ['sg', 'acc'], ['sg', 'gen'], ['pl', 'nom'], ['pl', 'acc']]
    form = make_form_with_active_cases('η γκαρσονιέρα', [
        'γκαρσονιέρα', 'γκαρσονιέρα', 'γκαρσονιέρας', 'γκαρσονιέρες', 'γκαρσονιέρες'
    ], active)
    ok = check_noun_test('η γκαρσονιέρα', form, mode='simple')
    assert ok == True, "Should pass without gen.pl field"


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
        test_common_gender_masculine_article,
        test_common_gender_feminine_article,

        # General
        test_empty_form,
        test_wrong_word_stored,
        test_none_form,

        # Missing gen.pl
        test_noun_without_gen_pl_simple_correct,
        test_noun_without_gen_pl_simple_wrong,
        test_garsoniera_without_gen_pl,
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
