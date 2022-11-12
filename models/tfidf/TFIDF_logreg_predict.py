import pickle
import pandas as pd
import nltk
import re
from nltk.stem import WordNetLemmatizer

nltk.download("stopwords")
nltk.download('wordnet')
nltk.download('omw-1.4')

stopwords = nltk.corpus.stopwords.words('english')
lemmatizer = WordNetLemmatizer()

def process_test_data(df):
    df = df['Title']
    test_X = []

    for i in range(0, len(df)):
        review = re.sub('[^a-zA-Z]', ' ', df.iloc[i])
        review = review.lower()
        review = review.split()
        review = [lemmatizer.lemmatize(word) for word in review if not word in set(stopwords)]
        review = ' '.join(review)
        test_X.append(review)
    
    return test_X



def predict(df, model_path, tfidf_path):
    model = pickle.load(open(model_path, 'rb'))
    tfidf_vectorizer = pickle.load(open(tfidf_path, 'rb'))

    features = process_test_data(df)
    features = tfidf_vectorizer.transform(features)

    y_pred = model.predict(features)
    df['label'] = y_pred
    return df

if __name__ == "__main__":

    model_path = "tfidf_logistic_regression.sav"
    tfidf_path = "tfidf.pkl"

    df = pd.read_csv('labelled_marketaux_news_combined_2022-10-15.csv')

    df = df[0:100]

    print(predict(df, model_path, tfidf_path))
