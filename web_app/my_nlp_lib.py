# Process_string, build_text_vectorizer modified from NLP rescources
# from Galvanize.
# Original Plot_embedding modefied from a script by Adam Richards.

from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from string import punctuation, printable
import spacy
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly as plotly
from mpl_toolkits.mplot3d import Axes3D  # required for matplotlib 3d proj

nlp = spacy.load('en')


def process_string(doc, stoplist=None):
    '''
    Processes a string (doc) by removing stopwords, removing punctuation,
    and removing unprintable characters. Then running the string through spaCy
    and keeping only certain parts of speech.

    parameters:
    ----------------------
    doc(str) -> string to be transformed
    stoplist(list) -> additional words you can add to the stoplist

    returns:
    ----------------------
    (str) -> A processed and cleaned string
    '''
    STOPLIST = set(list(ENGLISH_STOP_WORDS) +
                   ["n't", "'s", "'m", "ca", "'", "'re", "-pron-", "say",
                    "tell", 's', 'skill', 'work', 'ability', 'data', 'provide',
                    'team', 'use', 'benefit', 'eligibility', 'hire',
                    'applicant', 'law', 'protect', 'employment',
                    'a_data_scientist', 'deloitte', 'require', 'cybercoders',
                    'experience', 'federal', 'verification', 'u',
                    'your_right_to_work_in', 'authorize', 'compliance',
                    'the_united_states', 'document', 'proud', 'status',
                    'disability', 'opportunity', 'veteran', 'origin',
                    'religion', 'race', 'color', 'national', 'sex', 'identity',
                    'company', 'regard', 'qualified', 'receive', 'career',
                    'consideration', 'gender', 'health', 'apply', 'info',
                    'available', 'contract', 'sponsorship', 'type', 'position',
                    'time', 'corp', 'www', 'date', 'performance', 'bonus',
                    'distribute', 'preferably', 'report', 'site', 'place',
                    'big', 'real', 'grow', 'com', 'help', 'world', 'look',
                    'people', 'great', 'make', 'product', 'build', 'employee',
                    'join', 'want', 'impact', 'good', 'pay', 'new', 'offer',
                    'ne', 'office', 'client', 'll', 'solution', 'job',
                    'professional', 'business', 'right', 'value', 'industry',
                    'deliver', 'customer', 'environment', 'growth', 'just',
                    'culture', 'high', 'know', 'service', 'firm', 'person',
                    'today', 'way', 'bring', 'start', 'partner', 'change',
                    'competitive', 'staffing', 'talent', 'passion', 'base',
                    'edge', 'think', 'magazine', 'anthem_inc', 'america',
                    'prefer', 'fortune', 'top_50_company', 'diversityinc',
                    'admired', 'insurer', 'care', 'rank', 'anthem',
                    'combination', 'output', 'diversity', 'unit', 'education',
                    'this_is', 'determine', 'action', 'medicare',
                    'termination', 'administer', 'support', 'il', 'location',
                    'tuition', 'addition', 'serve', 'recruit', 'transfer',
                    'personnel', 'accordance', 'address', 'member',
                    'accomplish', 'chicago', 'title', 'training', 'powerful',
                    'disclaimer', 'wells', 'fargo', 'contingent', 'candidate',
                    'successfully', 'complete', 'criminal', 'background',
                    'check', 'wells', 'fargo', 'consider', 'candidate',
                    'criminal', 'history', 'manner', 'consistent',
                    'requirement', 'applicable', 'local', 'state', 'include',
                    'section', 'deposit', 'insurance', 'act', 'relevant',
                    'military', 'consider', 'transitioning', 'man', 'woman',
                    'wells', 'fargo', 'affirmative', 'equal', 'employer',
                    'minority', 'female', 'disabled', 'sexual', 'orientation',
                    'drive', 'day', 'fast', 'able', 'role', 'act', 'year',
                    'hand', 'legally' 'United' 'States'
                    ])
    if stoplist is None:
        STOPLIST = STOPLIST
    else:
        STOPLIST = set(stoplist + list(STOPLIST))

    PUNCT_DICT = {ord(punc):
                  None for punc in punctuation if punc not in ['_', '*']}
    # remove punctuation
    doc = doc.translate(PUNCT_DICT)

    # remove unicode
    clean_doc = "".join([char for char in doc if char in printable])
    # run through spacy
    doc = nlp(clean_doc)

    # specify the parts of speech to keep
    pos_lst = ['ADJ', 'ADV', 'NOUN', 'PROPN', 'VERB']
    #     pos_lst = ['NOUN', 'PROPN']
    tokens = [token.lemma_.lower().replace(' ', '_')
              for token in doc if token.pos_ in pos_lst]

    # remove stopWords
    no_stopwords_tokens = [token for token in tokens if token not in STOPLIST]

    return ' '.join(w for w in no_stopwords_tokens)


