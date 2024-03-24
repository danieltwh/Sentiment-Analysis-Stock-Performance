import tensorflow as tf

def load_model(model_path):
    loaded_model = tf.saved_model.load(model_path)
    return loaded_model

def predict(text, model):
    text = [text.lower()]
    bert_result = model(text)
    bert_res_class = (tf.argmax(bert_result, axis=1)[0]).numpy()
    labels = {1: 'negative', 2: 'neutral', 0: 'positive'}
    return labels[bert_res_class]

if __name__ == '__main__':
    text = "Media Alert: Rambus to Present at 25th Annual Needham Virtual Growth Conference"
    dir_path = "./models/FinBert_v1.2"

    try:
        model = load_model(dir_path)
        sentiment = predict(text, model)
        print(sentiment)
    except Exception as e:
        print(e)
