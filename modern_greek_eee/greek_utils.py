import marimo as mo
import pandas as pd
import io
import random
import unicodedata
from types import SimpleNamespace
import modern_greek_inflexion_eee as modern_greek_inflexion
from modern_greek_inflexion_eee import Article, Noun, Verb, Adjective

_ERR = '<span style="color: red; font-weight: bold;">Error!</span>'

# --- Tense Labels ---
# Tense terminology consolidation with context prefixes for field labels
# Context prefixes (θα, να, αν) shown in UI labels as "εγώ θα", "εγώ να", "εγώ αν"
# Users input only the verb form, not the prefix
TENSE_LABELS = {
    'present': {
        'greek': 'Ενεστώτας',
        'english': 'Present',
        'feedback': 'Present',
        'dropdown': 'Ενεστώτας (Present)',
        'context_prefix': '',  # No prefix context
    },
    'imperfect': {
        'greek': 'Παρατατικός',
        'english': 'Imperfect',
        'feedback': 'Imperfect',
        'dropdown': 'Παρατατικός (Imperfect)',
        'context_prefix': '',
    },
    'past_continuous': {
        'greek': 'Συνεχής Παρακείμενος',
        'english': 'Past Continuous',
        'feedback': 'Past Continuous',
        'dropdown': 'Συνεχής Παρακείμενος (Past Continuous)',
        'context_prefix': '',
    },
    'aorist': {
        'greek': 'Αόριστος',
        'english': 'Aorist',
        'feedback': 'Aorist',
        'dropdown': 'Αόριστος (Aorist)',
        'context_prefix': '',
    },
    'future': {
        'greek': 'Απλός Μέλλοντας',
        'english': 'Simple Future',
        'feedback': 'Simple Future',
        'dropdown': 'Απλός Μέλλοντας (Simple Future)',
        'context_prefix': 'θα',  # Field labels: "εγώ θα", "εσύ θα", etc.
    },
    'future_continuous': {
        'greek': 'Συνεχής Μέλλοντας',
        'english': 'Continuous Future',
        'feedback': 'Continuous Future',
        'dropdown': 'Συνεχής Μέλλοντας (Continuous Future)',
        'context_prefix': 'θα',
    },
    'subjunctive_simple': {
        'greek': 'Υποτακτική Απλή',
        'english': 'Simple Subjunctive',
        'feedback': 'Simple Subjunctive',
        'dropdown': 'Υποτακτική Απλή (Simple Subjunctive)',
        'context_prefix': 'να',  # Field labels: "εγώ να", "εσύ να", etc.
    },
    'subjunctive_continuous': {
        'greek': 'Υποτακτική Συνεχής',
        'english': 'Continuous Subjunctive',
        'feedback': 'Continuous Subjunctive',
        'dropdown': 'Υποτακτική Συνεχής (Continuous Subjunctive)',
        'context_prefix': 'να',
    },
    'conditional_simple': {
        'greek': 'Υποθετική Απλή',
        'english': 'Simple Conditional',
        'feedback': 'Simple Conditional',
        'dropdown': 'Υποθετική Απλή (Simple Conditional)',
        'context_prefix': 'αν',  # Field labels: "εγώ αν", "εσύ αν", etc. (one-time events)
        'note': 'Uses aorist forms for one-time events (e.g., "Αν διαβάσεις")',
    },
    'conditional_continuous': {
        'greek': 'Υποθετική Συνεχής',
        'english': 'Continuous Conditional',
        'feedback': 'Continuous Conditional',
        'dropdown': 'Υποθετική Συνεχής (Continuous Conditional)',
        'context_prefix': 'αν',  # Field labels: "εγώ αν", "εσύ αν", etc. (habitual events)
        'note': 'Uses present forms for habitual/regular events (e.g., "Αν διαβάζεις")',
    },
}

# --- Core Logic ---

def get_word_by_type(word, wtype):
    """Wraps a raw word string into a morphological object of a given type."""
    if word and wtype:
        word_type = getattr(modern_greek_inflexion, wtype)
        return word_type(word)
    return None

