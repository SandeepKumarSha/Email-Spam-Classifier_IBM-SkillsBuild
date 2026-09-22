from flask import Flask, render_template, request
import pickle
import nltk
import string

from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from nltk.stem.porter import PorterStemmer

app = Flask(__name__)

ps = PorterStemmer()

# Load model and vectorizer
tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
model = pickle.load(open('model.pkl', 'rb'))


def transform_text(text):
    text = text.lower()
    text = text.split()

    y = []

    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in ENGLISH_STOP_WORDS and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)


@app.route('/', methods=['GET', 'POST'])
def home():
    prediction = None
    confidence = None

    if request.method == 'POST':
        message = request.form['message']

        transformed = transform_text(message)
        vector = tfidf.transform([transformed])
        result = model.predict(vector)[0]

        prediction = "Spam" if result == 1 else "Not Spam"

        if hasattr(model, 'predict_proba'):
            try:
                proba = model.predict_proba(vector)[0]
                confidence = round(proba[result] * 100, 1)
            except Exception:
                confidence = None

    return render_template('index.html', prediction=prediction, confidence=confidence)


if __name__ == '__main__':
    app.run(debug=True)