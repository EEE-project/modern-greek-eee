# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo>=0.19.4",
#     "mcp==1.25.0",
#     "modern-greek-eee @ git+https://github.com/EEE-project/modern-greek-eee.git",
#     "modern-greek-inflexion-eee @ git+https://github.com/EEE-project/modern-greek-inflexion-eee.git",
#     "pandas==2.3.3",
# ]
#
# [tool.uv.sources]
# modern-greek-eee = { git = "https://github.com/EEE-project/modern-greek-eee" }
# modern-greek-inflexion-eee = { git = "https://github.com/EEE-project/modern-greek-inflexion-eee" }
# ///

import marimo

__generated_with = "0.19.7"
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
    tense_selector = mo.ui.dropdown(
        options={
            "Ενεστώτας (Present)": "present",
            "Παρατατικός (Imperfect)": "imperfect",
            "Αόριστος (Aorist)": "aorist",
            "Απλός Μέλλοντας (Simple Future)": "future",
            "Συνεχής Μέλλοντας (Continuous Future)": "future_continuous",
            "Απλή Υποτακτική (Simple Subjunctive)": "subjunctive_simple",
        },
        value="Αόριστος (Aorist)",
        label=t_ui("select_tenses", _lang),
    )
    mo.md(f"""
    {t_ui("practice_heading", _lang)}

    {tense_selector}
    """)
    return (tense_selector,)


@app.cell(hide_code=True)
def _(cv, gu, language_selector, mo, t_ui, tense_selector, verb_form, words, words4test):
    # Tense Test View
    _lang = language_selector.value
    _tense_key = tense_selector.value
    _TENSE_LABELS = {
        "present": "Ενεστώτας",
        "imperfect": "Παρατατικός",
        "aorist": "Αόριστος",
        "future": "Απλός Μέλλοντας",
        "future_continuous": "Συνεχής Μέλλοντας",
        "subjunctive_simple": "Απλή Υποτακτική",
    }

    if not words4test():
        _view = mo.md(t_ui("empty_list", _lang))
    elif not _tense_key:
        _view = mo.md(t_ui("select_at_least_one", _lang))
    else:
        _feedback = ""
        if cv:
            _, _msg = gu.check_verb_test(cv['Word'], verb_form, _tense_key)
            _feedback = mo.md(_msg)

        _label = _TENSE_LABELS.get(_tense_key, _tense_key)
        _view = mo.vstack([
            mo.md(t_ui("test_heading", _lang).format(label=_label, current=len(words4test()), total=len(words))),
            mo.md(f"{t_ui('translation_label', _lang)} **{cv['Translation']}**") if cv else mo.md(""),
            verb_form,
            _feedback,
        ])

    _view
    return


@app.cell(hide_code=True)
def _(
    cv,
    gu,
    last_passed_mesg,
    mo,
    set_last_passed_mesg,
    set_words4test,
    tense_selector,
    verb_form,
    words,
    words4test,
):
    # Check and Progression
    _tense_key = tense_selector.value

    if cv and _tense_key:
        _ok, _ = gu.check_verb_test(cv['Word'], verb_form, _tense_key)
        if _ok:
            new_words4test = [w for w in words4test() if w["Word"] != cv["Word"]]
            set_words4test(new_words4test)
            remaining, total = len(new_words4test), len(words)
            passed_mesg = f'<span style="color: green;">Test for <b>"{cv["Word"]} -- {cv["Translation"]}"</b> passed.\n\n{remaining} words remaining out of {total}.</span>'
            set_last_passed_mesg(passed_mesg)

    res = mo.md(last_passed_mesg())
    res
    return


@app.cell(hide_code=True)
def _(file_upload, gu):
    # Setup test data

    test_data = [
        {"Translation": "write", "Word": "γράφω"},
        {"Translation": "read", "Word": "διαβάζω"},
        {"Translation": "speak", "Word": "μιλάω"},
        {"Translation": "drink", "Word": "πίνω"},
        {"Translation": "eat", "Word": "τρώω"},
        {"Translation": "go", "Word": "πηγαίνω"}
    ]
    df = gu.load_data(file_upload, test_data)
    return (df,)


@app.cell(hide_code=True)
def _(gu, mo, table):
    # Initialize state variables

    words = gu.get_words(table)
    words4test, set_words4test = mo.state(words.copy() if words else [])
    last_passed_mesg, set_last_passed_mesg = mo.state("")
    return (
        last_passed_mesg,
        set_last_passed_mesg,
        set_words4test,
        words,
        words4test,
    )


@app.cell(hide_code=True)
def _(gu, tense_selector, words, words4test):
    # Setup test form — derived directly from words4test state (like working version)
    cv = words4test()[0] if words4test() else None
    _tense_key = tense_selector.value
    _TENSE_UI_LABELS = {
        "present": "Present (Ενεστώτας)",
        "imperfect": "Imperfect (Παρατατικός)",
        "aorist": "Aorist (Αόριστος)",
        "future": "Simple Future (Απλός Μέλλοντας)",
        "future_continuous": "Continuous Future (Συνεχής Μέλλοντας)",
        "subjunctive_simple": "Simple Subjunctive (Απλή Υποτακτική)",
    }
    _ui_label = _TENSE_UI_LABELS.get(_tense_key, _tense_key) if _tense_key else "Select a tense"
    verb_form, _verb_md = gu.create_verb_test_ui(_ui_label, words, words4test(), cv)
    return cv, verb_form


# === Configuration and helpers (hidden) ===

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
def _():
    # Package imports

    import marimo as mo

    try:
        from modern_greek_eee import greek_utils as gu
    except ImportError:
        import greek_utils as gu

    return gu, mo


if __name__ == "__main__":
    app.run()