def build_text_vectorizer(contents, use_tfidf=True, max_features=None):
    '''
    Builds and returns a callable vectorizer that can be used to transform text
    into a vector, also returns an orderlist with the word index equal to the
    position in the list.

    parameters:
    ----------------------
    contents(list) -> a list of strings to be transformed
    use_tfidf(bool) -> If true it will use tf-idf if false it will use a
        standard count vectorizer
    max_features(bool) -> the max features for the vectorizer

    returns:
    ----------------------
    vocabulary(list) -> A list of all the vocabulary Words
    vectorizer_model (sklearn class) -> a vectorizer model that can be applied
    '''
    Vectorizer = TfidfVectorizer if use_tfidf else CountVectorizer

    vectorizer_model = Vectorizer(max_features=max_features)
    vectorizer_model.fit(contents)
    vocabulary = np.array(vectorizer_model.get_feature_names())

    return vocabulary, vectorizer_model


def plot_embedding(X, y, title=None):
    # This function modified from one provided by Adam Richards.
    """
    Creates a pyplot object showing digits projected onto 2-dimensional
    feature space. PCA should be performed on the feature matrix before
    passing it to plot_embedding.

    parameters:
    --------------------------------
    X : decomposed feature matrix
    y : target labels (digits)
    title : title for plot if desired

    returns:
    --------------------------------
    none
    """
    x_min, x_max = np.min(X, 0), np.max(X, 0)
    X = (X - x_min) / (x_max - x_min)

    plt.figure(figsize=(5, 3), dpi=250)
    ax = plt.subplot(111)
    ax.axis('off')
    ax.patch.set_visible(False)
    for i in range(X.shape[0]):
        plt.text(X[i, 0], X[i, 1], str(int(y[i])),
                 color=plt.cm.Set1(int(y[i])),
                 fontdict={'weight': 'bold', 'size': 6})
        plt.xticks([]), plt.yticks([])
    plt.ylim([-0.1, 1.1])
    plt.xlim([-0.1, 1.1])

    if title is not None:
        plt.title(title, fontsize=16)


def plot_embedding3d(X, y, title=None):
    # This function modified from one provided by Adam Richards and converted
    # to 3d.
    """
    Creates a pyplot object showing digits projected onto 3-dimensional
    feature space. PCA should be performed on the feature matrix before
    passing it to plot_embedding.

    parameters:
    --------------------------------
    X : decomposed feature matrix
    y : target labels (digits)
    title : title for plot if desired

    returns:
    --------------------------------
    none
    """
    x_min, x_max = np.min(X, 0), np.max(X, 0)
    X = (X - x_min) / (x_max - x_min)

    fig = plt.figure(figsize=(5, 3), dpi=250)
    ax = fig.add_subplot(111, projection='3d')
    # ax.axis('off')
    ax.patch.set_visible(False)
    ax.set_zlim(-0.1, 0.8)
    for i in range(X.shape[0]):
        ax.text(X[i, 0], X[i, 1], X[i, 2], str(int(y[i])),
                color=plt.cm.Set1(int(y[i])),
                fontdict={'weight': 'bold', 'size': 6})

        # ax.xticks([]), ax.yticks([]), ax.zticks([])
    plt.ylim([0.35, 1])
    plt.xlim([-0.1, 0.8])
    # plt.zlim([-0.1, 1.1])

    if title is not None:
        plt.title(title, fontsize=16)


def plot_embedding3dplotly(X, y, filename='plot3d.html'):
    '''
    Does the same thing as plot_embedding3d but in plotly. See documentation
    for plot_embedding3d.
    '''
    traces = []
    for i in range(X.shape[0]):
        trace = go.Scatter3d(
            x=[X[i, 0]],
            y=[X[i, 1]],
            z=[X[i, 2]],
            text=[y[i]],
            textposition='bottom',
            mode='marker+text',
            textfont=dict(
                family='sans serif',
                size=18,
                color='rgba' + str(plt.cm.tab10(int(y[i])))
                # color='rgba' + str(plt.cm.Set1(int(y[i]))) #No Idea why 4 and
                # 5 do not color using Set1
            )
        )
        traces.append(trace)
    data = traces
    layout = go.Layout(
        showlegend=False,
        scene=dict(
            xaxis=dict(
                autorange=True,
                showgrid=False,
                zeroline=False,
                showline=False,
                title='',
                ticks='',
                showticklabels=False
            ),
            yaxis=dict(
                autorange=True,
                showgrid=False,
                zeroline=False,
                showline=False,
                title='',
                ticks='',
                showticklabels=False
            ),
            zaxis=dict(
                autorange=True,
                showgrid=False,
                zeroline=False,
                showline=False,
                title='',
                ticks='',
                showticklabels=False
            ))
    )
    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename=filename)
