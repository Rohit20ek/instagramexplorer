# search_bow.py

from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

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
feature_names = vectorizer.get_feature_names_out()
print("\nFeature Names:\n", feature_names)

# ---------- MINI CHALLENGE SECTION BELOW ----------

print("\n" + "="*60)
print("Mini Challenge: Top 3 Words per Document\n" + "="*60)

# Convert sparse matrix to numpy array for easier manipulation
bow_matrix = X.toarray()

# For each document, find top 3 most frequent words
for i, row in enumerate(bow_matrix):
    top_indices = row.argsort()[-3:][::-1]  # indices of top 3 words
    top_words = [(feature_names[j], row[j]) for j in top_indices if row[j] > 0]
    print(f"\nDocument {i+1}:")
    for word, count in top_words:
        print(f"  {word}: {count}")

# ---------- BONUS: Represent a QUERY ----------

query = "chatbot ai"
query_vec = vectorizer.transform([query]).toarray()

print("\n" + "="*60)
print(f"Query: '{query}' Vector Representation:\n", query_vec)
