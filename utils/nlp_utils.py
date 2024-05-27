import re
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx

def generate_key_points(text):
    sentences = sent_tokenize(text)
    clean_sentences = [re.sub(r"[^a-zA-Z\s]", "", sentence) for sentence in sentences]

    vectorizer = CountVectorizer(stop_words='english')
    sentence_vectors = vectorizer.fit_transform(clean_sentences)

    similarity_matrix = cosine_similarity(sentence_vectors, sentence_vectors)

    graph = nx.from_numpy_array(similarity_matrix)
    scores = nx.pagerank(graph)

    ranked_sentences = sorted(((scores[i], sentence) for i, sentence in enumerate(sentences)), reverse=True)

    num_key_points = min(10, len(ranked_sentences))
    key_points = [ranked_sentence[1].replace("Here is a concise summary of the text:", "") for _, ranked_sentence in enumerate(ranked_sentences) if _ < num_key_points]
    return key_points

