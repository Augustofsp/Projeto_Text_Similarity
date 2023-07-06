from flask import Flask, request, jsonify
import numpy as np
import string
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

glove_embeddings = {}

with open('glove.6B.50d.txt', 'r', encoding='utf8') as f:
    for line in f:
        values = line.split()
        word = values[0]
        embedding = np.asarray(values[1:], dtype='float32')
        glove_embeddings[word] = embedding

def calculate_average_embedding(phrase):
    words = phrase.split()
    phrase_embedding = np.mean([glove_embeddings[word] for word in words if word in glove_embeddings], axis=0)
    return phrase_embedding.tolist()

def calculate_similarity(input_phrase):
    with open('reference_sentences.txt', 'r') as file:
        reference_sentences = [line.strip() for line in file]

    input_embedding = calculate_average_embedding(input_phrase)

    similarities = []
    for sentence in reference_sentences:
        sentence_embedding = calculate_average_embedding(sentence)
        similarity = cosine_similarity([input_embedding], [sentence_embedding])[0][0]
        similarities.append(similarity)

    return reference_sentences, similarities

app = Flask(__name__)

@app.route('/api/similarity', methods=['POST'])
def get_similarity():
    data = request.get_json()
    input_sentence = data['input_sentence']

    reference_sentences, similarities = calculate_similarity(input_sentence)

    response = {
        'reference_sentences': reference_sentences,
        'similarities': similarities
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run()