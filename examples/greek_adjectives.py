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

    [![Open in molab](https://molab.marimo.io/molab-shield.svg)](https://molab.marimo.io/notebooks/nb_C7b5s58CeEseJvBWTbw8Px)

    **{t_ui("description", _lang)}**

    {t_ui("use_csv", _lang)}

    {t_ui("instructions", _lang)}
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
def _(language_selector, mo, t_ui):
    _lang = language_selector.value
    _simple_label = t_ui("simple_mode", _lang)
    mode_selector = mo.ui.radio(
        options={
            _simple_label: "simple",
            t_ui("complex_mode", _lang): "complex"
        },
        value=_simple_label,
        label=t_ui("select_mode", _lang)
    )
    mo.md(f"""
    {mode_selector}
    """)
    return (mode_selector,)


@app.cell(hide_code=True)
def _(adj_cv, adj_form, captured_adj, clear_button, gu, language_selector, mo, mode_selector, session_total, skip_button, submit_button, t_ui, words4test):
    # Adjective Test View
    _lang = language_selector.value
    _mode = mode_selector.value
    _adj = adj_cv()
    if words4test() and _adj:
        _c = captured_adj()
        _feedback = mo.md("")
        if _c and getattr(_c, 'adj_word', None) == _adj['Word']:
            _, _msg = gu.check_adjective_test(_adj['Word'], _c, mode=_mode)
            if _msg:
                _feedback = mo.md(_msg)

        _view = mo.vstack([
            mo.md(f"**{t_ui('test_label', _lang)}** ({len(words4test())}/{session_total()})"),
            mo.md(f"{t_ui('translation_label', _lang)} **{_adj['Translation']}**"),
            adj_form,
            _feedback,
            mo.hstack([skip_button, clear_button, submit_button], justify="end"),
        ])
    else:
        _view = mo.md(f"**{t_ui('empty_list', _lang)}**")

    _view
    return


@app.cell(hide_code=True)
def _(adj_last_passed_mesg, mo):
    # Progression message display
    _res = mo.md(adj_last_passed_mesg())
    _res
    return


@app.cell(hide_code=True)
def _():
    UI_STRINGS = {
        "en": {
            "title": "Modern Greek — Adjective Declension",
            "description": "Practice adjective declension across different gender and number forms.",
            "use_csv": "Use the sample word set or upload a TAB-delimited CSV file with \"Word\" and \"Translation\" columns.",
            "file_upload": "Load TSV",
            "select_mode": "Test Mode:",
            "simple_mode": "Simple: 3 genders × 2 numbers (6 fields)",
            "complex_mode": "Complex: All genders, numbers, and cases (18 fields)",
            "instructions": "Select a mode and fill in all required forms for each adjective.",
            "test_label": "Test: Adjective Declension",
            "translation_label": "Translation:",
            "empty_list": "The word list is empty.",
        },
        "ru": {
            "title": "Новогреческий — Склонение прилагательных",
            "description": "Попрактикуйте склонение прилагательных в различных формах рода и числа.",
            "use_csv": "Используйте образец набора слов или загрузите CSV-файл с табуляцией в качестве разделителя со столбцами \"Word\" и \"Translation\".",
            "file_upload": "Загрузить TSV",
            "select_mode": "Режим теста:",
            "simple_mode": "Простой: 3 рода × 2 числа (6 полей)",
            "complex_mode": "Сложный: все роды, числа и падежи (18 полей)",
            "instructions": "Выберите режим и заполните все необходимые формы для каждого прилагательного.",
            "test_label": "Тест: Склонение прилагательных",
            "translation_label": "Перевод:",
            "empty_list": "Список слов пуст.",
        },
        "el": {
            "title": "Νέα Ελληνικά — Κλίση Επιθέτων",
            "description": "Εξασκηθείτε τη κλίση των επιθέτων σε διάφορες φόρμες φύλου και αριθμού.",
            "use_csv": "Χρησιμοποιήστε το δείγμα συνόλου λέξεων ή φορτώστε ένα αρχείο CSV που οριοθετείται με TAB με στήλες \"Word\" και \"Translation\".",
            "file_upload": "Φόρτωση TSV",
            "select_mode": "Λειτουργία δοκιμής:",
            "simple_mode": "Απλή: 3 φύλα × 2 αριθμοί (6 πεδία)",
            "complex_mode": "Σύνθετη: όλα τα φύλα, αριθμοί και πτώσεις (18 πεδία)",
            "instructions": "Επιλέξτε λειτουργία και συμπληρώστε όλες τις απαιτούμενες φόρμες για κάθε επίθετο.",
            "test_label": "Τεστ: Κλίση Επιθέτων",
            "translation_label": "Μετάφραση:",
            "empty_list": "Η λίστα λέξεων είναι κενή.",
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
def _(adj_cv, clear_count, gu, mode_selector):
    # Setup adjective test form with selected mode
    clear_count()
    _acv = adj_cv()
    _mode = mode_selector.value
    adj_form, _ = gu.create_adjective_test_ui([] if not _acv else [_acv], [], _acv, mode=_mode)
    return (adj_form,)


@app.cell(hide_code=True)
def _(adj_form, captured_adj, mo, set_submit_count):
    # Submit button: yellow when fields have input that differs from last snapshot
    _values = adj_form.value if adj_form else []
    _snap = captured_adj()
    _has_input = bool(_values and any(v.strip() for v in _values))
    _matches_snap = _snap is not None and [v.strip() for v in _values] == [v.strip() for v in (_snap.value or [])]
    _dirty = _has_input and not _matches_snap
    _clk = lambda v: (v or 0) + 1
    submit_button = mo.ui.button(label="Submit", on_click=_clk, kind="warn" if _dirty else "neutral")
    set_submit_count(0)
    return (submit_button,)


@app.cell(hide_code=True)
def _(
    adj_cv,
    captured_adj,
    df,
    gu,
    random,
    session_total,
    set_adj_cv,
    set_adj_last_passed_mesg,
    set_captured_adj,
    set_tbl_sel,
    set_words4test,
    words4test,
):
    # Adjective test progression
    _adj = adj_cv()
    _c = captured_adj()
    if words4test() and _adj and _c and getattr(_c, 'adj_word', None) == _adj['Word']:
        adj_ok, _ = gu.check_adjective_test(_adj['Word'], _c)
        if adj_ok:
            _new_list = [w for w in words4test() if w["Word"] != _adj["Word"]]
            set_words4test(_new_list)
            if df is not None:
                _rem = {w["Word"] for w in _new_list}
                set_tbl_sel([i for i, w in enumerate(df["Word"]) if w in _rem])
            set_adj_last_passed_mesg(f'<span style="color: green;">Test for <b>"{_adj["Word"]} -- {_adj["Translation"]}"</b> passed.\n\n{len(_new_list)} words remaining out of {session_total()}.</span>')
            set_adj_cv(random.choice(_new_list) if _new_list else None)
            set_captured_adj(None)
    return


@app.cell(hide_code=True)
def _(adj_cv, adj_form, gu, set_captured_adj, set_submit_count, submit_button, submit_count):
    # Submit handler: freeze current field values for checking
    if (submit_button.value or 0) > submit_count():
        set_submit_count(submit_button.value)
        _acv = adj_cv()
        if _acv and adj_form:
            set_captured_adj(gu.make_snapshot(adj_form))
    return


@app.cell(hide_code=True)
def _(adj_cv, df, random, set_adj_cv, set_captured_adj, set_skip_count, set_tbl_sel, set_words4test, skip_button, skip_count, words4test):
    # Skip handler: remove current adjective from words4test
    if (skip_button.value or 0) > skip_count():
        set_skip_count(skip_button.value)
        set_captured_adj(None)
        _acv = adj_cv()
        _new_list = [w for w in words4test() if not _acv or w["Word"] != _acv["Word"]]
        set_words4test(_new_list)
        if df is not None:
            _rem = {w["Word"] for w in _new_list}
            set_tbl_sel([i for i, w in enumerate(df["Word"]) if w in _rem])
        set_adj_cv(random.choice(_new_list) if _new_list else None)
    return


@app.cell(hide_code=True)
def _(clear_button, clear_count, set_captured_adj, set_clear_count):
    # Clear handler: reset fields and feedback
    if (clear_button.value or 0) > clear_count():
        set_clear_count(clear_button.value)
        set_captured_adj(None)
    return


@app.cell(hide_code=True)
def _(file_upload, gu):
    # Setup test data - 7 adjectives with different declension patterns
    test_data = [
        {"Word": "καλός", "Translation": "good"},
        {"Word": "τεμπέλης", "Translation": "lazy"},
        {"Word": "ωραίος", "Translation": "beautiful"},
        {"Word": "βαθύς", "Translation": "deep"},
        {"Word": "συνεχής", "Translation": "continuous"},
        {"Word": "κουρασμένος", "Translation": "tired"},
        {"Word": "μπλε", "Translation": "blue"},
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
    adj_last_passed_mesg, set_adj_last_passed_mesg = mo.state("")

    adj_cv, set_adj_cv = mo.state(None)
    captured_adj, set_captured_adj = mo.state(None)
    _clk = lambda v: (v or 0) + 1
    skip_button = mo.ui.button(label="Skip", on_click=_clk)
    clear_button = mo.ui.button(label="Clear", on_click=_clk)
    skip_count, set_skip_count = mo.state(0)
    clear_count, set_clear_count = mo.state(0)
    submit_count, set_submit_count = mo.state(0)

    # Sync current word state if words were selected/loaded
    if words:
        if adj_cv() is None:
            set_adj_cv(random.choice(words))
    return (
        adj_cv,
        adj_last_passed_mesg,
        captured_adj,
        clear_button,
        clear_count,
        set_adj_cv,
        set_adj_last_passed_mesg,
        set_captured_adj,
        set_clear_count,
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
def _(mo):
    tbl_sel, set_tbl_sel = mo.state(None)
    session_total, set_session_total = mo.state(0)
    return session_total, set_session_total, set_tbl_sel, tbl_sel


@app.cell(hide_code=True)
def _():
    import random
    import marimo as mo

    from modern_greek_eee import greek_utils as gu
    return gu, mo, random


if __name__ == "__main__":
    app.run()
