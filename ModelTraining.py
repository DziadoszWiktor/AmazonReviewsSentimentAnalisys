# Import libraries
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Conv1D, GlobalMaxPooling1D, Dense, Dropout
import pickle5 as pickle


# Load the dataset
df = pd.read_csv('./datasets/AmazonReviews.csv')
print(df.head())
# df = df.dropna(subset=['Text'])


# Preprocess the dataset
df = df[['Score','Text']]
df['sentiment'] = df['Score'].apply(lambda x: 'positive' if x > 3 else 'negative' if x < 3 else 'neutral')
df = df[['Text', 'sentiment']]
df = df.sample(frac=1).reset_index(drop=True)


# Tokenize and pad the review sequences
tokenizer = Tokenizer(num_words=5000, oov_token='')
tokenizer.fit_on_texts(df['Text'])
word_index = tokenizer.word_index
sequences = tokenizer.texts_to_sequences(df['Text'])
padded_sequences = pad_sequences(sequences, maxlen=100, truncating='post')


# Convert the sentiment labels to one-hot encoding
sentiment_labels = pd.get_dummies(df['sentiment']).values


# Split the dataset into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(padded_sequences, sentiment_labels, test_size=0.2)


# Build the model
model = Sequential()
model.add(Embedding(5000, 100, input_length=100))
model.add(Conv1D(64, 5, activation='relu'))
model.add(GlobalMaxPooling1D())
model.add(Dense(32, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(3, activation='softmax'))
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])


# Train the model
model.fit(x_train, y_train, epochs=10, batch_size=32, validation_data=(x_test, y_test))

# Evaluate the model
y_pred = np.argmax(model.predict(x_test), axis=-1)
print("Accuracy:", accuracy_score(np.argmax(y_test, axis=-1), y_pred))


# Save the trained model
model.summary()
model.save('models/sentiment_analysis_model.h5')
with open('models/tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
    

    
