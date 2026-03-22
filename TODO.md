# TODO - Future Improvements & Fixes

## High Priority

### Code Quality Issues

#### 1. Consolidate Tense Label Dictionaries (greek_verbs.py)
- **Issue**: Tense names duplicated 3 times in same file
  - Line 62-70: `tense_selector.options` dict keys
  - Line 86-93: `_TENSE_LABELS` dict
  - Line 184-191: `_TENSE_UI_LABELS` dict
- **Fix**: Extract to module-level constant or add to `UI_STRINGS`
- **Complexity**: Low
- **Files**: `examples/greek_verbs.py`

```python
# Current (duplicated)
tense_selector = mo.ui.dropdown(
    options={
        "Ενεστώτας (Present)": "present",
        "Παρατατικός (Imperfect)": "imperfect",
        ...
    }
)

# Could be
TENSES_CONFIG = {
    "present": {"gr": "Ενεστώτας", "ui": "Present (Ενεστώτας)"},
    "imperfect": {"gr": "Παρατατικός", "ui": "Imperfect (Παρατατικός)"},
    ...
}
```

#### 2. Reduce Redundant Adjective Form Validation (greek_adjectives.py)
- **Issue**: `check_adjective_test()` called twice per cycle:
  - Once in test view cell (line 82) for feedback display
  - Once in progression cell (line 197) for pass/fail boolean
- **Impact**: Morphological lookup (`get_word_by_type()` + `.all()`) runs 2x
- **Fix**: Cache result or pass feedback from first call to progression logic
- **Complexity**: Medium
- **Files**: `examples/greek_adjectives.py`, `modern_greek_eee/greek_utils.py`

---

## Medium Priority

### Structural Improvements

#### 3. Unify cv Pattern Across Notebooks
- **Issue**: Asymmetrical state management between verbs and adjectives
  - Verbs: `cv` derived locally from `words4test()[0]` (sequential order)
  - Adjectives: `adj_cv` separate state with random selection
- **Risk**: Future notebooks may miss randomization if following verb pattern
- **Fix**: Document the pattern difference, or create shared abstraction
- **Complexity**: Low
- **Files**: `examples/greek_verbs.py`, `examples/greek_adjectives.py`, README

#### 4. Extract Marimo Cell Patterns
- **Issue**: Cell dependency patterns are not documented
- **Fix**: Add comments explaining Marimo dependency cascade for maintainers
- **Complexity**: Low
- **Files**: `examples/*.py`

---

## Low Priority (Nice-to-Have)

#### 5. Performance: Conditional Form Creation
- **Issue**: All 6 verb forms created regardless of tense_selector.value
- **Optimization**: Only create forms for selected tenses
- **Impact**: 16-33% savings in form cell execution time
- **Complexity**: Medium
- **Files**: `examples/greek_verbs.py` line 195-228

#### 6. Article Lookup Optimization
- **Issue**: `['ο', 'η', 'το']` list check is O(n), could be O(1)
- **Fix**: Change to set `{'ο', 'η', 'το'}`
- **Impact**: Negligible (only 3 items), but good practice
- **Complexity**: Trivial
- **Files**: `modern_greek_eee/greek_utils.py` line 117

---

## Upstream Bugs - modern-greek-inflexion Library

These are bugs in the `modern-greek-inflexion` dependency. They affect Greek language accuracy but cannot be fixed in this repository without wrapping the library.

**File**: `UPSTREAM_BUGS.md` (see separate document)

**Summary**:
1. Neuter article forms backwards (nom/acc/gen swapped)
2. σχολάω verb missing variant forms (aorist)
3. Potential imperfect mood issues

**Action Items**:
- [ ] File bug reports with modern-greek-inflexion maintainers
- [ ] Document workarounds in this repository
- [ ] Add wrapper layer if library not fixed in 3 months

---

## Testing & Validation

#### 7. Add Integration Tests for Notebook Progression
- **Current**: Unit tests only (54 tests)
- **Need**: End-to-end notebook tests that simulate user interaction
- **Complexity**: Medium
- **Files**: `tests/test_notebook_integration.py` (new)

#### 8. Add Performance Benchmarks
- **Measure**: Form creation time, cell re-run time on word progression
- **Baseline**: ~100ms per form, <50ms cascade
- **Files**: `tests/test_performance.py` (new)

---

## Documentation

#### 9. Add Troubleshooting Guide for Notebook Development
- **Sections**:
  - Marimo cell dependencies and cascading
  - State management patterns (Derived vs Explicit)
  - Common UIElement errors and solutions
  - Library integration (greek_utils)
- **Files**: `docs/NOTEBOOK_DEVELOPMENT.md` (new)

#### 10. Document modern_greek_inflexion Workarounds
- **Sections**:
  - Known limitations and how notebooks work around them
  - Expected vs actual output examples
  - Validation strategies that account for library bugs
- **Files**: `UPSTREAM_BUGS.md` (see separate file)

---

## Completed Items ✓

- [x] Fix verb progression word advancement (confirmed working)
- [x] Fix UIElement truthiness warning in adjectives
- [x] Audit modern-greek-inflexion library issues (documented in LIBRARY_AUDIT.md)
- [x] All 54 unit tests passing
- [x] Live notebook testing completed
- [x] Push to adjectives branch

---

## Summary by Category

| Category | Count | Priority | Effort |
|----------|-------|----------|--------|
| Code Quality | 2 | High | Low-Med |
| Structure | 2 | Medium | Low |
| Performance | 2 | Low | Low-Med |
| Testing | 2 | Low | Medium |
| Documentation | 2 | Low | Low |
| **Upstream Bugs** | **3** | **High** | **Blocked** |

**Total Estimated Effort**: 20-30 hours (excluding upstream bugs)
**Recommended Next Step**: Start with #1 (tense labels) - quick win, improves maintainability
