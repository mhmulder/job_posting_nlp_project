from flask import Flask, request, render_template
import pickle
import my_nlp_lib as my_lib
from sklearn.decomposition import NMF
import numpy as np
np.random.seed(12345)


app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit')
def submit_func():
    return render_template('submit.html')

@app.route('/predict', methods = ["GET", "POST"])
def predict_func():

    with open('static/model.pkl', 'rb') as f:
       nlp_packages = pickle.load(f)
       vectorizer=nlp_packages[0]
       factorizer=nlp_packages[1]
       vocabulary=nlp_packages[2]

    #    working_corpus=nlp_packages[0]
    #    factorizer=nlp_packages[1]
    #    vocabulary=nlp_packages[2]
    #
    # vectorizer, vocabulary = my_lib.build_text_vectorizer(working_corpus,
    #                          use_tfidf=True,
    #                          max_features=2000
    print (type(vectorizer))


    X = request.form['words']
    clean_text = my_lib.process_string(X)

    text_word_mat = vectorizer.transform([clean_text])

    text_new_W = factorizer.transform(text_word_mat)
    new_label = text_new_W.argmax(axis=1)
    text_new_H = factorizer.components_

    DS_sorted_words = np.argsort(text_new_H[new_label[0]])[::-1][:100]

    DS_vocab = vocabulary[DS_sorted_words]
    my_set = set(clean_text.split(' '))

    missing_words = []

    for word in DS_vocab:
        if word not in my_set:
            missing_words.append(word)

    return render_template('predict.html', prediction = ' '.join(missing_words[0:50]))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8105, debug=True)
