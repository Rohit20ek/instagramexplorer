import string
import nltk
from nltk.tokenize import TreebankWordTokenizer
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Download necessary data (only first time)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

class SearchEngine:
    def __init__(self):
        self.docs = [
            '''About us. We deliver Artificial Intelligence & Machine Learning solutions to solve business challenges.''',
            '''Contact information. Email [martin davtyan at filament dot ai] if you have any questions''',
            '''Filament Chat. A framework for building and maintaining a scalable chatbot capability'''
        ]
        self.tokenizer = TreebankWordTokenizer()
        self.stemmer = PorterStemmer()
        self.remove_punctuation_table = str.maketrans({x: None for x in string.punctuation})
        
        # Pre-compute for Stemming
        self.doc_stems = [self.tokenize_and_stem(doc) for doc in self.docs]
        
        # Pre-compute for BoW
        self.vectorizer = CountVectorizer(stop_words='english')
        self.X = self.vectorizer.fit_transform(self.docs)

    def tokenize_and_stem(self, text):
        """Tokenize, lowercase, and stem a given text."""
        tokens = self.tokenizer.tokenize(text.translate(self.remove_punctuation_table))
        stems = [self.stemmer.stem(token.lower()) for token in tokens]
        return stems

    def search_stemming(self, query):
        query_stems = self.tokenize_and_stem(query)
        results = []
        for i, stems in enumerate(self.doc_stems):
            overlap = len(set(query_stems) & set(stems))
            if overlap > 0:
                results.append({
                    "id": i + 1,
                    "content": self.docs[i],
                    "score": overlap
                })
        results.sort(key=lambda x: x['score'], reverse=True)
        return results

    def search_bow(self, query):
        query_vec = self.vectorizer.transform([query])
        # Calculate cosine similarity between query and all docs
        cosine_similarities = cosine_similarity(query_vec, self.X).flatten()
        results = []
        for i, score in enumerate(cosine_similarities):
            if score > 0:
                results.append({
                    "id": i + 1,
                    "content": self.docs[i],
                    "score": round(score, 4)
                })
        results.sort(key=lambda x: x['score'], reverse=True)
        return results

    def search_exact(self, query):
        # Simple exact match of tokens (case-insensitive)
        query_tokens = set(self.tokenizer.tokenize(query.lower().translate(self.remove_punctuation_table)))
        results = []
        for i, doc in enumerate(self.docs):
            doc_tokens = set(self.tokenizer.tokenize(doc.lower().translate(self.remove_punctuation_table)))
            overlap = len(query_tokens & doc_tokens)
            if overlap > 0:
                results.append({
                    "id": i + 1,
                    "content": self.docs[i],
                    "score": overlap
                })
        results.sort(key=lambda x: x['score'], reverse=True)
        return results

    def search(self, query, method='stemming'):
        if method == 'bow':
            return self.search_bow(query)
        elif method == 'exact':
            return self.search_exact(query)
        else:
            return self.search_stemming(query)

search_engine = SearchEngine()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('q', '')
    method = request.args.get('method', 'stemming')
    if not query:
        return jsonify([])
    results = search_engine.search(query, method)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
