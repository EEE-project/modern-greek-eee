# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo>=0.19.4",
#     "mcp==1.25.0",
#     "modern-greek-eee @ git+https://github.com/EEE-project/modern-greek-eee.git",
#     "modern-greek-inflexion==2.0.7",
#     "pandas==2.3.3",
# ]
#
# [tool.uv.sources]
# modern-greek-eee = { git = "https://github.com/EEE-project/modern-greek-eee" }
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
    tense_selector = mo.ui.multiselect(
        options={
            "Ενεστώτας (Present)": "present",
            "Παρατατικός (Imperfect)": "imperfect",
            "Αόριστος (Aorist)": "aorist",
            "Απλός Μέλλοντας (Simple Future)": "future",
            "Συνεχής Μέλλοντας (Continuous Future)": "future_continuous",
            "Απλή Υποτακτική (Simple Subjunctive)": "subjunctive_simple",
        },
        value=["Αόριστος (Aorist)", "Απλός Μέλλοντας (Simple Future)"],
        label=t_ui("select_tenses", _lang),
        full_width=True,
    )
    mo.md(f"""
    {t_ui("practice_heading", _lang)}

    {tense_selector}
    """)
    return (tense_selector,)


@app.cell(hide_code=True)
def _(cv, gu, language_selector, mo, t_ui, tense_forms, tense_selector, words, words4test):
    # Dynamic Tense Test Views
    _lang = language_selector.value
    _ALL_FORMS = {
        "present": ("Ενεστώτας", tense_forms["present"]),
        "imperfect": ("Παρατατικός", tense_forms["imperfect"]),
        "aorist": ("Αόριστος", tense_forms["aorist"]),
        "future": ("Απλός Μέλλοντας", tense_forms["future"]),
        "future_continuous": ("Συνεχής Μέλλοντας", tense_forms["future_continuous"]),
        "subjunctive_simple": ("Απλή Υποτακτική", tense_forms["subjunctive_simple"]),
    }

    if not words4test():
        _view = mo.md(t_ui("empty_list", _lang))
    else:
        _cv = cv()
        _header = mo.md(f"{t_ui('translation_label', _lang)} **{_cv['Translation']}**") if _cv else mo.md("")
        _views = [_header]

        for _tense_key in tense_selector.value:
            if _tense_key not in _ALL_FORMS:
                continue
            _label, _verb_form = _ALL_FORMS[_tense_key]
            if _verb_form is None:
                continue

            _feedback = ""
            if _cv:
                _, _msg = gu.check_verb_test(_cv['Word'], _verb_form, _tense_key)
                _feedback = mo.md(_msg)

            _tense_view = mo.vstack([
                mo.md(t_ui("test_heading", _lang).format(label=_label, current=len(words4test()), total=len(words))),
                _verb_form,
                _feedback,
            ])
            _views.append(_tense_view)

        _view = mo.vstack(_views) if len(_views) > 1 else mo.md(t_ui("select_at_least_one", _lang))

    _view
    return


@app.cell(hide_code=True)
def _(
    cv,
    gu,
    last_passed_mesg,
    mo,
    set_cv,
    set_last_passed_mesg,
    set_words4test,
    tense_forms,
    tense_selector,
    words,
    words4test,
):
    # Check and Progression: all selected tenses must pass before moving on
    _ALL_FORMS = {
        "present": tense_forms["present"],
        "imperfect": tense_forms["imperfect"],
        "aorist": tense_forms["aorist"],
        "future": tense_forms["future"],
        "future_continuous": tense_forms["future_continuous"],
        "subjunctive_simple": tense_forms["subjunctive_simple"],
    }
    _current_verb = cv()

    if _current_verb:
        _all_passed = True
        for _tense_key in tense_selector.value:
            _f = _ALL_FORMS.get(_tense_key)
            if _f is not None:
                _ok, _ = gu.check_verb_test(_current_verb['Word'], _f, _tense_key)
                if not _ok:
                    _all_passed = False
                    break

        if _all_passed:
            import random as _random
            new_words4test = [w for w in words4test() if w["Word"] != _current_verb["Word"]]
            set_words4test(new_words4test)
            if new_words4test:
                set_cv(_random.choice(new_words4test))
            else:
                set_cv(None)
            remaining, total = len(new_words4test), len(words)
            passed_mesg = f'<span style="color: green;">Test for <b>"{_current_verb["Word"]} -- {_current_verb["Translation"]}"</b> passed.\n\n{remaining} words remaining out of {total}.</span>'
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
    cv, set_cv = mo.state(None)
    return (
        cv,
        last_passed_mesg,
        set_cv,
        set_last_passed_mesg,
        set_words4test,
        words,
        words4test,
    )


