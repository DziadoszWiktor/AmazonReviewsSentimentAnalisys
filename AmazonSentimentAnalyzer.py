import pandas as pd
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle5 as pickle

class AmazonSentimentAnalyzer:
    def __init__(self, model_path, tokenizer_path):
        self.model = load_model(model_path)
        with open(tokenizer_path, 'rb') as handle:
            self.tokenizer = pickle.load(handle)

    def predict_sentiment_batch(self, texts):
        text_sequences = self.tokenizer.texts_to_sequences(texts)
        text_sequences = pad_sequences(text_sequences, maxlen=1000)
        predicted_ratings = self.model.predict(text_sequences)
        sentiments = []
        for rating in predicted_ratings:
            if rating[0] > 0.6:
                sentiments.append('Negative')
            elif rating[0] < 0.4:
                sentiments.append('Positive')
            else:
                sentiments.append('Neutral')
        return sentiments
    
    

    def analyze_sentiment(self, input_csv, output_csv):
        df = pd.read_csv(input_csv)
        df['Sentiment'] = self.predict_sentiment_batch(df['Description'])
        
        sentiment_counts = df['Sentiment'].value_counts()
        sentiment_counts_dict = sentiment_counts.to_dict()
        print("Sentiment Counts:")
        for sentiment, count in sentiment_counts_dict.items():
            print(f"{sentiment}: {count}")
        
        df.to_csv(output_csv, index=False)
        