def make_snapshot(fields, **kwargs):
    """Freeze a UI fields array's current values into a plain object.

    The returned SimpleNamespace has .value (list of strings) and copies any
    metadata attributes set by create_*_test_ui (verb_word, test_word,
    active_cases, adj_word, adj_mode, etc.). Extra keyword args are also set.
    """
    s = SimpleNamespace()
    s.value = list(fields.value) if fields and fields.value else []
    for attr in ('verb_word', 'test_word', 'is_pluralia_tantum', 'active_cases', 'adj_word', 'adj_mode'):
        if hasattr(fields, attr):
            setattr(s, attr, getattr(fields, attr))
    for k, v in kwargs.items():
        setattr(s, k, v)
    return s

def word_kind(word_obj, kind_path, word_desc=None):
    """Extracts specific grammatical forms from a morphological word object.

    Args:
        word_obj: The morphological word object
        kind_path: List of keys to traverse the morphological dict
        word_desc: Optional pre-computed word_obj.all() dict to avoid recomputation
    """
    if word_obj and kind_path:
        result = word_desc if word_desc is not None else word_obj.all()
        for item in kind_path:
            if isinstance(result, dict) and item in result:
                result = result[item]
            else:
                return None
        return result
    return None

def get_words(table):
    """Selects a random subset of words from a table widget."""
    if table is not None and table.value is not None and table.value.index is not None:
        selected_words = table.data.loc[table.value.index]
        selected_words = selected_words[['Word', 'Translation']]
        return selected_words.to_dict('records')
    return []

def load_data(file_upload, default_data):
    """Helper for CSV loading or default data fallback."""
    if file_upload.value is not None and len(file_upload.value) > 0:
        contents = file_upload.value[0].contents
        contents = io.BytesIO(contents)
        return pd.read_csv(contents, sep='\t')
    return pd.DataFrame(default_data)

# --- Noun Logic ---

def _is_pluralia_tantum(noun_word):
    """Return True if the noun has no singular forms in the inflection database."""
    n_obj = get_word_by_type(noun_word, 'Noun')
    n_desc = n_obj.all() if n_obj else {}
    for noun_type in n_desc:
        sg_nom = word_kind(n_obj, [noun_type, 'sg', 'nom'])
        if sg_nom and sg_nom != {''}:
            return False
    return True


def _active_noun_cases(noun_word, is_pluralia_tantum):
    """Return the subset of cases that have non-empty forms for this noun."""
    all_cases = [['sg', 'nom'], ['sg', 'acc'], ['sg', 'gen'], ['pl', 'nom'], ['pl', 'acc'], ['pl', 'gen']]
    pl_cases  = [['pl', 'nom'], ['pl', 'acc'], ['pl', 'gen']]
    candidates = pl_cases if is_pluralia_tantum else all_cases
    v_obj = get_word_by_type(noun_word, 'Noun')
    if not v_obj:
        return candidates
    descr = v_obj.all()
    active = []
    for case in candidates:
        forms = None
        for gk in descr:
            result = descr[gk]
            for item in case:
                result = result.get(item) if isinstance(result, dict) else None
            if result and result != {''}:
                forms = result
                break
        if forms:
            active.append(case)
    return active

