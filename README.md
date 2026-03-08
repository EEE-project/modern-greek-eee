<p align="center">
  <img src="EEE-project.png" alt="EEE Project Logo" width="200"/>
</p>

# Ελληνικά Εκπαιδευτικά Εργαλεία (EEE) -- Greek Language Educational Tools

A collection of interactive **Marimo** notebooks designed to help students practice Modern Greek grammar, specifically noun declensions and verb inflections.

## Project Structure

- **`greek_nouns.py`**: Interactive notebook for practicing noun declensions (Simple and with Articles).
- **`greek_verbs.py`**: Interactive notebook for practicing verb inflections (supports Aorist, Imperfect, Future, Subjunctive, and Perfect).
- **`greek_utils.py`**: Shared utility module containing morphological logic and UI components.

## Prerequisites

- **Python 3.12+**
- **Marimo** (reactive notebook for Python)
- **modern-greek-inflexion** (morphological engine)

## Installation

1.  **Clone the repository**:
    ```bash
    git clone https://codeberg.org/sadov/modern-greek-eee.git
    cd modern-greek-eee
    ```

2.  **Install dependencies**:
    We recommend using a virtual environment:
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install -e .
    ```

## Running the Notebooks

You can run the notebooks in "edit" mode (to see the code) or "app" mode (for a clean interface).

### For Nouns:
```bash
marimo edit greek_nouns.py
# OR
marimo run greek_nouns.py
```

### For Verbs:
```bash
marimo edit greek_verbs.py
# OR
marimo run greek_verbs.py
```

## How to Work with the Forms

### 1. Load Data
By default, the notebooks come with a few sample words. You can also upload your own **TAB-delimited CSV** file using the "Load CSV" button. The file should have `Word` and `Translation` columns.

### 2. Select Words
Check the boxes next to the words you want to practice in the table. The notebooks will randomly cycle through these selected words until all are completed.

### 3. Practice Forms
- **Nouns**: Fill in the required declensions (Simple or with Articles). Both forms are synchronized to practice the same word.
- **Verbs**: Input all 6 persons (Sg/Pl) for the current tense. 
    - **Future forms** (Simple/Continuous) require the **`θα `** prefix (e.g., `θα γράψω`).
    - **Subjunctive forms** (Simple/Continuous) require the **`να `** prefix (e.g., `να γράψω`).
    - **Perfect forms** require the **`έχω `** prefix (e.g., `έχω γράψει`).
- **Feedback**: After pressing the **"Check"** button, the system will provide immediate feedback. Errors are highlighted in red with the expected result shown.

### 4. Progression
Once you correctly fill in all forms for a word, it is automatically removed from the "Words to Test" list. A progress counter (e.g., `3/6 words remaining`) keeps you updated.

## Extending the Project

The project is designed to be modular.
- **Adding new tenses**: Update the `VERB_TENSE_CONFIG` in `greek_utils.py`. The system currently supports:
    - Present (Ενεστώτας)
    - Imperfect / Past Continuous (Παρατατικός)
    - Aorist (Αόριστος)
    - Simple Future (Στιγμιαίος Μέλλοντας)
    - Continuous Future (Συνεχής Μέλλοντας)
    - Simple Subjunctive (Στιγμιαία Υποτακτική)
    - Continuous Subjunctive (Συνεχής Υποτακτική)
    - Perfect (Παρακείμενος)
- **Custom CSS**: Modify `marimo.App` settings or use a custom CSS file to change the visual theme.
