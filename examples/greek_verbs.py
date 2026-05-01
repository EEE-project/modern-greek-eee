# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo>=0.19.4",
#     "mcp==1.25.0",
#     "modern-greek-eee @ git+https://codeberg.org/EEE-project/modern-greek-eee.git",
#     "modern-greek-inflexion-eee @ git+https://codeberg.org/EEE-project/modern-greek-inflexion-eee.git",
#     "pandas==2.3.3",
# ]
#
# [tool.uv.sources]
# modern-greek-eee = { git = "https://codeberg.org/EEE-project/modern-greek-eee" }
# modern-greek-inflexion-eee = { git = "https://codeberg.org/EEE-project/modern-greek-inflexion-eee" }
# ///

import marimo

__generated_with = "0.23.1"
app = marimo.App(
    width="medium",
    css_file="/usr/local/_marimo/custom.css",
    html_head_file="head.html",
    auto_download=["html"],
)


@app.cell(hide_code=True)
def _(language_selector, mo, t_ui):
    _lang = language_selector.value
    mo.md(f"""
    # {t_ui("title", _lang)}

    [![Open in molab](https://molab.marimo.io/molab-shield.svg)](https://molab.marimo.io/notebooks/nb_HJPdFCQMSBvpw3EafKK88v)

    **{t_ui("description", _lang)}**

    {t_ui("select_hint", _lang)}

    {t_ui("use_csv", _lang)}
    """)
    return


@app.cell(hide_code=True)
def _(df, mo, tbl_sel):
    table = mo.ui.table(df, selection="multi", initial_selection=tbl_sel()) if df is not None else None
    table
    return (table,)


@app.cell(hide_code=True)
def _(language_selector, mo, t_ui):
    _lang = language_selector.value
    file_upload = mo.ui.file(label=t_ui("file_upload", _lang))
    file_upload
    return (file_upload,)


@app.cell(hide_code=True)
def _(gu, language_selector, mo, t_ui):
    _lang = language_selector.value
    # Build dropdown options from TENSE_LABELS
    _tense_options = {gu.TENSE_LABELS[k]['dropdown']: k for k in gu.TENSE_LABELS}
    tense_selector = mo.ui.dropdown(
        options=_tense_options,
        value=gu.TENSE_LABELS['aorist']['dropdown'],
        label=t_ui("select_tenses", _lang),
    )
    mo.md(f"""
    {t_ui("practice_heading", _lang)}

    {tense_selector}
    """)
    return (tense_selector,)


@app.cell(hide_code=True)
def _(
    captured_verb,
    clear_button,
    cv,
    gu,
    language_selector,
    mo,
    session_total,
    skip_button,
    submit_button,
    t_ui,
    tense_selector,
    verb_fields,
    words4test,
):
    # Tense Test View
    _lang = language_selector.value
    _tense_key = tense_selector.value
    _TENSE_LABELS = {k: gu.TENSE_LABELS[k]['greek'] for k in gu.TENSE_LABELS}

    if not words4test():
        _view = mo.md(t_ui("empty_list", _lang))
    elif not _tense_key:
        _view = mo.md(t_ui("select_at_least_one", _lang))
    else:
        _feedback = ""
        _c = captured_verb()
        if cv and _c and getattr(_c, 'verb_word', None) == cv['Word'] and getattr(_c, 'tense', None) == _tense_key:
            _, _msg = gu.check_verb_test(cv['Word'], _c, _tense_key)
            _feedback = mo.md(_msg)

        _label = _TENSE_LABELS.get(_tense_key, _tense_key)
        _view = mo.vstack([
            mo.md(t_ui("test_heading", _lang).format(label=_label, current=len(words4test()), total=session_total())),
            mo.md(f"{t_ui('translation_label', _lang)} **{cv['Translation']}**") if cv else mo.md(""),
            verb_fields,
            mo.hstack([skip_button, clear_button, submit_button], justify="end"),
            _feedback,
        ])

    _view
    return


@app.cell(hide_code=True)
def _(cv, gu, set_captured_verb, set_submit_count, submit_button, submit_count, tense_selector, verb_fields):
    # Submit handler: freeze current field values for checking
    if (submit_button.value or 0) > submit_count():
        set_submit_count(submit_button.value)
        if cv and verb_fields is not None:
            set_captured_verb(gu.make_snapshot(verb_fields, verb_word=cv['Word'], tense=tense_selector.value))
    return