def create_noun_test_ui(words, mode='simple'):
    """Creates a UI form for testing noun declension."""
    word = None
    noun_form = None
    translation = None
    if words:
        item = random.choice(words)
        word = item['Word']
        translation = item['Translation']

        word_parts = word.split()
        noun_article_only = word_parts[0].strip() if len(word_parts) > 1 else None
        noun_word_only = word_parts[1].strip() if len(word_parts) > 1 else word.strip()
        # Treat as pluralia tantum if the article is plural (τα/οι) OR if the library
        # reports no singular forms.
        is_pluralia_tantum = noun_article_only in ('τα', 'οι') or _is_pluralia_tantum(noun_word_only)

        active_cases = _active_noun_cases(noun_word_only, is_pluralia_tantum)

        _simple_labels = {
            ('sg', 'nom'): 'Sg. Nom.:', ('sg', 'acc'): 'Sg. Acc.:', ('sg', 'gen'): 'Sg. Gen.:',
            ('pl', 'nom'): 'Pl. Nom.:', ('pl', 'acc'): 'Pl. Acc.:', ('pl', 'gen'): 'Pl. Gen.:',
        }
        _def_labels = {
            ('sg', 'nom'): 'Def. Sg. Nom.:', ('sg', 'acc'): 'Def. Sg. Acc.:', ('sg', 'gen'): 'Def. Sg. Gen.:',
            ('pl', 'nom'): 'Def. Pl. Nom.:', ('pl', 'acc'): 'Def. Pl. Acc.:', ('pl', 'gen'): 'Def. Pl. Gen.:',
        }
        _indef_labels = {
            ('sg', 'nom'): 'Ind. Sg. Nom.:', ('sg', 'acc'): 'Ind. Sg. Acc.:', ('sg', 'gen'): 'Ind. Sg. Gen.:',
        }

        if mode == 'simple':
            labels = [_simple_labels[tuple(c)] for c in active_cases]
        else:
            sg_cases = [c for c in active_cases if c[0] == 'sg']
            labels = (
                [_def_labels[tuple(c)] for c in active_cases] +
                [_indef_labels[tuple(c)] for c in sg_cases]
            )

        noun_form = mo.ui.array([mo.ui.text(label=l) for l in labels])
        noun_form.test_word = word
        noun_form.is_pluralia_tantum = is_pluralia_tantum
        noun_form.active_cases = active_cases
    return word, translation, noun_form

def _ci_match(value, forms):
    """Case-insensitive, NFC-normalized membership test."""
    if not forms:
        return False
    value_norm = unicodedata.normalize('NFC', value).lower()
    return any(unicodedata.normalize('NFC', f).lower() == value_norm for f in forms)

def _noun_declension_test(user_input, declension, noun_base, noun_descr, article_descr, article_gender=None):
    """Internal validator for a single noun form."""
    if not user_input:
        return False

    parts = user_input.split()
    if len(parts) > 1:
        noun_article = parts[0].strip()
        noun_word = parts[1].strip()
    else:
        noun_article = ''
        noun_word = user_input.strip()

    # When article_gender is known, try it first; iterate all gender keys until forms are found.
    # Use noun_descr directly — it's already the correct description (incl. neuter sg lookup).
    gender_keys = list(noun_descr.keys())
    if article_gender and article_gender in noun_descr:
        gender_keys = [article_gender] + [k for k in gender_keys if k != article_gender]
    noun_type = gender_keys[0]

    correct_noun_forms = None
    for gk in gender_keys:
        result = noun_descr.get(gk, {})
        for item in declension:
            result = result.get(item) if isinstance(result, dict) else None
        if result:
            noun_type = gk
            correct_noun_forms = result
            break
    word_is_correct = _ci_match(noun_word, correct_noun_forms)

    _num = {'sg': 'Sg.', 'pl': 'Pl.'}.get(declension[0], declension[0])
    _case = {'nom': 'Nom.', 'acc': 'Acc.', 'gen': 'Gen.'}.get(declension[1], declension[1])

    if article_descr is None:
        if word_is_correct:
            return True
        else:
            _correct = " / ".join(sorted(correct_noun_forms)) if correct_noun_forms else "?"
            print(f'{_ERR} [{_num} {_case}]: entered **"{noun_word}"**, must be **{_correct}**<br>')
            return False

    art_type = article_gender if article_gender is not None else noun_type
    art_path = [declension[0], art_type, declension[1]]
    article_forms = word_kind(article_descr, art_path)

    if _ci_match(noun_article, article_forms) and word_is_correct:
        return True
    else:
        article_type = 'def' if article_descr.article in ['ο', 'η', 'το'] else 'indef'
        _art_prefix = {'def': 'Def.', 'indef': 'Indef.'}.get(article_type, article_type)
        _art_str = " / ".join(sorted(article_forms)) if article_forms else "?"
        _noun_str = " / ".join(sorted(correct_noun_forms)) if correct_noun_forms else "?"
        _correct = f"{_art_str} {_noun_str}"
        print(f'{_ERR} [{_art_prefix} {_num} {_case}]: entered **"{user_input}"**, must be **{_correct}**<br>')
        return False

