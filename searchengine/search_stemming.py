# search_stemming.py

import string
import nltk
from nltk.tokenize import TreebankWordTokenizer
from nltk.stem.porter import PorterStemmer

# Download necessary data (only first time)
nltk.download('punkt')

# Sample documents
docs = [
    '''About us. We deliver Artificial Intelligence & Machine Learning solutions to solve business challenges.''',
    '''Contact information. Email [martin davtyan at filament dot ai] if you have any questions''',
    '''Filament Chat. A framework for building and maintaining a scalable chatbot capability'''
]

# Query (user input)
query = "contacts"

# Initialize tokenizer and stemmer
tokenizer = TreebankWordTokenizer()
stemmer = PorterStemmer()

# Remove punctuation
REMOVE_PUNCTUATION_TABLE = str.maketrans({x: None for x in string.punctuation})

def tokenize_and_stem(text):
    """Tokenize, lowercase, and stem a given text."""
    tokens = tokenizer.tokenize(text.translate(REMOVE_PUNCTUATION_TABLE))
    stems = [stemmer.stem(token.lower()) for token in tokens]
    return stems

# Tokenize & stem documents
doc_stems = [tokenize_and_stem(doc) for doc in docs]

# Tokenize & stem query
query_stems = tokenize_and_stem(query)

print(f"Query stems: {query_stems}\n")

# Compare overlap between query and each document
for i, stems in enumerate(doc_stems):
    overlap = len(set(query_stems) & set(stems))
    print(f"Doc {i+1} overlap score: {overlap} | {docs[i][:60]}...")
