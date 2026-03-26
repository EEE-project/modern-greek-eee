#!/usr/bin/env python3
"""
Unit tests for Greek verb conjugation validation.

Tests cover verb conjugation in multiple tenses:

1. Present (Ενεστώτας) - ongoing or habitual actions
2. Imperfect (Παρατατικός) - past continuous or habitual
3. Aorist (Αόριστος) - completed single action in past
4. Simple Future (Απλός Μέλλοντας) - single completed action in future (θα + aorist)
5. Continuous Future (Συνεχής Μέλλοντας) - ongoing action in future (θα + present)
6. Simple Subjunctive (Απλή Υποτακτική) - single action subjunctive (να + aorist)

Each tense has 6 forms (singular and plural for 1st, 2nd, 3rd person).
"""

from unittest.mock import Mock
from modern_greek_eee.greek_utils import check_verb_test


def make_form(verb, values):
    """Helper to create mock form_array object."""
    form = Mock()
    form.value = values
    form.verb_word = verb
    return form


# =============================================================================
# Present Tense (Ενεστώτας)
# Example: λύω (to solve)
# =============================================================================

def test_present_all_correct():
    """Present tense: All 6 forms correct."""
    form = make_form('λύω', [
        'λύω',       # εγώ (1st sg)
        'λύεις',     # εσύ (2nd sg)
        'λύει',      # αυτός (3rd sg)
        'λύουμε',    # εμείς (1st pl)
        'λύετε',     # εσείς (2nd pl)
        'λύουν'      # αυτοί (3rd pl)
    ])
    ok, _ = check_verb_test('λύω', form, 'present')
    assert ok == True, "Should pass with all correct forms"


def test_present_wrong_form():
    """Present tense: Wrong form for εσύ."""
    form = make_form('λύω', [
        'λύω',       # εγώ
        'wrong',     # εσύ - WRONG
        'λύει',      # αυτός
        'λύουμε',    # εμείς
        'λύετε',     # εσείς
        'λύουν'      # αυτοί
    ])
    ok, msg = check_verb_test('λύω', form, 'present')
    assert ok == False
    assert 'entered' in msg.lower()


def test_present_case_insensitive():
    """Present tense: Case-insensitive matching."""
    form = make_form('λύω', [
        'Λύω',       # Uppercase
        'Λύεις',
        'Λύει',
        'Λύουμε',
        'Λύετε',
        'Λύουν'
    ])
    ok, _ = check_verb_test('λύω', form, 'present')
    assert ok == True, "Should handle uppercase"


# =============================================================================
# Imperfect Tense (Παρατατικός)
# Example: έλυα (I was solving)
# =============================================================================

def test_imperfect_all_correct():
    """Imperfect tense: All 6 forms correct."""
    form = make_form('λύω', [
        'έλυα',      # εγώ
        'έλυες',     # εσύ
        'έλυε',      # αυτός
        'ελύαμε',    # εμείς (accent on ε)
        'ελύατε',    # εσείς (accent on ε)
        'ελύανε'     # αυτοί (or έλυαν)
    ])
    ok, _ = check_verb_test('λύω', form, 'imperfect')
    assert ok == True, "Should pass"


def test_imperfect_wrong_plural():
    """Imperfect tense: Wrong plural form."""
    form = make_form('λύω', [
        'έλυα',      # εγώ
        'έλυες',     # εσύ
        'έλυε',      # αυτός
        'wrong',     # εμείς - WRONG
        'λύατε',     # εσείς
        'έλυαν'      # αυτοί
    ])
    ok, msg = check_verb_test('λύω', form, 'imperfect')
    assert ok == False


# =============================================================================
# Aorist Tense (Αόριστος)
# Example: έλυσα (I solved)
# =============================================================================

def test_aorist_all_correct():
    """Aorist tense: All 6 forms correct."""
    form = make_form('λύω', [
        'έλυσα',     # εγώ
        'έλυσες',    # εσύ
        'έλυσε',     # αυτός
        'λύσαμε',    # εμείς
        'λύσατε',    # εσείς
        'έλυσαν'     # αυτοί
    ])
    ok, _ = check_verb_test('λύω', form, 'aorist')
    assert ok == True, "Should pass"


