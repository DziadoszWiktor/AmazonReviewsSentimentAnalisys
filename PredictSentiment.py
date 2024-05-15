import numpy as np
import pandas as pd
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle5 as pickle
import keras

# Load the model and tokenizer
model = keras.models.load_model('models/sentiment_analysis_model.h5')
with open('models/tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

# Function to predict sentiment for a batch of texts
def predict_sentiment_batch(texts):
    # Tokenize and pad the input texts
    text_sequences = tokenizer.texts_to_sequences(texts)
    text_sequences = pad_sequences(text_sequences, maxlen=10000)

    # Make predictions using the trained model
    predicted_ratings = model.predict(text_sequences)
    sentiments = np.argmax(predicted_ratings, axis=1)

    return ['Negative' if sentiment == 0 else 'Neutral' if sentiment == 1 else 'Positive' for sentiment in sentiments]

# Function to process CSV file
def process_csv(filename, reviews_with_sentiment):
    # Read the CSV file
    df = pd.read_csv(filename)

    # Pull all texts into one batch
    all_texts = df['Description'].tolist()

    # Predict sentiment for all texts
    sentiments = predict_sentiment_batch(all_texts)
   
    # Add sentiment predictions to the DataFrame
    df['sentiment'] = sentiments

    # Count sentiments
    sentiment_counts = {'Negative': sentiments.count('Negative'), 'Neutral': sentiments.count('Neutral'), 'Positive': sentiments.count('Positive')}

    # Print the counts
    for sentiment, count in sentiment_counts.items():
        print(f"{sentiment}: {count}")
        
    # Save the DataFrame to a new CSV file
    df.to_csv(reviews_with_sentiment, index=False)

process_csv('reviews.csv', 'results/reviews_with_sentiment.csv')

