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

    [![Open in molab](https://molab.marimo.io/molab-shield.svg)](https://molab.marimo.io/notebooks/nb_KZYjBCXm1jiSjMBnvxWezi)

    **{t_ui("description", _lang)}**

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
def _(language_selector, mo, t_ui):
    _lang = language_selector.value
    mo.md(f"""
    {t_ui("instructions", _lang)}
    """)
    return


@app.cell(hide_code=True)
def _(
    captured_simple,
    clear_button,
    gu,
    language_selector,
    mo,
    noun,
    noun_form,
    noun_trans,
    session_total,
    skip_button,
    submit_button,
    t_ui,
    words4test,
):
    # View Simple Test
    _lang = language_selector.value
    _feedback = mo.md("")
    if words4test() and noun:
        _cs = captured_simple()
        if _cs and getattr(_cs, 'test_word', None) == noun:
            with mo.capture_stdout() as _buf:
                gu.check_noun_test(noun, _cs, mode='simple')
            if _buf.getvalue():
                _feedback = mo.md(_buf.getvalue())

        _view = mo.vstack([
            mo.md(f"**{t_ui('simple_test', _lang)}** ({len(words4test())}/{session_total()})"),
            mo.md(f"{t_ui('translation_label', _lang)} **{noun_trans}**"),
            noun_form,
            _feedback,
            mo.hstack([skip_button, clear_button, submit_button], justify="end"),
        ])
    else:
        _view = mo.md(f"**{t_ui('empty_list', _lang)}**")

    _view
    return


@app.cell(hide_code=True)
def _(
    art_noun,
    art_noun_form,
    art_noun_trans,
    captured_article,
    clear_button,
    gu,
    language_selector,
    mo,
    session_total,
    skip_button,
    submit_button,
    t_ui,
    words4test,
):
    # View Article Test
    _lang = language_selector.value
    _feedback = mo.md("")
    if words4test() and art_noun:
        _ca = captured_article()
        if _ca and getattr(_ca, 'test_word', None) == art_noun:
            with mo.capture_stdout() as _buf:
                gu.check_noun_test(art_noun, _ca, mode='article')
            if _buf.getvalue():
                _feedback = mo.md(_buf.getvalue())

        _view_art = mo.vstack([
            mo.md(f"**{t_ui('article_test', _lang)}** ({len(words4test())}/{session_total()})"),
            mo.md(f"{t_ui('translation_label', _lang)} **{art_noun_trans}**"),
            art_noun_form,
            _feedback,
            mo.hstack([skip_button, clear_button, submit_button], justify="end"),
        ])
    else:
        _view_art = mo.md(f"**{t_ui('empty_list', _lang)}**")

    _view_art
    return


@app.cell(hide_code=True)
def _(last_passed_mesg, mo):
    # Progression message display
    _res = mo.md(last_passed_mesg())
    _res
    return


@app.cell(hide_code=True)
def _():
    UI_STRINGS = {
        "en": {
            "title": "Modern Greek — Noun Declension",
            "description": "Practice noun declensions in simple and article modes.",
            "use_csv": "Use the sample word set or upload a TAB-delimited CSV file with \"Word\" and \"Translation\" columns.",
            "instructions": "To complete the test, you must correctly fill in all fields in **one of the test forms** (simple or article mode).",
            "file_upload": "Load TSV",
            "simple_test": "Simple test for Nouns",
            "article_test": "Test for Nouns with Articles",
            "translation_label": "Translation:",
            "empty_list": "The word list is empty.",
        },
        "ru": {
            "title": "Новогреческий — Склонение существительных",
            "description": "Попрактикуйте склонение существительных в простом и артиклевом режимах.",
            "use_csv": "Используйте образец набора слов или загрузите CSV-файл с табуляцией в качестве разделителя со столбцами \"Word\" и \"Translation\".",
            "instructions": "Чтобы завершить тест, вы должны правильно заполнить все поля в **одной из форм теста** (простой или артиклевый режим).",
            "file_upload": "Загрузить TSV",
            "simple_test": "Простой тест для существительных",
            "article_test": "Тест для существительных с артиклями",
            "translation_label": "Перевод:",
            "empty_list": "Список слов пуст.",
        },
        "el": {
            "title": "Νέα Ελληνικά — Κλίση Ουσιαστικών",
            "description": "Εξασκήστε την κλίση ουσιαστικών σε απλή και μορφή άρθρου.",
            "use_csv": "Χρησιμοποιήστε το δείγμα συνόλου λέξεων ή φορτώστε ένα αρχείο CSV που οριοθετείται με TAB με στήλες \"Word\" και \"Translation\".",
            "instructions": "Για να ολοκληρώσετε το τεστ, πρέπει να συμπληρώσετε σωστά όλα τα πεδία σε **μία από τις φόρμες δοκιμής** (απλή ή μορφή άρθρου).",
            "file_upload": "Φόρτωση TSV",
            "simple_test": "Απλό τεστ για ουσιαστικά",
            "article_test": "Τεστ για ουσιαστικά με άρθρα",
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
def _(clear_count, current_noun, gu):
    # Setup simple test form (reactive to shared current word state)
    clear_count()
    _cn = current_noun()
    noun, noun_trans, noun_form = gu.create_noun_test_ui([_cn] if _cn else [], mode='simple')
    return noun, noun_form, noun_trans


@app.cell(hide_code=True)
def _(clear_count, current_noun, gu):
    # Setup article test form (reactive to shared current word state)
    clear_count()
    _acn = current_noun()
    art_noun, art_noun_trans, art_noun_form = gu.create_noun_test_ui([_acn] if _acn else [], mode='article')
    return art_noun, art_noun_form, art_noun_trans


@app.cell(hide_code=True)
def _(art_noun_form, captured_article, captured_simple, mo, noun_form, set_submit_count):
    # Submit button: yellow when either form has input that differs from its snapshot
    _vals_s = noun_form.value if noun_form else []
    _vals_a = art_noun_form.value if art_noun_form else []
    _snap_s = captured_simple()
    _snap_a = captured_article()
    _has_s = bool(_vals_s and any(v.strip() for v in _vals_s))
    _has_a = bool(_vals_a and any(v.strip() for v in _vals_a))
    _match_s = _snap_s is not None and [v.strip() for v in _vals_s] == [v.strip() for v in (_snap_s.value or [])]
    _match_a = _snap_a is not None and [v.strip() for v in _vals_a] == [v.strip() for v in (_snap_a.value or [])]
    _dirty = (_has_s and not _match_s) or (_has_a and not _match_a)
    _clk = lambda v: (v or 0) + 1
    submit_button = mo.ui.button(label="Submit", on_click=_clk, kind="warn" if _dirty else "neutral")
    set_submit_count(0)
    return (submit_button,)


@app.cell(hide_code=True)
def _(
    captured_article,
    captured_simple,
    current_noun,
    df,
    gu,
    random,
    session_total,
    set_captured_article,
    set_captured_simple,
    set_current_noun,
    set_last_passed_mesg,
    set_tbl_sel,
    set_words4test,
    words4test,
):
    # Progression: check either snapshot; word passes if either mode is complete
    _cn = current_noun()
    _cs = captured_simple()
    _ca = captured_article()
    if words4test() and _cn and (_cs or _ca):
        _passed = False
        if _cs and getattr(_cs, 'test_word', None) == _cn['Word']:
            _passed = gu.check_noun_test(_cn['Word'], _cs, mode='simple')
        if not _passed and _ca and getattr(_ca, 'test_word', None) == _cn['Word']:
            _passed = gu.check_noun_test(_cn['Word'], _ca, mode='article')
        if _passed:
            _new_list = [w for w in words4test() if w["Word"] != _cn["Word"]]
            set_words4test(_new_list)
            if df is not None:
                _rem = {w["Word"] for w in _new_list}
                set_tbl_sel([i for i, w in enumerate(df["Word"]) if w in _rem])
            set_last_passed_mesg(f'<span style="color: green;">Test for <b>"{_cn["Word"]}"</b> passed.\n\n{len(_new_list)} words remaining out of {session_total()}.</span>')
            set_captured_simple(None)
            set_captured_article(None)
            set_current_noun(random.choice(_new_list) if _new_list else None)
    return


@app.cell(hide_code=True)
def _(art_noun, art_noun_form, gu, noun, noun_form, set_captured_article, set_captured_simple, set_submit_count, submit_button, submit_count):
    # Submit handler: freeze both forms for checking
    if (submit_button.value or 0) > submit_count():
        set_submit_count(submit_button.value)
        if noun and noun_form:
            set_captured_simple(gu.make_snapshot(noun_form))
        if art_noun and art_noun_form:
            set_captured_article(gu.make_snapshot(art_noun_form))
    return


@app.cell(hide_code=True)
def _(clear_button, clear_count, set_captured_article, set_captured_simple, set_clear_count):
    # Clear handler: reset fields and feedback
    if (clear_button.value or 0) > clear_count():
        set_clear_count(clear_button.value)
        set_captured_simple(None)
        set_captured_article(None)
    return


@app.cell(hide_code=True)
def _(current_noun, df, random, set_captured_article, set_captured_simple, set_current_noun, set_skip_count, set_tbl_sel, set_words4test, skip_button, skip_count, words4test):
    # Skip handler: remove current word from words4test
    if (skip_button.value or 0) > skip_count():
        set_skip_count(skip_button.value)
        set_captured_simple(None)
        set_captured_article(None)
        _cn = current_noun()
        _new_list = [w for w in words4test() if not _cn or w["Word"] != _cn["Word"]]
        set_words4test(_new_list)
        if df is not None:
            _rem = {w["Word"] for w in _new_list}
            set_tbl_sel([i for i, w in enumerate(df["Word"]) if w in _rem])
        set_current_noun(random.choice(_new_list) if _new_list else None)
    return


@app.cell(hide_code=True)
def _(file_upload, gu):
    # Setup test data

    test_data = [
        {"Word": "το ωράριο", "Translation": "schedule, working hours"},
        {"Word": "η ώρα", "Translation": "hour"},
        {"Word": "ο χώρος", "Translation": "space, room"},
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

    current_noun, set_current_noun = mo.state(None)
    captured_simple, set_captured_simple = mo.state(None)
    captured_article, set_captured_article = mo.state(None)
    _clk = lambda v: (v or 0) + 1
    skip_button = mo.ui.button(label="Skip", on_click=_clk)
    clear_button = mo.ui.button(label="Clear", on_click=_clk)
    skip_count, set_skip_count = mo.state(0)
    clear_count, set_clear_count = mo.state(0)
    submit_count, set_submit_count = mo.state(0)

    # Sync current word state if words were selected/loaded
    if words:
        if current_noun() is None:
            set_current_noun(random.choice(words))
    return (
        captured_article,
        captured_simple,
        clear_button,
        clear_count,
        current_noun,
        last_passed_mesg,
        set_captured_article,
        set_captured_simple,
        set_clear_count,
        set_current_noun,
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
