# search_bow.py

from sklearn.feature_extraction.text import CountVectorizer

# Sample documents
docs = [
    '''About us. We deliver Artificial Intelligence & Machine Learning solutions to solve business challenges.''',
    '''Contact information. Email [martin davtyan at filament dot ai] if you have any questions''',
    '''Filament Chat. A framework for building and maintaining a scalable chatbot capability'''
]

# Initialize CountVectorizer (it tokenizes automatically)
vectorizer = CountVectorizer(stop_words='english')

# Learn vocabulary and transform documents into count vectors
X = vectorizer.fit_transform(docs)

# Show the vocabulary
print("Vocabulary:\n", vectorizer.vocabulary_, "\n")

# Show the Bag of Words matrix
print("BoW Matrix (Document-Term Counts):\n")
print(X.toarray())

# Show feature names (words)
print("\nFeature Names:\n", vectorizer.get_feature_names_out())