def check_noun_test(noun, noun_form, mode='simple'):
    """Checks noun declension forms."""
    if not noun or noun_form is None or not noun_form.value:
        return False
        
    if hasattr(noun_form, 'test_word') and noun_form.test_word != noun:
        return False

    noun_array = noun.split()
    noun_article = noun_array[0].strip() if len(noun_array) > 1 else None
    noun_word = noun_array[1].strip() if len(noun_array) > 1 else noun.strip()

    # For 'τα X' entries (neuter plural), the headword is the plural form.
    # The library may return the feminine reading; look up neuter sg (word[:-1]+'ο') instead.
    v_obj = None
    descr = None
    if noun_article == 'τα':
        candidate = noun_word[:-1] + 'ο'
        candidate_obj = get_word_by_type(candidate, 'Noun')
        if candidate_obj:
            candidate_desc = candidate_obj.all()
            if list(candidate_desc.keys())[0] == 'neut':
                v_obj, descr = candidate_obj, candidate_desc
    if v_obj is None:
        v_obj = get_word_by_type(noun_word, 'Noun')
        if not v_obj:
            return False
        descr = v_obj.all()

    is_pluralia_tantum = getattr(noun_form, 'is_pluralia_tantum', False)
    active_cases = getattr(noun_form, 'active_cases', None)
    if not isinstance(active_cases, list):
        all_cases = [['sg', 'nom'], ['sg', 'acc'], ['sg', 'gen'], ['pl', 'nom'], ['pl', 'acc'], ['pl', 'gen']]
        pl_cases  = [['pl', 'nom'], ['pl', 'acc'], ['pl', 'gen']]
        active_cases = pl_cases if is_pluralia_tantum else all_cases

    if mode == 'simple':
        checks = [_noun_declension_test(val, case, noun_word, descr, None)
                  for val, case in zip(noun_form.value, active_cases)]
        return all(checks)
    else:
        noun_type = list(descr.keys())[0] if descr else 'masc'
        # Article('ο') covers ALL definite forms (sg/pl × masc/fem/neut).
        # article_gender + declension path select the right form during validation.
        # 'οι' gender is ambiguous — resolve from noun_type.
        _article_to_gender = {'ο': 'masc', 'η': 'fem', 'το': 'neut', 'τα': 'neut', 'οι': noun_type}
        article_gender = _article_to_gender.get(noun_article) if noun_article else None
        art_def = Article('ο')
        art_indef = Article('ένας')
        sg_cases = [c for c in active_cases if c[0] == 'sg']
        def_checks = [_noun_declension_test(val, case, noun_word, descr, art_def, article_gender)
                      for val, case in zip(noun_form.value, active_cases)]
        indef_checks = [_noun_declension_test(val, case, noun_word, descr, art_indef, article_gender)
                        for val, case in zip(noun_form.value[len(active_cases):], sg_cases)]
        return all(def_checks) and all(indef_checks)

