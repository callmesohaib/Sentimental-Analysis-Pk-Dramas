import pandas as pd
from transformers import pipeline
from tqdm import tqdm

# Load the sentiment analysis pipeline
print("Loading sentiment analysis model...")
sentiment_pipeline = pipeline("text-classification", model="finiteautomata/bertweet-base-sentiment-analysis")

# Function to get sentiment label
def get_sentiment(text):
    try:
        if pd.isna(text) or str(text).strip() == "":
            return "N"  
        
        
        result = sentiment_pipeline(text[:512])  # Truncate to model's max length
        label = result[0]['label']
        
        if label == 'POS':
            return "P"
        elif label == 'NEG':
            return "N"
        else:  # NEU
            return "M"  # Or you might want to use another code for neutral
    except Exception as e:
        print(f"Error processing text: {text}. Error: {str(e)}")
        return "E"

# Load your dataset
print("Loading dataset...")

dataset_path = r"A:\University\BSCS 6th sem\NLP\NLP\Dataset.csv"
df = pd.read_csv(dataset_path, encoding='utf-8-sig')

# Process English sentences and add sentiment labels
print("Analyzing sentiment for English sentences...")
tqdm.pandas()  # Enable progress bar for pandas apply
df['Sentiment(P/N)'] = df['English_Sentence_text'].progress_apply(get_sentiment)

# Save the labeled dataset
output_path = r"A:\University\BSCS 6th sem\NLP\NLP\Labeled_Dataset1.csv"
df.to_csv(output_path, index=False, encoding='utf-8-sig')
print(f"\n✅ Sentiment analysis complete! Labeled dataset saved to: {output_path}")