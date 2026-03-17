# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo>=0.19.4",
#     "mcp==1.25.0",
#     "modern-greek-eee
#     "modern-greek-inflexion==2.0.7",
#     "pandas==2.3.3",
# ]
# ///

import marimo

__generated_with = "0.21.0"
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

    [![Open in molab](https://molab.marimo.io/molab-shield.svg)](https://molab.marimo.io/notebooks/nb_ADJECTIVES)

    **{t_ui("description", _lang)}**

    {t_ui("use_csv", _lang)}

    {t_ui("instructions", _lang)}
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
def _(adj_cv, adj_form, gu, language_selector, mo, t_ui, words, words4test):
    # Adjective Test View
    _lang = language_selector.value
    _adj = adj_cv()
    if words4test() and _adj:
        _, _msg = gu.check_adjective_test(_adj['Word'], adj_form)

        _view = mo.vstack([
            mo.md(f"**{t_ui('test_label', _lang)}** ({len(words4test())}/{len(words)})"),
            mo.md(f"{t_ui('translation_label', _lang)} **{_adj['Translation']}**"),
            adj_form,
            mo.md(_msg) if _msg else mo.md("")
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
            "instructions": "To complete the test, fill in all three gender forms (masculine, feminine, neuter) for each adjective.",
            "test_label": "Test: Adjective Declension",
            "translation_label": "Translation:",
            "empty_list": "The word list is empty.",
        },
        "ru": {
            "title": "Новогреческий — Склонение прилагательных",
            "description": "Попрактикуйте склонение прилагательных в различных формах рода и числа.",
            "use_csv": "Используйте образец набора слов или загрузите CSV-файл с табуляцией в качестве разделителя со столбцами \"Word\" и \"Translation\".",
            "file_upload": "Загрузить TSV",
            "instructions": "Чтобы завершить тест, заполните все три формы рода (мужской род, женский род, средний род) для каждого прилагательного.",
            "test_label": "Тест: Склонение прилагательных",
            "translation_label": "Перевод:",
            "empty_list": "Список слов пуст.",
        },
        "el": {
            "title": "Νέα Ελληνικά — Κλίση Επιθέτων",
            "description": "Εξασκηθείτε τη κλίση των επιθέτων σε διάφορες φόρμες φύλου και αριθμού.",
            "use_csv": "Χρησιμοποιήστε το δείγμα συνόλου λέξεων ή φορτώστε ένα αρχείο CSV που οριοθετείται με TAB με στήλες \"Word\" και \"Translation\".",
            "file_upload": "Φόρτωση TSV",
            "instructions": "Για να ολοκληρώσετε το τεστ, συμπληρώστε και τις τρεις φόρμες φύλου (αρσενικό, θηλυκό, ουδέτερο) για κάθε επίθετο.",
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
def _(adj_cv, gu):
    # Setup adjective test form
    _acv = adj_cv()
    adj_form, _ = gu.create_adjective_test_ui([] if not _acv else [_acv], [], _acv)
    return (adj_form,)


@app.cell(hide_code=True)
def _(
    adj_cv,
    adj_form,
    gu,
    set_adj_cv,
    set_adj_last_passed_mesg,
    set_words4test,
    words,
    words4test,
):
    # Adjective test progression
    _adj = adj_cv()
    if words4test() and _adj and adj_form:
        adj_ok, _ = gu.check_adjective_test(_adj['Word'], adj_form)
        gu.process_adjective_completion(_adj, adj_ok, words, words4test(), set_words4test, set_adj_last_passed_mesg, set_adj_cv)
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
def _(gu, mo, random, table):
    # Initialize state variables
    words = gu.get_words(table)
    words4test, set_words4test = mo.state(words.copy() if words else [])
    adj_last_passed_mesg, set_adj_last_passed_mesg = mo.state("")

    adj_cv, set_adj_cv = mo.state(None)

    # Sync current word state if words were selected/loaded
    if words:
        if adj_cv() is None:
            set_adj_cv(random.choice(words))
    return (
        adj_cv,
        adj_last_passed_mesg,
        set_adj_cv,
        set_adj_last_passed_mesg,
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
