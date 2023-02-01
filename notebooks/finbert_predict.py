import pandas as pd
import numpy as np
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer


def load_tokenizer_and_model(dir_path):
    tokenizer = AutoTokenizer.from_pretrained(dir_path)
    trained_finbert = trained_finbert = AutoModelForSequenceClassification.from_pretrained(
        dir_path)
    return tokenizer, trained_finbert


def normalize_and_tokenize(text, tokenizer):
    text = text.lower()
    text_df = pd.DataFrame({"text": [text]})
    text_dataset = Dataset.from_pandas(text_df)
    def tokenize(x): return tokenizer(
        x["text"], padding="max_length", truncation=True)
    tokenized_text = text_dataset.shuffle(seed=42).map(tokenize, batched=True)
    return tokenized_text


def predict(text, dir_path):

    tokenizer, trained_finbert = load_tokenizer_and_model(dir_path)

    tokenized_text = normalize_and_tokenize(text, tokenizer)

    labels = {1: 'negative', 2: 'neutral', 0: 'positive'}
    trained_model = Trainer(trained_finbert,
                            tokenizer=tokenizer
                            )
    output = trained_model.predict(
        test_dataset=tokenized_text
    )
    prediction = np.argmax(output.predictions, axis=-1)[0]

    return labels[prediction]


if __name__ == "__main__":
    '''
        parameters to be populated
    '''
    text = "<input text to predict sentiments on>"
    dir_path = "<absolute path of the directory containing the finbert model>"

    try:
        sentiment = predict(text, dir_path)
        print(sentiment)
    except Exception as e:
        print(e)