def test_aorist_partial_input():
    """Aorist tense: Partial input (empty field) should fail."""
    form = make_form('λύω', [
        'έλυσα',     # εγώ
        '',          # εσύ - EMPTY
        'έλυσε',     # αυτός
        'λύσαμε',    # εμείς
        'λύσατε',    # εσείς
        'έλυσαν'     # αυτοί
    ])
    ok, msg = check_verb_test('λύω', form, 'aorist')
    assert ok == False, "Should fail with empty field"
    assert msg == '', "Should have no error message"


# =============================================================================
# Simple Future (Απλός Μέλλοντας)
# Prefix: θα + aorist stem
# Example: θα λύσω (I will solve)
# =============================================================================

def test_simple_future_all_correct():
    """Simple Future tense: All 6 forms with θα prefix."""
    form = make_form('λύω', [
        'θα λύσω',   # εγώ
        'θα λύσεις', # εσύ
        'θα λύσει',  # αυτός
        'θα λύσουμε',# εμείς
        'θα λύσετε', # εσείς
        'θα λύσουν'  # αυτοί
    ])
    ok, _ = check_verb_test('λύω', form, 'future')
    assert ok == True, "Should pass"


def test_simple_future_missing_prefix():
    """Simple Future: Missing θα prefix should fail."""
    form = make_form('λύω', [
        'λύσω',      # εγώ - NO PREFIX
        'θα λύσεις', # εσύ
        'θα λύσει',  # αυτός
        'θα λύσουμε',# εμείς
        'θα λύσετε', # εσείς
        'θα λύσουν'  # αυτοί
    ])
    ok, msg = check_verb_test('λύω', form, 'future')
    assert ok == False
    assert 'θα' in msg or 'prefix' in msg.lower()


def test_simple_future_case_insensitive():
    """Simple Future: Case-insensitive (Θα Λύσω)."""
    form = make_form('λύω', [
        'Θα Λύσω',   # Uppercase
        'Θα Λύσεις',
        'Θα Λύσει',
        'Θα Λύσουμε',
        'Θα Λύσετε',
        'Θα Λύσουν'
    ])
    ok, _ = check_verb_test('λύω', form, 'future')
    assert ok == True, "Should handle uppercase"


# =============================================================================
# Continuous Future (Συνεχής Μέλλοντας)
# Prefix: θα + present stem
# Example: θα λύω (I will be solving)
# =============================================================================

def test_continuous_future_all_correct():
    """Continuous Future: All 6 forms with θα prefix."""
    form = make_form('λύω', [
        'θα λύω',    # εγώ
        'θα λύεις',  # εσύ
        'θα λύει',   # αυτός
        'θα λύουμε', # εμείς
        'θα λύετε',  # εσείς
        'θα λύουν'   # αυτοί
    ])
    ok, _ = check_verb_test('λύω', form, 'future_continuous')
    assert ok == True, "Should pass"


def test_continuous_future_wrong_form():
    """Continuous Future: Wrong form."""
    form = make_form('λύω', [
        'θα λύω',    # εγώ
        'wrong',     # εσύ - WRONG
        'θα λύει',   # αυτός
        'θα λύουμε', # εμείς
        'θα λύετε',  # εσείς
        'θα λύουν'   # αυτοί
    ])
    ok, msg = check_verb_test('λύω', form, 'future_continuous')
    assert ok == False


# =============================================================================
# Simple Subjunctive (Απλή Υποτακτική)
# Prefix: να + aorist stem
# Example: να λύσω (that I solve / in order to solve)
# =============================================================================

def test_simple_subjunctive_all_correct():
    """Simple Subjunctive: All 6 forms with να prefix."""
    form = make_form('λύω', [
        'να λύσω',   # εγώ
        'να λύσεις', # εσύ
        'να λύσει',  # αυτός
        'να λύσουμε',# εμείς
        'να λύσετε', # εσείς
        'να λύσουν'  # αυτοί
    ])
    ok, _ = check_verb_test('λύω', form, 'subjunctive_simple')
    assert ok == True, "Should pass"


def test_simple_subjunctive_wrong_prefix():
    """Simple Subjunctive: Wrong prefix (θα instead of να)."""
    form = make_form('λύω', [
        'θα λύσω',   # εγώ - WRONG PREFIX
        'να λύσεις', # εσύ
        'να λύσει',  # αυτός
        'να λύσουμε',# εμείς
        'να λύσετε', # εσείς
        'να λύσουν'  # αυτοί
    ])
    ok, msg = check_verb_test('λύω', form, 'subjunctive_simple')
    assert ok == False
    assert 'να' in msg or 'prefix' in msg.lower()


