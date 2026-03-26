# Changelog

All notable changes to this project are documented in this file.

## Version 0.3.0 (March 26, 2026)

### Added

- **New Conditional Tense Support:**
  - Added `conditional_simple` tense for one-time conditional events (uses conjunctive/subjunctive aorist forms)
    - Example: "Αν διαβάσεις, θα περάσεις" (If you read once, you will pass)
  - Added `conditional_continuous` tense for habitual/repeated conditional events (uses present forms)
    - Example: "Αν διαβάζεις, θα μαθαίνεις" (If you read regularly, you will learn)
  - Both conditional tenses display context prefix "αν" in field labels for UI clarity
  - 8 unit tests covering conditional tense validation

- **Centralized Tense Configuration:**
  - Created `TENSE_LABELS` constant for unified tense terminology management
  - Consolidates tense metadata: Greek name, English name, feedback, dropdown label, context prefix
  - All 10 tenses (8 original + 2 new conditionals) centralized in single location
  - Simplifies future tense additions: only need to add one TENSE_LABELS entry

- **Comprehensive Adjective Test Coverage:**
  - Added 10 complex mode (18-field) adjective test cases
  - Complex mode covers all adjective declensions: 3 genders × 2 numbers × 3 cases
  - Tests cover multiple adjective types: καλός, μεγάλος, ωραίος, βαθύς, συνεχής, κουρασμένος
  - Coverage now includes both adjective modes: simple (6-field) and complex (18-field)

### Changed

- **Refactored tense label definitions:**
  - Moved from 3 scattered locations (greek_verbs.py, greek_utils.py) to single `TENSE_LABELS` constant
  - Improves maintainability and reduces code duplication
  - Easier to add, modify, or remove tenses in future

- **Updated verb form morphology paths:**
  - Fixed `conditional_simple` to use conjunctive path (subjunctive aorist forms) instead of indicative aorist
  - All prefix handling now consistently applied across present, future, subjunctive, and conditional tenses

### Technical Details

- **Total Tenses:** 10 (8 original: present, imperfect, past_continuous, aorist, future, future_continuous, subjunctive_simple, subjunctive_continuous + 2 new: conditional_simple, conditional_continuous)
- **Total Tests:** 72 (14 nouns + 30 adjectives [20 simple + 10 complex] + 28 verbs [20 original + 8 conditional])
- **Breaking Changes:** None — all changes are backward compatible

### Files Modified

- `modern_greek_eee/greek_utils.py` — Added TENSE_LABELS, updated VERB_TENSE_CONFIG, updated imports
- `tests/test_verbs.py` — Added 8 conditional tense tests
- `tests/test_adjectives.py` — Added 10 complex mode adjective tests
- `examples/greek_verbs.py` — Updated to use TENSE_LABELS from greek_utils
- `pyproject.toml` — Version bump 0.2.0 → 0.3.0

## Version 0.2.0

Initial release with support for:
- Verb conjugation (present, imperfect, aorist, future, future_continuous, subjunctive tenses)
- Noun declension (simple and complex modes)
- Adjective declension (simple mode)
- Multiple adjective types (καλός, τεμπέλης, ωραίος, βαθύς, συνεχής, κουρασμένος, μπλε)