def process_noun_test(noun, noun_form, words, words4test, set_words4test, set_last_passed_mesg, set_current_noun=None, mode='simple'):
    """Processes noun test result for a specific mode and updates state."""
    w4t = words4test() if callable(words4test) else words4test
    if not w4t or noun_form is None or not noun_form.value:
        return mo.md("")
    
    output = ""
    with mo.capture_stdout() as buffer:
        passed = check_noun_test(noun, noun_form, mode)
        if passed:
            new_words4test = [w for w in w4t if w["Word"] != noun]
            set_words4test(new_words4test)
            remaining, total = len(new_words4test), len(words)
            msg = f'<span style="color: green;">Test for <b>"{noun}"</b> passed.\n\n{remaining} words remaining out of {total}.</span>'
            set_last_passed_mesg(msg)
            if set_current_noun:
                # Pick a new word that is different from the current one if possible
                _candidates = [w for w in new_words4test if w["Word"] != noun]
                if not _candidates and new_words4test:
                    _candidates = new_words4test
                
                if _candidates:
                    set_current_noun(random.choice(_candidates))
                else:
                    set_current_noun(None)
            output = msg
        else:
            output = buffer.getvalue()
            
    return mo.md(output)

# --- Verb Logic ---

VERB_TENSE_CONFIG = {
    'present': {  # Present (Ενεστώτας)
        'path': ['present', 'active', 'ind'],
    },
    'imperfect': {  # Imperfect (Παρατατικός)
        'path': ['paratatikos', 'active', 'ind'],
        'alt_path': ['imperfect', 'active', 'ind'],
    },
    'past_continuous': {  # Past Continuous (Παρατατικός)
        'path': ['paratatikos', 'active', 'ind'],
        'alt_path': ['imperfect', 'active', 'ind'],
    },
    'aorist': {  # Aorist (Αόριστος)
        'path': ['aorist', 'active', 'ind'],
    },
    'future': {  # Simple Future (Στιγμιαίος Μέλλοντας)
        'path': ['conjunctive', 'active', 'ind'],
        'alt_path': ['conjunctive', 'active', 'subj'],
        'fallback_path': ['present', 'active', 'ind'],
        'prefix': 'θα',
    },
    'future_continuous': {  # Continuous Future (Συνεχής Μέλλοντας)
        'path': ['present', 'active', 'ind'],
        'prefix': 'θα',
    },
    'subjunctive_simple': {  # Simple Subjunctive (Στιγμιαία Υποτακτική)
        'path': ['conjunctive', 'active', 'ind'],
        'alt_path': ['conjunctive', 'active', 'subj'],
        'fallback_path': ['present', 'active', 'ind'],
        'prefix': 'να',
    },
    'subjunctive_continuous': {  # Continuous Subjunctive (Συνεχής Υποτακτική)
        'path': ['present', 'active', 'ind'],
        'prefix': 'να',
    },
    'conditional_simple': {  # Simple Conditional (Υποθετική Απλή) - uses CONJUNCTIVE (subjunctive aorist) forms
        'path': ['conjunctive', 'active', 'ind'],
        'alt_path': ['conjunctive', 'active', 'subj'],
        'fallback_path': ['present', 'active', 'ind'],
        'prefix': 'αν',
    },
    'conditional_continuous': {  # Continuous Conditional (Υποθετική Συνεχής) - uses PRESENT forms
        'path': ['present', 'active', 'ind'],
        'prefix': 'αν',
    }
}

def create_verb_test_ui(title, words, words4test_val, current_verb):
    """Generates verb form UI."""
    form = None
    md_view = mo.md(f'**The word list for {title} is empty.**')

    if current_verb:
        word = current_verb["Word"]
        translation = current_verb["Translation"]

        form = mo.ui.array([
            mo.ui.text(label="εγώ:"),
            mo.ui.text(label="εσύ:"),
            mo.ui.text(label="αυτός,-ή,-ό:"),
            mo.ui.text(label="εμείς:"),
            mo.ui.text(label="εσείς:"),
            mo.ui.text(label="αυτοί,-ές,-ά:"),
        ])
        form.verb_word = word

        if len(words4test_val):
            md_view = mo.md(f"""
            ### {title}
            (words: {len(words4test_val)}/{len(words)})
            Translation: **{translation}**
            {form}
            """)
    return form, md_view