# =============================================================================
# Simple Conditional (Υποθετική Απλή)
# Prefix: αν + aorist stem
# Example: αν λύσω (if I solve - one-time event)
# =============================================================================

def test_conditional_simple_all_correct():
    """Simple Conditional: All 6 forms with αν prefix (conjunctive forms)."""
    form = make_form('λύω', [
        'αν λύσω',    # εγώ - conjunctive
        'αν λύσεις',  # εσύ
        'αν λύσει',   # αυτός
        'αν λύσουμε', # εμείς (or λύσομε)
        'αν λύσετε',  # εσείς
        'αν λύσουν'   # αυτοί (or λύσουνε)
    ])
    ok, _ = check_verb_test('λύω', form, 'conditional_simple')
    assert ok == True, "Should accept conjunctive forms with αν prefix"


def test_conditional_simple_wrong_tense():
    """Simple Conditional: Wrong tense (present instead of conjunctive)."""
    form = make_form('λύω', [
        'αν λύω',    # εγώ - WRONG: present, not conjunctive
        'αν λύσεις', # εσύ - correct conjunctive
        'αν λύσει',  # αυτός
        'αν λύσουμε',# εμείς
        'αν λύσετε', # εσείς
        'αν λύσουν'  # αυτοί
    ])
    ok, msg = check_verb_test('λύω', form, 'conditional_simple')
    assert ok == False, "Should reject present forms (needs conjunctive)"


def test_conditional_simple_wrong_prefix():
    """Simple Conditional: Wrong prefix (να instead of αν)."""
    form = make_form('λύω', [
        'να λύσω',   # εγώ - WRONG PREFIX
        'να λύσεις', # εσύ
        'να λύσει',  # αυτός
        'να λύσουμε',# εμείς
        'να λύσετε', # εσείς
        'να λύσουν'  # αυτοί
    ])
    ok, msg = check_verb_test('λύω', form, 'conditional_simple')
    assert ok == False, "Should reject να prefix (needs αν for conditional)"


def test_conditional_simple_aorist_verb():
    """Simple Conditional: With different verb (αρχίζω)."""
    form = make_form('αρχίζω', [
        'αν αρχίσω',   # εγώ - conjunctive
        'αν αρχίσεις', # εσύ
        'αν αρχίσει',  # αυτός
        'αν αρχίσουμε',# εμείς
        'αν αρχίσετε', # εσείς
        'αν αρχίσουν'  # αυτοί
    ])
    ok, _ = check_verb_test('αρχίζω', form, 'conditional_simple')
    assert ok == True, "Should work with different verb's conjunctive forms"


# =============================================================================
# Continuous Conditional (Υποθετική Συνεχής)
# Prefix: αν + present stem
# Example: αν λύω (if I solve - habitual/repeated events)
# =============================================================================

def test_conditional_continuous_all_correct():
    """Continuous Conditional: All 6 forms with αν prefix (present forms)."""
    form = make_form('λύω', [
        'αν λύω',    # εγώ
        'αν λύεις',  # εσύ
        'αν λύει',   # αυτός
        'αν λύουμε', # εμείς
        'αν λύετε',  # εσείς
        'αν λύουν'   # αυτοί
    ])
    ok, _ = check_verb_test('λύω', form, 'conditional_continuous')
    assert ok == True, "Should accept present forms with αν prefix"


def test_conditional_continuous_wrong_tense():
    """Continuous Conditional: Wrong tense (aorist instead of present)."""
    form = make_form('λύω', [
        'αν λύσω',   # εγώ - WRONG: aorist, not present
        'αν λύεις',  # εσύ - correct present
        'αν λύει',   # αυτός
        'αν λύουμε', # εμείς
        'αν λύετε',  # εσείς
        'αν λύουν'   # αυτοί
    ])
    ok, msg = check_verb_test('λύω', form, 'conditional_continuous')
    assert ok == False, "Should reject aorist forms (needs present)"


def test_conditional_continuous_wrong_prefix():
    """Continuous Conditional: Wrong prefix (να instead of αν)."""
    form = make_form('λύω', [
        'να λύω',    # εγώ - WRONG PREFIX
        'να λύεις',  # εσύ
        'να λύει',   # αυτός
        'να λύουμε', # εμείς
        'να λύετε',  # εσείς
        'να λύουν'   # αυτοί
    ])
    ok, msg = check_verb_test('λύω', form, 'conditional_continuous')
    assert ok == False, "Should reject να prefix (needs αν for conditional)"


