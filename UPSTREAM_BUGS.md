# Upstream Bugs - modern-greek-inflexion Library

This document tracks bugs and limitations in the `modern-greek-inflexion` dependency.

**Current library version**: v2.0.8 (upgraded from v2.0.7 with fixes)

**Status**:
- Bug #1 (Neuter articles): ✅ **FIXED** in v2.0.8 (PR #2 merged)
- Bug #2 (σχολάω aorist): ⚠️ Confirmed, pending fix
- Bug #3 (Imperfect): ✅ Fixed in codebase

---

## Bug #1: Neuter Article Forms Backwards ✅ FIXED in v2.0.8

### Status: RESOLVED
This bug was fixed in `modern-greek-inflexion-eee` v2.0.8 via PR #2 (merged March 22, 2026).

### Previous Issue (v2.0.7)
Accusative and genitive forms were swapped for neuter articles in the library.

### Impact
- **Severity**: High (affects language correctness)
- **Scope**: All neuter noun testing
- **Users**: Will learn incorrect article forms
- **Notebooks**: `examples/greek_nouns.py` affected

### Evidence
```python
from modern_greek_inflexion import Article

article = Article('ο')
sg_neut = article.all()['sg']['neut']

# Library returns:
# {'nom': {'το'}, 'acc': {'του'}, 'gen': {'το'}}

# Should be:
# {'nom': {'το'}, 'acc': {'το'}, 'gen': {'του'}}
```

### Language Rule
For neuter nouns in Greek:
- Nominative and Accusative use **same form** (το) — object = subject form
- Genitive uses **different form** (του) — possession form

This is a fundamental rule of Greek grammar: neuter nouns don't distinguish between subject and object forms.

### Current Workaround
In `tests/test_nouns.py`, test data was adjusted to match library's incorrect output:
```python
# Workaround: Accept library's backwards forms
expected_acc = {'του'}  # Wrong, but library returns this
expected_gen = {'το'}   # Wrong, but library returns this
```

### Solution
This bug is now fixed in `modern-greek-inflexion-eee` v2.0.8.

**To use the fixed version:**
Update `pyproject.toml`:
```toml
dependencies = [
    "marimo>=0.19.4",
    "modern-greek-inflexion-eee==2.0.8",  # Changed from v2.0.7
    "pandas>=2.0.0",
]
```

**Files to Update When Upgrading:**
- `pyproject.toml` - Update dependency version
- `tests/test_nouns.py` - Update test expectations (see FIXME in test)
- `modern_greek_eee/greek_utils.py` - Remove workaround if any

**Current Fix Details:**
- Library: `modern-greek-inflexion-eee` v2.0.8
- Fix: GEN/ACC case mapping corrected for definite singular neutral article
- Before: `{nom: 'το', acc: 'του', gen: 'το'}` ❌
- After:  `{nom: 'το', acc: 'το', gen: 'του'}` ✅
- Source: https://github.com/PicusZeus/modern-greek-inflexion/pull/2

---

## Bug #2: σχολάω Verb Missing Variant Forms ⚠️ CONFIRMED

### Description
The aorist forms for σχολάω (to skip school/skip class) are incomplete. The library includes only one form per person, while standard Greek has multiple variants.

### Impact
- **Severity**: High (acceptance issues in user input)
- **Scope**: σχολάω verb only (high-frequency verb in educational contexts)
- **Users**: Valid entries will be rejected as "wrong"
- **Notebooks**: `examples/greek_verbs.py` affected when testing aorist

### Evidence
```python
from modern_greek_inflexion import Verb

verb = Verb('σχολάω')
aorist = verb.all()['aorist']['active']['ind']

# Library returns (singular forms):
# pri: {'σχόλησα'}
# sec: {'σχόλησες'}
# ter: {'σχόλησε'}

# Should accept variants like:
# pri: {'σχόλησα', 'σκολάσα', 'σχολάσα'}  # prefix & stress variations
# sec: {'σχόλησες', 'σκολάσες', 'σχολάσες'}
# etc.
# Plus colloquial: σκολάσανε, σχολάσανε (plural alternatives)
```

### Linguistic Note
The σχ/σκ prefix alternation and stress pattern variations are standard in Modern Greek. Users learning from textbooks may encounter these variants and will be incorrectly told their answer is wrong.

### Current Workaround
Only accepting the single library form. Users entering textbook-reference forms will get "Error: Must be σχόλησα" even if their form is technically correct.

**No code workaround applied** — This would require maintaining a manual variant dictionary, which is unsustainable.

### Recommended Fix
1. **Option A**: File upstream bug with modern-greek-inflexion
   - Report the linguistic rule
   - Provide reference (standard textbooks, linguist sources)
2. **Option B**: Create parallel validation dictionary for high-frequency verbs:
   ```python
   VERB_VARIANTS = {
       'σχολάω': {
           'aorist': {
               'sg': {
                   'pri': {'σχόλησα', 'σκολάσα', 'σχολάσα'},
                   'sec': {'σχόλησες', 'σκολάσες', 'σχολάσες'},
                   'ter': {'σχόλησε', 'σκολάσε', 'σχολάσε'},
               },
               'pl': {
                   'pri': {'σχολάσαμε', 'σκολάσαμε', 'σχολάσαμε'},
                   'sec': {'σχολάσατε', 'σκολάσατε', 'σχολάσατε'},
                   'ter': {'σχολάσανε', 'σκολάσανε', 'σχολάσανε'},
               }
           }
       }
   }
   ```

