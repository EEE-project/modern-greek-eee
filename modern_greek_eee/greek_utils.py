import marimo as mo
import pandas as pd
import io
import random
import modern_greek_inflexion_eee as modern_greek_inflexion
from modern_greek_inflexion_eee import Article, Noun, Verb, Adjective

# --- Core Logic ---

def get_word_by_type(word, wtype):
    """Wraps a raw word string into a morphological object of a given type."""
    if word and wtype:
        word_type = getattr(modern_greek_inflexion, wtype)
        return word_type(word)
    return None

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

def create_noun_test_ui(words, mode='simple'):
    """Creates a UI form for testing noun declension."""
    word = None
    noun_form = None
    translation = None
    if words:
        item = random.choice(words)
        word = item['Word']
        translation = item['Translation']

        if mode == 'simple':
            labels = ['Sg. Nom.:', 'Sg. Acc.:', 'Sg. Gen.:', 'Pl. Nom.:', 'Pl. Acc.:', 'Pl. Gen.:']
        else:
            labels = [
                'Def. Sg. Nom.:', 'Def. Sg. Acc.:', 'Def. Sg. Gen.:',
                'Def. Pl. Nom.:', 'Def. Pl. Acc.:', 'Def. Pl. Gen.:',
                'Ind. Sg. Nom.:', 'Ind. Sg. Acc.:', 'Ind. Sg. Gen.:'
            ]
        
        noun_form = mo.ui.array([mo.ui.text(label=l) for l in labels]).form(label="Check", show_clear_button=True)
        noun_form.test_word = word
    return word, translation, noun_form

def _ci_match(value, forms):
    """Case-insensitive membership test with early exit. Returns True if value.lower() matches any form.lower()"""
    if not forms:
        return False
    value_lower = value.lower()
    return any(f.lower() == value_lower for f in forms)

def _noun_declension_test(user_input, declension, noun_base, noun_descr, article_descr):
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

    noun_type = list(noun_descr.keys())[0]
    noun_path = [noun_type] + declension

    # Validate noun form
    correct_noun_forms = word_kind(get_word_by_type(noun_base, 'Noun'), noun_path)
    word_is_correct = _ci_match(noun_word, correct_noun_forms)

    if article_descr is None:
        if word_is_correct:
            return True
        else:
            case_label = f"{declension[0]}.{declension[1]}"
            print(f'<span style="color: red; font-weight: bold;">Error!</span> [{case_label}]: entered **"{noun_word}"**, must be **{correct_noun_forms}**\n\n')
            return False

    art_path = [declension[0], noun_type, declension[1]]
    article_forms = word_kind(article_descr, art_path)

    if _ci_match(noun_article, article_forms) and word_is_correct:
        return True
    else:
        article_type = 'def' if article_descr.article in ['ο', 'η', 'το'] else 'indef'
        case_label = f"{article_type}.{declension[0]}.{declension[1]}"
        correct_full = f"{article_forms} {correct_noun_forms}"
        print(f'<span style="color: red; font-weight: bold;">Error!</span> [{case_label}]: entered **"{user_input}"**, must be **{correct_full}**\n\n')
        return False

def check_noun_test(noun, noun_form, mode='simple'):
    """Checks noun declension forms."""
    if not noun or noun_form is None or not noun_form.value:
        return False
        
    if hasattr(noun_form, 'test_word') and noun_form.test_word != noun:
        return False

    noun_array = noun.split()
    noun_word = noun_array[1].strip() if len(noun_array) > 1 else noun.strip()
    
    v_obj = get_word_by_type(noun_word, 'Noun')
    if not v_obj:
        return False
    descr = v_obj.all()

    cases = [['sg', 'nom'], ['sg', 'acc'], ['sg', 'gen'], ['pl', 'nom'], ['pl', 'acc'], ['pl', 'gen']]
    
    if mode == 'simple':
        checks = [_noun_declension_test(val, case, noun_word, descr, None) 
                  for val, case in zip(noun_form.value, cases)]
        return all(checks)
    else:
        art_def = Article('ο')
        art_indef = Article('ένας')
        def_checks = [_noun_declension_test(val, case, noun_word, descr, art_def) 
                      for val, case in zip(noun_form.value[:6], cases)]
        indef_checks = [_noun_declension_test(val, case, noun_word, descr, art_indef) 
                        for val, case in zip(noun_form.value[6:], cases[:3])]
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
        'prefix': 'θα ',
    },
    'future_continuous': {  # Continuous Future (Συνεχής Μέλλοντας)
        'path': ['present', 'active', 'ind'],
        'prefix': 'θα ',
    },
    'subjunctive_simple': {  # Simple Subjunctive (Στιγμιαία Υποτακτική)
        'path': ['conjunctive', 'active', 'ind'],
        'alt_path': ['conjunctive', 'active', 'subj'],
        'fallback_path': ['present', 'active', 'ind'],
        'prefix': 'να ',
    },
    'subjunctive_continuous': {  # Continuous Subjunctive (Συνεχής Υποτακτική)
        'path': ['present', 'active', 'ind'],
        'prefix': 'να ',
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
        ]).form(show_clear_button=True)
        form.verb_word = word

        if len(words4test_val):
            md_view = mo.md(f"""
            ### {title}
            (words: {len(words4test_val)}/{len(words)})
            Translation: **{translation}**
            {form}
            """)
    return form, md_view

def check_verb_test(verb_base, form_array, tense):
    """Validates verb forms using modular tense configuration."""
    if form_array is None or form_array.value is None:
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

    possible_paths = [config.get('path')]
    if 'alt_path' in config:
        possible_paths.append(config['alt_path'])
    if 'fallback_path' in config:
        possible_paths.append(config['fallback_path'])

    path_prefix = None
    for p in possible_paths:
        if p and word_kind(v_obj, p, v_desc):
            path_prefix = p
            break

    if not path_prefix:
        path_prefix = config.get('path')

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
                    errors.append(f'<span style="color: red; font-weight: bold;">Error!</span> [{pronoun}]: Write with **"{display_prefix.strip()}"**')
                    success = False
                    continue

            correct_forms = word_kind(v_obj, path_prefix + [num, pers], v_desc)
            if not correct_forms or not _ci_match(check_val, correct_forms):
                success = False
                available_tenses = list(v_desc.keys())
                expected = "/".join(correct_forms) if correct_forms else f"unknown (path: {path_prefix}, keys: {available_tenses})"
                if display_prefix: expected = f"{display_prefix}{expected}"
                errors.append(f'<span style="color: red; font-weight: bold;">Error!</span> [{pronoun}]: entered **"{user_val}"**, must be **{expected}**')

    return success, "\n\n".join(errors)

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

        form = mo.ui.array([mo.ui.text(label=l) for l in labels]).form(show_clear_button=True)
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
    if form_array is None or form_array.value is None:
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
            errors.append(f'<span style="color: red; font-weight: bold;">Error!</span> [{field_label}]: entered **"{user_val}"**, must be **{correct_text}**')

    if not has_any_input:
        return False, '<span style="color: red; font-weight: bold;">Error!</span> Please fill in at least one gender form'

    return success, "\n\n".join(errors)

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
