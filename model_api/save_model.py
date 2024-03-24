from transformers import AutoTokenizer, AutoConfig, AutoModelForSequenceClassification

dir_path = "./models/FinBert_v1.2"

labels = {1: 'negative', 2: 'neutral', 0: 'positive'}
pred_labels = {1: -1.0, 2: 0.0, 0: 1.0}


tokenizer = AutoTokenizer.from_pretrained(dir_path)
config = AutoConfig.from_pretrained(dir_path)

tokenizer.save_pretrained('./models/tokenizer')
config.save_pretrained('Y./models/tokenizer')

tokenizer = AutoTokenizer.from_pretrained('./models/tokenizer')


trained_finbert = AutoModelForSequenceClassification.from_pretrained(
        dir_path, local_files_only=True)

trained_finbert.save_pretrained("./models/model")

trained_finbert = AutoModelForSequenceClassification.from_pretrained(
        './models/model', local_files_only=True)