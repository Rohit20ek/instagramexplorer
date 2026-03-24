import string
import nltk
from nltk.tokenize import TreebankWordTokenizer

# download required data (only first time)
nltk.download('punkt')

# Sample documents
docs = [
    '''About us. We deliver Artificial Intelligence & Machine Learning solutions to solve business challenges.''',
    '''Contact information. Email [martin davtyan at filament dot ai] if you have any questions''',
    '''Filament Chat. A framework for building and maintaining a scalable chatbot capability'''
]

# Initialize tokenizer
tokenizer = TreebankWordTokenizer()

# Remove punctuation
REMOVE_PUNCTUATION_TABLE = str.maketrans({x: None for x in string.punctuation})

# Tokenize each document
for i, doc in enumerate(docs):
    tokens = tokenizer.tokenize(doc.translate(REMOVE_PUNCTUATION_TABLE))
    print(f"Document {i+1} tokens:\n", tokens, "\n")