from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer

def extract_common_questions(file_path):
    """Finds the most frequently asked words in extracted questions."""
    with open(file_path, "r", encoding="utf-8") as f:
        emails = f.readlines()

    vectorizer = CountVectorizer(stop_words="english")
    X = vectorizer.fit_transform(emails)
    word_freq = Counter(vectorizer.get_feature_names_out())

    return word_freq.most_common(10)

# Run the FAQ Extraction
common_questions = extract_common_questions("extracted_questions.txt")

print("\n🔹 Most Common Student Questions:\n")
for word, count in common_questions:
    print(f"{word}: {count} times")