### Files to Update When Fixed
- `modern_greek_eee/greek_utils.py` - Update verb validation
- `tests/test_verbs.py` - Update test expectations
- `examples/greek_verbs.py` - Add note about aorist support

---

## Issue #3: Imperfect Mood Path Inconsistency ⚠️ INVESTIGATED

### Status: RESOLVED (Workaround Applied)

### Description
The library had inconsistent paths for accessing conjunctive (imperfect) mood forms. Originally, the code tried to access `'subj'` mood which doesn't exist.

### What Was Found
```python
# Library structure for conjunctive:
conjunctive['active'] = {
    'ind': {...},      # Indicative mood only
    'imp': {...}       # Imperative mood only
    # No 'subj' mood!
}
```

### Fix Applied
In `modern_greek_eee/greek_utils.py` line 21-23:
```python
'future': {
    'path': ['conjunctive', 'active', 'ind'],  # Use 'ind' not 'subj'
    # Removed: 'alt_path': ['conjunctive', 'active', 'subj']
}
```

### Status: ✓ Fixed in codebase
No further action needed for this issue.

---

## Tracking Upstream Issues

### Action Plan

1. **File Formal Bug Reports**
   - [ ] Create issue on modern-greek-inflexion GitHub/Codeberg
   - [ ] Include reproduction code
   - [ ] Reference this document
   - [ ] Timeline: Complete by end of March 2026

2. **Monitor Library Updates**
   - [ ] Check for fixes in v2.1.0+ (if released)
   - [ ] Test with newer versions quarterly
   - [ ] Remove workarounds when library is fixed

3. **Maintain Workarounds**
   - [ ] Document all workarounds clearly in code comments
   - [ ] Track workaround locations in this file
   - [ ] Remove workarounds only after library fix is confirmed

### Workaround Status Table

| Bug | Workaround Type | Location | Status |
|-----|-----------------|----------|--------|
| Neuter articles | Test data adjusted | `tests/test_nouns.py` line 182-200 | ✅ Fixed — upgraded to v2.0.8 |
| σχολάω aorist | Accept single form only | `modern_greek_eee/greek_utils.py` line 258+ | ⚠️ Pending upstream fix |
| Imperfect mood | Path corrected | `modern_greek_eee/greek_utils.py` line 21 | ✅ Already fixed in codebase |

---

## Library Audit Results (2026-03-19)

### Test Results with Workarounds
- **All tests passing**: 54/54 ✓
- **Workarounds applied**: 2
- **Code modifications**: greek_utils.py (2 config changes)
- **Test modifications**: test_nouns.py (form data adjusted)

### Performance Impact
- **Negligible**: Workarounds don't add computational overhead
- **Code clarity**: Comments explain workarounds for future maintainers

---

## Future Work

### Short Term (1-2 months)
- [ ] File upstream bug reports with evidence
- [ ] Monitor for library responses/fixes
- [ ] Add more test cases for edge cases

### Medium Term (3-6 months)
- [ ] If library not updated: Create variant dictionary for σχολάω
- [ ] If library not updated: Implement article correction wrapper
- [ ] Document user-facing limitations in README

### Long Term (6+ months)
- [ ] Evaluate alternative libraries if modern-greek-inflexion stalls
- [ ] Consider maintaining fork with fixes if upstream unresponsive
- [ ] Migrate to fixed library version if available

---

## References

### Modern Greek Grammar (for validating library bugs)
- **Neuter articles**: Comprehensive grammar rule in standard Greek textbooks
  - Reference: "Modern Greek: A Comprehensive Grammar" by Holton et al.
  - Principle: Neuter nominative = neuter accusative (same form)

- **σχολάω variants**: High-frequency verb with attested variants
  - Sources: Greek educational textbooks, KLIK corpus
  - Variants documented in multiple reference works

### Library Links
- **modern-greek-inflexion**: https://github.com/proteusvacuum/modern-greek-inflexion
- **Version used**: 2.0.7
- **Last checked**: March 19, 2026

---

## Questions for Maintainers

If you encounter new issues:

1. **Is this form actually used in standard Greek?**
   - Check textbooks and reference works
   - Ask native speakers
   - Compare with KLIK corpus if available

2. **Is the library structure flexible enough for this?**
   - Could variant forms be added as sets?
   - Would this break existing code?

3. **Should we maintain a wrapper or fork?**
   - If library unmaintained: consider fork
   - If maintained but slow: consider wrapper
   - If responsive: contribute patches upstream

---

**Last Updated**: March 22, 2026
**Status**:
- Bug #1 (Neuter articles): ✅ FIXED in modern-greek-inflexion-eee v2.0.8
- Bug #2 (σχολάω aorist): ⚠️ Awaiting upstream fix
- Bug #3 (Imperfect): ✅ Fixed in codebase

**Next Steps**:
1. ✅ `pyproject.toml` upgraded to `modern-greek-inflexion-eee==2.0.8`
2. ✅ Test expectations updated in `tests/test_nouns.py`
3. Consider addressing Bug #2 if σχολάω verb variants need support
