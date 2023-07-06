from flask import Flask, request, jsonify
import numpy as np
import string
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

def preprocess_text(text):
    # Remove acentos e transforma em lowercase
    text = text.lower().translate(str.maketrans('', '', string.punctuation))
    return text

def calculate_similarity(input_sentence, reference_sentences):
    input_sentence = preprocess_text(input_sentence)

    vectorizer = CountVectorizer()
    input_vector = vectorizer.fit_transform([input_sentence])
    reference_vectors = vectorizer.transform(reference_sentences)

    similarities = cosine_similarity(input_vector, reference_vectors)[0]

    return similarities

def get_best_similarity(input_sentence):
    with open('reference_sentences.txt', 'r') as file:
        reference_sentences = [line.strip() for line in file]

    similarities = calculate_similarity(input_sentence, reference_sentences)

    similarity_scores = [(sentence, score) for sentence, score in zip(reference_sentences, similarities)]

    return similarity_scores

@app.route('/api/similarity', methods=['POST'])
def calculate_similarity_endpoint():
    input_sentence = request.json['input_sentence']

    similarity_scores = get_best_similarity(input_sentence)

    response = {
        'similarity_scores': similarity_scores
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)