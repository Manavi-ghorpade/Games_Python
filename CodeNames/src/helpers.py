import nltk

nltk.download("words")
from nltk.corpus import words


def get_english_words():
    """
    Returns a set of English words using NLTK's word list.
    Note: Requires NLTK and the 'words' dataset to be installed:
        import nltk
        nltk.download('words')

    Returns:
        set: A list of English words in lowercase
    """
    try:
        return list(words.words())
    except LookupError:
        # Provide instructions if NLTK words not installed
        raise RuntimeError(
            "NLTK words dataset not found. Please install it by running:\n"
            "import nltk\n"
            "nltk.download('words')"
        )
