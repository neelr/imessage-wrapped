import re
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from fuzzywuzzy import process
import nltk

# Download required NLTK data
nltk.download('punkt')
nltk.download('wordnet')

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove non-alphabetic characters
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Tokenize
    tokens = word_tokenize(text)
    # Lemmatize
    lemmatizer = WordNetLemmatizer()
    lemmas = [lemmatizer.lemmatize(token) for token in tokens]
    return lemmas

def get_fuzzy_common_words(words, threshold=90, top_n=10):
    word_counts = Counter(words)
    unique_words = list(word_counts.keys())
    common_words = []

    while unique_words:
        word = unique_words.pop()
        matches = process.extractBests(word, unique_words, score_cutoff=threshold)
        total_count = sum(word_counts[match] for match, score in matches) + word_counts[word]
        common_words.append((word, total_count))

        # Remove matched words from unique_words
        for match, score in matches:
            unique_words.remove(match)

    # Sort by frequency
    common_words.sort(key=lambda x: x[1], reverse=True)
    return common_words[:top_n]

# Main execution
file_path = '2023.txt'
text = read_file(file_path)
words = preprocess_text(text)
common_words = get_fuzzy_common_words(words)

for word, count in common_words[:3]:
    print(f"'{word}': {count}")

