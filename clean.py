import pandas as pd
import re

# Load dataset
input_path = r"A:\University\BSCS 6th sem\NLP\NLP\Labeled_Dataset.csv"
df = pd.read_csv(input_path, encoding='utf-8-sig')
print("Original dataset shape:", df.shape)

# 1. Remove neutral sentiment
df_filtered = df[df['Sentiment(P/N)'] != 'M'].copy()
print("After removing neutral:", df_filtered.shape)

# 2. Remove short sentences (<5 words)
def count_urdu_words(sentence):
    if pd.isna(sentence):
        return 0
    words = re.sub(r'[۔،؛؟!\s]+', ' ', str(sentence)).strip().split()
    return len(words)

df_filtered['word_count'] = df_filtered['Sentence_text'].apply(count_urdu_words)
df_filtered = df_filtered[df_filtered['word_count'] >= 5].drop(columns=['word_count'])
print("After removing short sentences:", df_filtered.shape)

# 3. Balance sentiments (max 20k each)
MAX_SAMPLES = 20000

# Split by sentiment
pos = df_filtered[df_filtered['Sentiment(P/N)'] == 'P']
neg = df_filtered[df_filtered['Sentiment(P/N)'] == 'N']

# Limit to 20k each (or available if less)
pos_limited = pos.head(min(len(pos), MAX_SAMPLES))
neg_limited = neg.head(min(len(neg), MAX_SAMPLES))

# Get extra negatives beyond 20k
neg_extra = neg.iloc[MAX_SAMPLES:] if len(neg) > MAX_SAMPLES else pd.DataFrame()

# Combine balanced dataset
df_balanced = pd.concat([pos_limited, neg_limited]).sample(frac=1).reset_index(drop=True)

# 4. Save results
# Balanced dataset
balanced_path = r"A:\University\BSCS 6th sem\NLP\NLP\Labeled_Dataset.csv"
df_balanced.to_csv(balanced_path, index=False, encoding='utf-8-sig')

# Extra negatives (if any)
if len(neg_extra) > 0:
    extra_path = r"A:\University\BSCS 6th sem\NLP\NLP\Extra_Instances.csv"
    neg_extra.to_csv(extra_path, index=False, encoding='utf-8-sig')

# 5. Print statistics
print("\nFinal Counts:")
print(f"Positive: {len(pos_limited)}")
print(f"Negative: {len(neg_limited)}")
if len(neg_extra) > 0:
    print(f"Extra negatives saved: {len(neg_extra)}")

print(f"\n✅ Balanced dataset saved to: {balanced_path}")
if len(neg_extra) > 0:
    print(f"✅ Extra negatives saved to: {extra_path}")

print("\nSample of balanced data:")
print(df_balanced[['Sentence_text', 'Sentiment(P/N)']].head())