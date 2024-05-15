import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import load_model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle5 as pickle

# Load the saved model and tokenizer
model = load_model('sentiment_analysis_model_3.h5')
with open('tokenizer3.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

# Load the new dataset
new_df = pd.read_csv('AmazonReviews.csv')  # Change 'new_data.csv' to your new dataset filename

# Preprocess the new dataset
new_df = new_df[['Text', 'Score']]
new_df['sentiment'] = new_df['Score'].apply(lambda x: 'positive' if x > 3 else 'negative' if x < 3 else 'neutral')
new_df = new_df[['Text', 'sentiment']]
new_df = new_df.dropna(subset=['Text'])
new_df = new_df[new_df['Text'].apply(lambda x: isinstance(x, str))]

# Tokenize and pad the review sequences for the new dataset
new_sequences = tokenizer.texts_to_sequences(new_df['Text'])
new_padded_sequences = pad_sequences(new_sequences, maxlen=100, truncating='post')

# Convert the sentiment labels to one-hot encoding for the new dataset
new_sentiment_labels = pd.get_dummies(new_df['sentiment']).values

# Split the dataset into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(new_padded_sequences, new_sentiment_labels, test_size=0.2)

# Create a new optimizer instance
optimizer = Adam()

# Compile the model with the new optimizer
model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

# Retrain the model
model.fit(x_train, y_train, epochs=5, batch_size=32, validation_data=(x_test, y_test))

# Save the updated model
model.save('models/sentiment_analysis_model_finetuned.h5')