@app.cell(hide_code=True)
def _(
    captured_verb,
    cv,
    df,
    gu,
    last_passed_mesg,
    mo,
    random,
    session_total,
    set_captured_verb,
    set_cv_state,
    set_last_passed_mesg,
    set_tbl_sel,
    set_words4test,
    tense_selector,
    words4test,
):
    # Check and Progression
    _tense_key = tense_selector.value
    _c = captured_verb()
    if cv and _tense_key and _c and getattr(_c, 'verb_word', None) == cv['Word'] and getattr(_c, 'tense', None) == _tense_key:
        _ok, _ = gu.check_verb_test(cv['Word'], _c, _tense_key)
        if _ok:
            _new_list = [w for w in words4test() if w["Word"] != cv["Word"]]
            set_words4test(_new_list)
            if df is not None:
                _rem = {w["Word"] for w in _new_list}
                set_tbl_sel([i for i, w in enumerate(df["Word"]) if w in _rem])
            set_last_passed_mesg(f'<span style="color: green;">Test for <b>"{cv["Word"]} -- {cv["Translation"]}"</b> passed.\n\n{len(_new_list)} words remaining out of {session_total()}.</span>')
            set_captured_verb(None)
            set_cv_state(random.choice(_new_list) if _new_list else None)

    res = mo.md(last_passed_mesg())
    res
    return


@app.cell(hide_code=True)
def _(cv, df, random, set_captured_verb, set_cv_state, set_skip_count, set_tbl_sel, set_words4test, skip_button, skip_count, words4test):
    # Skip handler: remove current verb from words4test
    if (skip_button.value or 0) > skip_count():
        set_skip_count(skip_button.value)
        set_captured_verb(None)
        _new_list = [w for w in words4test() if not cv or w["Word"] != cv["Word"]]
        set_words4test(_new_list)
        if df is not None:
            _rem = {w["Word"] for w in _new_list}
            set_tbl_sel([i for i, w in enumerate(df["Word"]) if w in _rem])
        set_cv_state(random.choice(_new_list) if _new_list else None)
    return


@app.cell(hide_code=True)
def _(clear_button, clear_count, set_captured_verb, set_clear_count):
    # Clear handler: reset fields and feedback
    if (clear_button.value or 0) > clear_count():
        set_clear_count(clear_button.value)
        set_captured_verb(None)
    return


@app.cell(hide_code=True)
def _(file_upload, gu):
    # Setup test data

    test_data = [
        {"Word": "γράφω", "Translation": "write"},
        {"Word": "διαβάζω", "Translation": "read"},
        {"Word": "μιλάω", "Translation": "speak"},
        {"Word": "πίνω", "Translation": "drink"},
        {"Word": "τρώω", "Translation": "eat"},
        {"Word": "πηγαίνω", "Translation": "go"}
    ]
    df = gu.load_data(file_upload, test_data)
    return (df,)


@app.cell(hide_code=True)
def _(gu, mo, random, session_total, set_session_total, table):
    # Initialize state variables

    words = gu.get_words(table)
    words4test, set_words4test = mo.state(words.copy() if words else [])
    if words and not session_total():
        set_session_total(len(words))
    elif not words:
        set_session_total(0)
    last_passed_mesg, set_last_passed_mesg = mo.state("")
    _clk = lambda v: (v or 0) + 1
    clear_button = mo.ui.button(label="Clear", on_click=_clk)
    skip_button = mo.ui.button(label="Skip", on_click=_clk)
    submit_count, set_submit_count = mo.state(0)
    clear_count, set_clear_count = mo.state(0)
    skip_count, set_skip_count = mo.state(0)
    captured_verb, set_captured_verb = mo.state(None)
    cv_state, set_cv_state = mo.state(None)
    if words and cv_state() is None:
        set_cv_state(random.choice(words))
    return (
        captured_verb,
        clear_button,
        clear_count,
        cv_state,
        last_passed_mesg,
        set_captured_verb,
        set_clear_count,
        set_cv_state,
        set_last_passed_mesg,
        set_skip_count,
        set_submit_count,
        set_words4test,
        skip_button,
        skip_count,
        submit_count,
        words,
        words4test,
    )


@app.cell(hide_code=True)
def _(clear_count, cv_state, gu, tense_selector, words, words4test):
    # Setup test fields — recreates on word change, tense change, or clear
    clear_count()
    cv = cv_state()
    _tense_key = tense_selector.value
    _TENSE_UI_LABELS = {k: f"{gu.TENSE_LABELS[k]['english']} ({gu.TENSE_LABELS[k]['greek']})" for k in gu.TENSE_LABELS}
    _ui_label = _TENSE_UI_LABELS.get(_tense_key, _tense_key) if _tense_key else "Select a tense"
    verb_fields, _ = gu.create_verb_test_ui(_ui_label, words, words4test(), cv)
    return cv, verb_fields


