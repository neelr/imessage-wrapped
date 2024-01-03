import re
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')

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
    # Remove stopwords
    filtered_tokens = [word for word in tokens if word not in stopwords.words('english')]
    return filtered_tokens

def get_common_words(words, top_n=10):
    word_counts = Counter(words)
    return word_counts.most_common(top_n)

# Main execution
file_path = '2023.txt'
text = read_file(file_path)
words = preprocess_text(text)
common_words = get_common_words(words, top_n=100)

for word, count in common_words:
    print(f"'{word}': {count}")