@app.cell(hide_code=True)
def _(cv, gu, set_cv, words, words4test):
    # Setup test forms for all tenses
    _current_verb = cv()
    if not _current_verb and words4test():
        import random as _random
        _current_verb = _random.choice(words4test())
        set_cv(_current_verb)

    tense_forms = {
        "present": gu.create_verb_test_ui("Present (Ενεστώτας)", words, words4test(), _current_verb)[0],
        "imperfect": gu.create_verb_test_ui("Imperfect (Παρατατικός)", words, words4test(), _current_verb)[0],
        "aorist": gu.create_verb_test_ui("Aorist (Αόριστος)", words, words4test(), _current_verb)[0],
        "future": gu.create_verb_test_ui("Simple Future (Απλός Μέλλοντας)", words, words4test(), _current_verb)[0],
        "future_continuous": gu.create_verb_test_ui("Continuous Future (Συνεχής Μέλλοντας)", words, words4test(), _current_verb)[0],
        "subjunctive_simple": gu.create_verb_test_ui("Simple Subjunctive (Απλή Υποτακτική)", words, words4test(), _current_verb)[0],
    }
    return (tense_forms,)


# === Configuration and helpers (hidden) ===

@app.cell(hide_code=True)
def _():
    UI_STRINGS = {
        "en": {
            "title": "Modern Greek — Verb Conjugation",
            "description": "Practice verb conjugation across multiple tenses.",
            "select_hint": "Select a tense or combination of tenses to practice: Present, Imperfect, Aorist, Simple Future, Continuous Future, or Simple Subjunctive.",
            "use_csv": "Use the sample word set or upload a TAB-delimited CSV file with \"Word\" and \"Translation\" columns.",
            "file_upload": "Load TSV",
            "select_tenses": "Select tenses:",
            "practice_heading": "## Practice: Verb Conjugation",
            "empty_list": "Word list is empty. Select words in the table above.",
            "translation_label": "Translation:",
            "test_heading": "### Test: {label} ({current}/{total})",
            "select_at_least_one": "Select at least one tense above.",
        },
        "ru": {
            "title": "Новогреческий — Спряжение глаголов",
            "description": "Попрактикуйте спряжение глаголов в различных временах.",
            "select_hint": "Выберите один или несколько времен для практики: Present, Imperfect, Aorist, Simple Future, Continuous Future или Simple Subjunctive.",
            "use_csv": "Используйте образец набора слов или загрузите CSV-файл с табуляцией в качестве разделителя со столбцами \"Word\" и \"Translation\".",
            "file_upload": "Загрузить TSV",
            "select_tenses": "Выберите времена:",
            "practice_heading": "## Практика: Спряжение глаголов",
            "empty_list": "Список слов пуст. Выберите слова в таблице выше.",
            "translation_label": "Перевод:",
            "test_heading": "### Тест: {label} ({current}/{total})",
            "select_at_least_one": "Выберите хотя бы одно время выше.",
        },
        "el": {
            "title": "Νέα Ελληνικά — Σύζευξη Ρημάτων",
            "description": "Εξασκηθείτε σε ρηματική σύζευξη σε διάφορους χρόνους.",
            "select_hint": "Επιλέξτε έναν ή περισσότερους χρόνους για εξάσκηση: Present, Imperfect, Aorist, Simple Future, Continuous Future ή Simple Subjunctive.",
            "use_csv": "Χρησιμοποιήστε το δείγμα συνόλου λέξεων ή φορτώστε ένα αρχείο CSV που οριοθετείται με TAB με στήλες \"Word\" και \"Translation\".",
            "file_upload": "Φόρτωση TSV",
            "select_tenses": "Επιλέξτε χρόνους:",
            "practice_heading": "## Εξάσκηση: Σύζευξη Ρημάτων",
            "empty_list": "Η λίστα λέξεων είναι κενή. Επιλέξτε λέξεις στον παραπάνω πίνακα.",
            "translation_label": "Μετάφραση:",
            "test_heading": "### Τεστ: {label} ({current}/{total})",
            "select_at_least_one": "Επιλέξτε τουλάχιστον έναν χρόνο παραπάνω.",
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