def test_conditional_continuous_present_verb():
    """Continuous Conditional: With different verb (αρχίζω)."""
    form = make_form('αρχίζω', [
        'αν αρχίζω',  # εγώ
        'αν αρχίζεις',# εσύ
        'αν αρχίζει', # αυτός
        'αν αρχίζουμε',# εμείς
        'αν αρχίζετε',# εσείς
        'αν αρχίζουν' # αυτοί
    ])
    ok, _ = check_verb_test('αρχίζω', form, 'conditional_continuous')
    assert ok == True, "Should work with different verb's present forms"


# =============================================================================
# Irregular Verb: λέω (to say)
# =============================================================================

def test_irregular_future():
    """Irregular verb λέω with complete stem change in future."""
    form = make_form('λέω', [
        'θα πω',      # εγώ (stem changes to π-)
        'θα πεις',    # εσύ
        'θα πει',     # αυτός
        'θα πούμε',   # εμείς
        'θα πείτε',   # εσείς
        'θα πουν'     # αυτοί (without accent, or πούνε)
    ])
    ok, _ = check_verb_test('λέω', form, 'future')
    assert ok == True, "Should handle irregular verbs"


# =============================================================================
# Stem Change Verbs: αγοράζω (to buy)
# Type A: -ζω → -σω
# =============================================================================

def test_type_a_future():
    """Type A verb: -ζω → -σω in future."""
    form = make_form('αγοράζω', [
        'θα αγοράσω', # εγώ
        'θα αγοράσεις',
        'θα αγοράσει',
        'θα αγοράσουμε',
        'θα αγοράσετε',
        'θα αγοράσουν'
    ])
    ok, _ = check_verb_test('αγοράζω', form, 'future')
    assert ok == True, "Should handle stem changes"


# =============================================================================
# General behavior tests
# =============================================================================

def test_empty_form():
    """All fields empty should fail."""
    form = make_form('λύω', ['', '', '', '', '', ''])
    ok, _ = check_verb_test('λύω', form, 'present')
    assert ok == False, "Should fail with all empty fields"


def test_wrong_word_stored():
    """Wrong word stored in form should fail."""
    form = make_form('wrong_word', ['λύω', 'λύεις', 'λύει', 'λύουμε', 'λύετε', 'λύουν'])
    form.verb_word = 'different_word'
    ok, _ = check_verb_test('λύω', form, 'present')
    assert ok == False, "Should fail when word doesn't match"


def test_none_form():
    """None form_array should fail."""
    ok, _ = check_verb_test('λύω', None, 'present')
    assert ok == False, "Should fail with None form"


def test_unknown_tense():
    """Unknown tense should fail."""
    form = make_form('λύω', ['λύω', 'λύεις', 'λύει', 'λύουμε', 'λύετε', 'λύουν'])
    ok, msg = check_verb_test('λύω', form, 'unknown_tense')
    assert ok == False
    assert 'unknown' in msg.lower() or 'error' in msg.lower()


if __name__ == '__main__':
    import sys

    test_functions = [
        # Present
        test_present_all_correct,
        test_present_wrong_form,
        test_present_case_insensitive,

        # Imperfect
        test_imperfect_all_correct,
        test_imperfect_wrong_plural,

        # Aorist
        test_aorist_all_correct,
        test_aorist_partial_input,

        # Simple Future
        test_simple_future_all_correct,
        test_simple_future_missing_prefix,
        test_simple_future_case_insensitive,

        # Continuous Future
        test_continuous_future_all_correct,
        test_continuous_future_wrong_form,

        # Simple Subjunctive
        test_simple_subjunctive_all_correct,
        test_simple_subjunctive_wrong_prefix,

        # Conditional Simple
        test_conditional_simple_all_correct,
        test_conditional_simple_wrong_tense,
        test_conditional_simple_wrong_prefix,
        test_conditional_simple_aorist_verb,

        # Conditional Continuous
        test_conditional_continuous_all_correct,
        test_conditional_continuous_wrong_tense,
        test_conditional_continuous_wrong_prefix,
        test_conditional_continuous_present_verb,

        # Irregular verbs
        test_irregular_future,

        # Stem changes
        test_type_a_future,

        # General
        test_empty_form,
        test_wrong_word_stored,
        test_none_form,
        test_unknown_tense,
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
