from AmazonReviewScraper import AmazonReviewScraper
from AmazonSentimentAnalyzer import AmazonSentimentAnalyzer

def main():
    
    reviews_url = ['https://www.amazon.com/DECKER-Nonstick-Reversible-Stainless-G48TD/product-reviews/B000063XH7', 'https://www.amazon.com/LtYioe-Colorful-Humidifier-Personal-Shut-Off/product-reviews/B08FBP26RL/']
    
    num = 1
    for url in reviews_url:
        scraper = AmazonReviewScraper(url)
        df_reviews = scraper.scrape_reviews()
        print(df_reviews)
        df_reviews.to_csv(f'./results/reviews_{num}.csv', index=False)
        analyzer = AmazonSentimentAnalyzer('models/sentiment_analysis_model.h5','models/tokenizer.pickle')
        analyzer.analyze_sentiment(f'./results/reviews_{num}.csv', f'./results_checked/checked_reviews_{num}.csv')
        num += 1

if __name__ == "__main__":
    main()