def _patch_voice(path, v_desc):
    """Replace voice element in path[1] with the voice actually present in v_desc."""
    if not path or len(path) < 2:
        return path
    tense_data = v_desc.get(path[0], {})
    for voice in ('active', 'middle', 'passive'):
        if voice in tense_data:
            if voice == path[1]:
                return path
            patched = list(path)
            patched[1] = voice
            return patched
    return path

def check_verb_test(verb_base, form_array, tense):
    """Validates verb forms using modular tense configuration."""
    if form_array is None or not form_array.value:
        return False, ""
    if hasattr(form_array, 'verb_word') and form_array.verb_word != verb_base:
        return False, ""
    
    config = VERB_TENSE_CONFIG.get(tense)
    if not config:
        return False, f"Error: Unknown tense '{tense}'"

    v_obj = get_word_by_type(verb_base, 'Verb')
    if not v_obj:
        return False, "Error: Morphological object not found."

    # Cache morphological expansion to avoid 6+ redundant calls in the loop
    v_desc = v_obj.all()

    persons = ['pri', 'sec', 'ter']
    numbers = ['sg', 'pl']

    possible_paths = [_patch_voice(config.get('path'), v_desc)]
    if 'alt_path' in config:
        possible_paths.append(_patch_voice(config['alt_path'], v_desc))
    if 'fallback_path' in config:
        possible_paths.append(_patch_voice(config['fallback_path'], v_desc))

    path_prefix = None
    for p in possible_paths:
        if p and word_kind(v_obj, p, v_desc):
            path_prefix = p
            break

    if not path_prefix:
        path_prefix = config.get('path')

    # Defective verb: no forms exist at any person/number for this tense
    if not any(word_kind(v_obj, path_prefix + [num, pers], v_desc) for num in numbers for pers in persons):
        return False, f'{_ERR} [defective verb]: **{verb_base}** has no {tense} forms — remove from test list'

    display_prefix = config.get('prefix', '')
    prefix_lower = display_prefix.lower() if display_prefix else ''
    pronouns = ['εγώ', 'εσύ', 'αυτός,-ή,-ό', 'εμείς', 'εσείς', 'αυτοί,-ές,-ά']
    success, errors, idx = True, [], 0

    for num in numbers:
        for pers in persons:
            user_val = form_array.value[idx].strip()
            pronoun = pronouns[idx]
            idx += 1
            if not user_val:
                success = False
                continue

            check_val = user_val
            if prefix_lower:
                if user_val.lower().startswith(prefix_lower):
                    check_val = user_val[len(display_prefix):].strip()
                else:
                    errors.append(f'{_ERR} [{pronoun}]: Write with **"{display_prefix.strip()}"**')
                    success = False
                    continue

            correct_forms = word_kind(v_obj, path_prefix + [num, pers], v_desc)
            if not correct_forms or not _ci_match(check_val, correct_forms):
                success = False
                available_tenses = list(v_desc.keys())
                expected = "/".join(correct_forms) if correct_forms else f"unknown (path: {path_prefix}, keys: {available_tenses})"
                if display_prefix: expected = f"{display_prefix} {expected}"
                errors.append(f'{_ERR} [{pronoun}]: entered **"{user_val}"**, must be **{expected}**')

    return success, "<br>".join(errors)

def process_verb_completion(current_verb_val, aorist_ok, future_ok, words, words4test_val, set_words4test, set_last_passed_mesg, set_current_verb):
    """Updates state and returns message after verb test completion."""
    if aorist_ok and future_ok and current_verb_val:
        new_words4test = [w for w in words4test_val if w["Word"] != current_verb_val["Word"]]
        set_words4test(new_words4test)
        remaining, total = len(new_words4test), len(words)
        passed_mesg = f'<span style="color: green;">Test for <b>"{current_verb_val["Word"]} -- {current_verb_val["Translation"]}"</b> passed.\n\n{remaining} words remaining out of {total}.</span>'
        set_last_passed_mesg(passed_mesg)
        if new_words4test:
            set_current_verb(random.choice(new_words4test))
        else:
            set_current_verb(None)
        return passed_mesg
    return ""