@app.cell(hide_code=True)
def _(captured_verb, mo, set_submit_count, verb_fields):
    # Submit button: yellow when fields have input that differs from last snapshot
    _values = verb_fields.value if verb_fields is not None else []
    _snap = captured_verb()
    _has_input = bool(_values and any(v.strip() for v in _values))
    _matches_snap = _snap is not None and [v.strip() for v in _values] == [v.strip() for v in (_snap.value or [])]
    _dirty = _has_input and not _matches_snap
    _clk = lambda v: (v or 0) + 1
    submit_button = mo.ui.button(label="Submit", on_click=_clk, kind="warn" if _dirty else "neutral")
    set_submit_count(0)
    return (submit_button,)


@app.cell(hide_code=True)
def _():
    UI_STRINGS = {
        "en": {
            "title": "Modern Greek — Verb Conjugation",
            "description": "Practice verb conjugation across multiple tenses.",
            "select_hint": "Select a tense to practice: Present, Imperfect, Aorist, Simple Future, Continuous Future, or Simple Subjunctive.",
            "use_csv": "Use the sample word set or upload a TAB-delimited CSV file with \"Word\" and \"Translation\" columns.",
            "file_upload": "Load TSV",
            "select_tenses": "Select tense:",
            "practice_heading": "## Practice: Verb Conjugation",
            "empty_list": "Word list is empty. Select words in the table above.",
            "translation_label": "Translation:",
            "test_heading": "### Test: {label} ({current}/{total})",
            "select_at_least_one": "Select a tense above.",
        },
        "ru": {
            "title": "Новогреческий — Спряжение глаголов",
            "description": "Попрактикуйте спряжение глаголов в различных временах.",
            "select_hint": "Выберите время для практики: Present, Imperfect, Aorist, Simple Future, Continuous Future или Simple Subjunctive.",
            "use_csv": "Используйте образец набора слов или загрузите CSV-файл с табуляцией в качестве разделителя со столбцами \"Word\" и \"Translation\".",
            "file_upload": "Загрузить TSV",
            "select_tenses": "Выберите время:",
            "practice_heading": "## Практика: Спряжение глаголов",
            "empty_list": "Список слов пуст. Выберите слова в таблице выше.",
            "translation_label": "Перевод:",
            "test_heading": "### Тест: {label} ({current}/{total})",
            "select_at_least_one": "Выберите время выше.",
        },
        "el": {
            "title": "Νέα Ελληνικά — Σύζευξη Ρημάτων",
            "description": "Εξασκηθείτε σε ρηματική σύζευξη σε διάφορους χρόνους.",
            "select_hint": "Επιλέξτε έναν χρόνο για εξάσκηση: Present, Imperfect, Aorist, Simple Future, Continuous Future ή Simple Subjunctive.",
            "use_csv": "Χρησιμοποιήστε το δείγμα συνόλου λέξεων ή φορτώστε ένα αρχείο CSV που οριοθετείται με TAB με στήλες \"Word\" και \"Translation\".",
            "file_upload": "Φόρτωση TSV",
            "select_tenses": "Επιλέξτε χρόνο:",
            "practice_heading": "## Εξάσκηση: Σύζευξη Ρημάτων",
            "empty_list": "Η λίστα λέξεων είναι κενή. Επιλέξτε λέξεις στον παραπάνω πίνακα.",
            "translation_label": "Μετάφραση:",
            "test_heading": "### Τεστ: {label} ({current}/{total})",
            "select_at_least_one": "Επιλέξτε έναν χρόνο παραπάνω.",
        },
    }

    def t_ui(key, lang=None):
        """Returns translated UI string for given language."""
        _lang = lang if lang else "en"
        return UI_STRINGS.get(_lang, UI_STRINGS["en"]).get(key, UI_STRINGS["en"].get(key, key))

    return (t_ui,)


@app.cell(hide_code=True)
def _(mo):
    language_selector = mo.ui.dropdown(
        options={"English": "en", "Русский": "ru", "Ελληνικά": "el"},
        value="English",
        label="🌐",
    )
    mo.Html(f"""
    <div style="position: fixed; top: 60px; right: 10px; z-index: 1000; background: white; padding: 8px 12px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.15);">
        {language_selector}
    </div>
    """)
    return (language_selector,)


@app.cell(hide_code=True)
def _(mo):
    tbl_sel, set_tbl_sel = mo.state(None)
    session_total, set_session_total = mo.state(0)
    return session_total, set_session_total, set_tbl_sel, tbl_sel


@app.cell(hide_code=True)
def _():
    # Package imports

    import random
    import marimo as mo

    from modern_greek_eee import greek_utils as gu
    return gu, mo, random


if __name__ == "__main__":
    app.run()
