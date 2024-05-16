import pandas as pd

def check_csv(filename):
    # Read the CSV file
    df = pd.read_csv(filename)

    # Initialize counts for each sentiment
    sentiment_counts = {'Negative': 0, 'Neutral': 0, 'Positive': 0}

    # Iterate through the reviews
    for index, row in df.iterrows():
        if row['Stars'] > 3.0:
            sentiment = "Positive"
        elif row['Stars'] < 3.0:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
        sentiment_counts[sentiment] += 1
        
    print(f'Sentiment count based on stars in file: {filename}')    
    for sentiment, count in sentiment_counts.items():
        print(f"{sentiment}: {count}")
        
check_csv('./results/reviews_1.csv')
check_csv('./results/reviews_2.csv')
        