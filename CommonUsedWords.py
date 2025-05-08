import pandas as pd
from collections import Counter
import re

# Load the dataset (update the file path as needed)
df = pd.read_excel("Dataset_Final.xlsx")

# Combine all Urdu sentences into a single string
all_urdu_text = " ".join(df["Urdu_Sentence_text"].astype(str))

# Clean the text: remove Urdu punctuation and normalize spaces
cleaned_text = re.sub(r"[۔،؛؟!٭ء]", " ", all_urdu_text)
cleaned_text = re.sub(r"\s+", " ", cleaned_text).strip()

# Tokenize the cleaned text
words = cleaned_text.split()

# Count word frequencies
word_freq = Counter(words)

# Display the 10 most common words
top_words = word_freq.most_common(3)
for word, freq in top_words:
    print(f"{word} — {freq} times")
