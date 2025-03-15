import nltk
import numpy as np
from nltk.stem.porter import PorterStemmer

# Initialize the PorterStemmer
stemmer = PorterStemmer()

# Ensure necessary NLTK downloads
nltk.download("punkt")

def tokenize(sentence):
    """Tokenizes a sentence into words."""
    return nltk.word_tokenize(sentence)

def stem(word):
    """Stems a word to its root form."""
    return stemmer.stem(word.lower())

def bag_of_words(tokenized_sentence, words):
    """Creates a bag of words representation."""
    sentence_words = [stem(word) for word in tokenized_sentence]
    bag = np.zeros(len(words), dtype=np.float32)
    for idx, w in enumerate(words):
        if w in sentence_words:
            bag[idx] = 1
    return bag
