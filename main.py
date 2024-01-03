import re
import multiprocessing
from collections import Counter
from nltk.tokenize import TreebankWordTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from thefuzz import process
import argparse
from tqdm import tqdm
import nltk
import spacy
#loading the english language small model of spacy
en = spacy.load('en_core_web_sm')
sw_spacy = en.Defaults.stop_words

# Download required NLTK data
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    tokenizer = TreebankWordTokenizer()
    tokens = tokenizer.tokenize(text)
    lemmatizer = WordNetLemmatizer()
    lemmas = [lemmatizer.lemmatize(token) for token in tokens]
    return tokens

def fuzzy_match(args):
    word, unique_words, word_counts, threshold = args
    matches = process.extractBests(word, unique_words, score_cutoff=threshold)
    total_count = sum(word_counts[match] for match, score in matches) + word_counts[word]
    return word, total_count

def get_fuzzy_common_words(words, threshold=94, top_n=50):
    word_counts = Counter(words)
    unique_words = list(word_counts.keys())

    # Prepare arguments for multiprocessing
    args = [(word, unique_words, word_counts, threshold) for word in unique_words]

    with multiprocessing.Pool() as pool:
        results = list(tqdm(pool.imap(fuzzy_match, args),
                            total=len(unique_words),
                            desc="Processing words"))

    # Flatten results and sort
    common_words = sorted(results, key=lambda x: x[1], reverse=True)
    common_words = filter_common_english_words(common_words)
    return common_words[:top_n]

def filter_common_english_words(common_words):
    common_english_words = set(stopwords.words('english'))
    common_english_words.update(sw_spacy)
    return [word for word in common_words if word[0] not in common_english_words]

def main():
    parser = argparse.ArgumentParser("fuzzy_match")
    parser.add_argument("--file_path", type=str, default="2023.txt")
    parser.add_argument("--threshold", type=int, default=94)
    parser.add_argument("--top_n", type=int, default=50)
    args = parser.parse_args()
    file_path = args.file_path
    text = read_file(file_path)
    words = preprocess_text(text)
    common_words = get_fuzzy_common_words(words, threshold=args.threshold, top_n=args.top_n)
    
    for (word, count), rank in zip(common_words, range(1, args.top_n + 1)):
        print(f"{rank}. {word} ({count})")

if __name__ == '__main__':
    main()

