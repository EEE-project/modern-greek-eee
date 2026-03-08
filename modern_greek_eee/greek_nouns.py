# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo>=0.19.4",
#     "mcp==1.25.0",
#     "modern-greek-eee @ git+https://github.com/EEE-project/modern-greek-eee.git",
#     "modern-greek-inflexion==2.0.7",
#     "pandas==2.3.3",
# ]
# ///

import marimo

__generated_with = "0.20.4"
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
def _(df, mo):
    table = mo.ui.table(df, selection="multi") if df is not None else None
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
    gu,
    language_selector,
    mo,
    noun,
    noun_form,
    noun_trans,
    t_ui,
    words,
    words4test,
):
    # View Simple Test
    _lang = language_selector.value
    _feedback = ""
    if words4test() and noun:
        with mo.capture_stdout() as _buffer:
            gu.check_noun_test(noun, noun_form, mode='simple')
            _feedback = _buffer.getvalue()

        _view = mo.vstack([
            mo.md(f"**{t_ui('simple_test', _lang)}** ({len(words4test())}/{len(words)})"),
            mo.md(f"{t_ui('translation_label', _lang)} **{noun_trans}**"),
            noun_form,
            mo.md(_feedback)
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
    gu,
    language_selector,
    mo,
    t_ui,
    words,
    words4test,
):
    # View Article Test
    _lang = language_selector.value
    _feedback = ""
    if words4test() and art_noun:
        with mo.capture_stdout() as _buffer:
            gu.check_noun_test(art_noun, art_noun_form, mode='article')
            _feedback = _buffer.getvalue()

        _view_art = mo.vstack([
            mo.md(f"**{t_ui('article_test', _lang)}** ({len(words4test())}/{len(words)})"),
            mo.md(f"{t_ui('translation_label', _lang)} **{art_noun_trans}**"),
            art_noun_form,
            mo.md(_feedback)
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
            "file_upload": "Load CSV",
            "simple_test": "Simple test for Nouns",
            "article_test": "Test for Nouns with Articles",
            "translation_label": "Translation:",
            "empty_list": "The word list is empty.",
        },
        "ru": {
            "title": "Новогреческий — Склонение существительных",
            "description": "Попрактикуйте склонение существительных в простом и артиклевом режимах.",
            "use_csv": "Используйте образец набора слов или загрузите TAB-разделенный CSV-файл со столбцами \"Word\" и \"Translation\".",
            "instructions": "Чтобы завершить тест, вы должны правильно заполнить все поля в **одной из форм теста** (простая или артиклевая режим).",
            "file_upload": "Загрузить CSV",
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
            "file_upload": "Φόρτωση CSV",
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
def _(current_noun, gu):
    # Setup simple test form (reactive to shared current word state)
    _cn = current_noun()
    noun, noun_trans, noun_form = gu.create_noun_test_ui([_cn] if _cn else [], mode='simple')
    return noun, noun_form, noun_trans


@app.cell(hide_code=True)
def _(current_noun, gu):
    # Setup article test form (reactive to shared current word state)
    _acn = current_noun()
    art_noun, art_noun_trans, art_noun_form = gu.create_noun_test_ui([_acn] if _acn else [], mode='article')
    return art_noun, art_noun_form, art_noun_trans


@app.cell(hide_code=True)
def _(
    gu,
    noun,
    noun_form,
    set_current_noun,
    set_last_passed_mesg,
    set_words4test,
    words,
    words4test,
):
    # Logic Simple progression
    if words4test() and noun:
        gu.process_noun_test(noun, noun_form, words, words4test, set_words4test, set_last_passed_mesg, set_current_noun, mode='simple')
    return


@app.cell(hide_code=True)
def _(
    art_noun,
    art_noun_form,
    gu,
    set_current_noun,
    set_last_passed_mesg,
    set_words4test,
    words,
    words4test,
):
    # Logic Article progression (syncs current_noun)
    if words4test() and art_noun:
        gu.process_noun_test(art_noun, art_noun_form, words, words4test, set_words4test, set_last_passed_mesg, set_current_noun, mode='article')
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
def _(gu, mo, random, table):
    # Initialize state variables
    words = gu.get_words(table)
    words4test, set_words4test = mo.state(words.copy() if words else [])
    last_passed_mesg, set_last_passed_mesg = mo.state("")

    current_noun, set_current_noun = mo.state(None)

    # Sync current word state if words were selected/loaded
    if words:
        if current_noun() is None:
            set_current_noun(random.choice(words))
    return (
        current_noun,
        last_passed_mesg,
        set_current_noun,
        set_last_passed_mesg,
        set_words4test,
        words,
        words4test,
    )


@app.cell(hide_code=True)
def _():
    import random
    import marimo as mo

    try:
        from modern_greek_eee import greek_utils as gu
    except ImportError:
        import greek_utils as gu

    return gu, mo, random


if __name__ == "__main__":
    app.run()