# --- Adjective Logic ---

def create_adjective_test_ui(words, words4test_val, current_adj, mode='simple'):
    """Generates adjective form UI.

    Simple mode: 6 fields (all singulars first: Masc/Fem/Neut Sg, then all plurals: Masc/Fem/Neut Pl)
    Complex mode: 18 fields (all singulars for all genders × cases, then all plurals for all genders × cases)
    """
    form = None
    md_view = mo.md(f'**The word list for adjective test is empty.**')

    if current_adj:
        word = current_adj["Word"]
        translation = current_adj["Translation"]

        # Get field labels from schema to ensure consistency
        _, field_labels = _adj_field_schema(mode)
        labels = [f"{label}:" for label in field_labels]

        form = mo.ui.array([mo.ui.text(label=l) for l in labels])
        form.adj_word = word
        form.adj_mode = mode

        if len(words4test_val):
            md_view = mo.md(f"""
            ### Test: Adjective Declension ({len(words4test_val)}/{len(words)})
            Translation: **{translation}**
            {form}
            """)
    return form, md_view

def _adj_field_schema(mode):
    """Builds field keys and labels for adjective test based on mode.

    Simple mode: 6 fields (all singulars first: Masc/Fem/Neut Sg, then all plurals: Masc/Fem/Neut Pl)
    Complex mode: 18 fields (all singulars for all genders × cases, then all plurals for all genders × cases)
    """
    gender_config = [('masculine', 'masc', 'Masc'), ('feminine', 'fem', 'Fem'), ('neuter', 'neut', 'Neut')]
    cases = [('nom', 'Nom'), ('acc', 'Acc'), ('gen', 'Gen')]

    field_keys = []
    field_labels = []

    if mode == 'simple':
        # Simple: all singulars first (3 genders), then all plurals (3 genders), nominative only
        # Singulars: Masc Sg, Fem Sg, Neut Sg
        for gender_label, _gender_key, gender_short in gender_config:
            field_keys.append(f'{gender_label}_sg_nom')
            field_labels.append(f'{gender_short} Sg')
        # Plurals: Masc Pl, Fem Pl, Neut Pl
        for gender_label, _gender_key, gender_short in gender_config:
            field_keys.append(f'{gender_label}_pl_nom')
            field_labels.append(f'{gender_short} Pl')
    else:
        # Complex: all singulars first (all genders × 3 cases), then all plurals
        # Singulars: Masc Sg (Nom, Acc, Gen), Fem Sg (Nom, Acc, Gen), Neut Sg (Nom, Acc, Gen)
        for gender_label, _gender_key, gender_short in gender_config:
            for case_key, case_short in cases:
                field_keys.append(f'{gender_label}_sg_{case_key}')
                field_labels.append(f'{gender_short} Sg {case_short}')
        # Plurals: Masc Pl (Nom, Acc, Gen), Fem Pl (Nom, Acc, Gen), Neut Pl (Nom, Acc, Gen)
        for gender_label, _gender_key, gender_short in gender_config:
            for case_key, case_short in cases:
                field_keys.append(f'{gender_label}_pl_{case_key}')
                field_labels.append(f'{gender_short} Pl {case_short}')

    return field_keys, field_labels


