from AmazonReviewScraper import AmazonReviewScraper
from AmazonSentimentAnalyzer import AmazonSentimentAnalyzer

def main():
    reviews_url_1 = 'https://www.amazon.com/SAMSUNG-Smartphone-Unlocked-Android-Titanium/product-reviews/B0CMDM65JH'
    reviews_url_2 = 'https://www.amazon.com/Google-Pixel-Pro-Smartphone-Telephoto/product-reviews/B0BCQWYR2Z'
    
    # reviews_url = 'https://www.amazon.com/Legendary-Whitetails-Journeyman-Jacket-Tarmac/product-reviews/B013KW38RQ/'
    scraper_1 = AmazonReviewScraper(reviews_url_1)
    df_reviews_1 = scraper_1.scrape_reviews()
    print(df_reviews_1)
    df_reviews_1.to_csv('./results/reviews_1.csv', index=False)
    
    scraper_2 = AmazonReviewScraper(reviews_url_2)
    df_reviews_2 = scraper_2.scrape_reviews()
    print(df_reviews_2)
    df_reviews_2.to_csv('./results/reviews_2.csv', index=False)
    

    analyzer = AmazonSentimentAnalyzer('models/sentiment_analysis_model.h5', 'models/tokenizer.pickle')
    analyzer.analyze_sentiment('./results/reviews_1.csv', './results_checked/checked_reviews_1.csv')
    analyzer.analyze_sentiment('./results/reviews_2.csv', './results_checked/checked_reviews_2.csv')
    

if __name__ == "__main__":
    main()