def _adj_expected_forms(adj_base, mode, adj_desc=None):
    """Builds expected forms dict from morphological library.

    Args:
        adj_base: The adjective base word
        mode: 'simple' or 'complex'
        adj_desc: Optional pre-computed adj_obj.all() dict to avoid recomputation

    Returns dict mapping field_key -> list of acceptable forms.
    """
    cases = ['nom'] if mode == 'simple' else ['nom', 'acc', 'gen']
    gender_config = [('masculine', 'masc'), ('feminine', 'fem'), ('neuter', 'neut')]

    expected = {}

    if adj_desc is None:
        adj_obj = get_word_by_type(adj_base, 'Adjective')
        if adj_obj:
            try:
                adj_desc = adj_obj.all()
            except Exception:
                adj_desc = None

    if adj_desc:
        try:
            for gender_label, gender_key in gender_config:
                for num_key in ['sg', 'pl']:
                    for case_key in cases:
                        forms = adj_desc.get('adj', {}).get(num_key, {}).get(gender_key, {}).get(case_key, set())
                        key = f'{gender_label}_{num_key}_{case_key}'
                        expected[key] = list(forms) if forms else [adj_base]
        except Exception:
            pass

    # Fill missing keys with fallback
    for gender_label, _gender_key in gender_config:
        for num_key in ['sg', 'pl']:
            for case_key in cases:
                key = f'{gender_label}_{num_key}_{case_key}'
                if key not in expected:
                    expected[key] = [adj_base]

    return expected


def check_adjective_test(adj_base, form_array, mode='simple'):
    """Validates adjective forms with mode support.

    Simple mode: validates 6 forms (3 genders × 2 numbers: singular + plural nominative)
    Complex mode: validates 18 forms (3 genders × 2 numbers × 3 cases: nom, acc, gen)

    Allow partial input - only validate non-empty fields."""
    if form_array is None or not form_array.value:
        return False, ""
    if hasattr(form_array, 'adj_word') and form_array.adj_word != adj_base:
        return False, ""

    if hasattr(form_array, 'adj_mode'):
        mode = form_array.adj_mode

    # Cache morphological expansion to pass to _adj_expected_forms
    adj_obj = get_word_by_type(adj_base, 'Adjective')
    adj_desc = None
    if adj_obj:
        try:
            adj_desc = adj_obj.all()
        except Exception:
            pass

    field_keys, field_labels = _adj_field_schema(mode)
    expected_forms = _adj_expected_forms(adj_base, mode, adj_desc)

    success = True
    has_any_input = False
    errors = []

    for idx, (field_key, field_label) in enumerate(zip(field_keys, field_labels)):
        user_val = form_array.value[idx].strip()
        if not user_val:
            success = False
            continue

        has_any_input = True
        correct_forms = expected_forms.get(field_key, [adj_base])

        if not _ci_match(user_val, correct_forms):
            success = False
            correct_text = "/".join(correct_forms)
            errors.append(f'{_ERR} [{field_label}]: entered **"{user_val}"**, must be **{correct_text}**')

    if not has_any_input:
        return False, f'{_ERR} Please fill in at least one gender form'

    return success, "<br>".join(errors)

def process_adjective_completion(current_adj_val, adj_ok, words, words4test_val, set_words4test, set_last_passed_mesg, set_current_adj):
    """Updates state and returns message after adjective test completion."""
    if adj_ok and current_adj_val:
        new_words4test = [w for w in words4test_val if w["Word"] != current_adj_val["Word"]]
        set_words4test(new_words4test)
        remaining, total = len(new_words4test), len(words)
        passed_mesg = f'<span style="color: green;">Test for <b>"{current_adj_val["Word"]} -- {current_adj_val["Translation"]}"</b> passed.\n\n{remaining} words remaining out of {total}.</span>'
        set_last_passed_mesg(passed_mesg)
        if new_words4test:
            set_current_adj(random.choice(new_words4test))
        else:
            set_current_adj(None)
        return passed_mesg
    return ""

# --- Display Helpers ---

def make_noun_display(header, translation_md, result, form, done_msg):
    """Build vstack for noun/adj display cell. Returns done message when form is None."""
    if form is not None:
        return mo.vstack([mo.md(header), mo.md(translation_md), result, form])
    return mo.md(done_msg)


def make_verb_display(header, msg_fn, result, form, done_msg):
    """Build vstack for verb/adj display cell. Returns done message when form is None."""
    if form is not None:
        items = [mo.md(header)]
        _msg = msg_fn() if msg_fn else None
        if _msg:
            items.append(mo.md(_msg))
        items += [result, form]
        return mo.vstack(items)
    return mo.md(done_msg)
