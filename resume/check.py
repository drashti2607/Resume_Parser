from turtle import back
from . import nltk_model


def skills_check(customfile):

    res = nltk_model.resumeParser(customfile)
    details = res.get_person_info()
    skilss = details['skills']
    # print(skilss)
    
    terms = {'Machine Learning': ['machine learning', 'ml', 'linear regression', 'logistic regression', "clustering",
                                  'random forest', 'xgboost', 'svm', 'knn', 'cluster', 'pca', 'decision tree', 'ensemble models',
                                  'boltzman machine', 'numpy', 'pandas', 'seaborn', 'matplotlib', 'scipy', 'sklearn', 'scikitlearn',
                                  'scikit learn'],
            
            'Deep Learning': ['deep learning', 'dl', 'neural network', 'keras', 'tensorflow', 'tensor flow', 'pytorch',
                               'theano', 'cnn', 'ann', 'rnn', 'object detection', 'convolutional neural network',
                               'recurrent neural network', 'artificial neural network', 'yolo', 'gpu', 'lstm', 'gan', 'opencv'],

             'Natural Language Processing ': ['natural language processing', 'nlp', 'topic modeling', 'lda', 'name entity recognition', 'pos    tagging', 'word2vec', 'word embedding', 'lsi', 'spacy', 'nltk', 'gensim', 'nmf', 'doc2vec', 'cbow', 'bag of words', 'skip grams', 'bert', 'sentimental analysis','chat bot ', 'voice bot'],

             "Statitcs": ['statictical models', 'statictical modeling', 'probability', 'normal distruibution', 'poisson distribution',
                          'survival models', 'hypothesis testing', 'bayesian inference', 'factor analysis', 'forecasting', 'markov chain', 'monte carlo'],

             'Front End': [' html', 'html5', 'css', 'css3', 'javascript', 'js', 'react', 'react js', 'node js', 'angular', 'bootstrap', 'dom manipulation',
                           'json', 'ajax', 'mysql', 'monogodb'],

             'Back End': ['java',  'php', 'expressjs', 'djnago', 'nodejs', 'spring', 'github', 'gitlab', 'aws', 'cloud computing', 'git', 'database',
                          '.net', 'sql', 'haskell', 'clojure', 'flask', 'ruby', 'spring boot', 'apis', 'api'],

             'Data analytics': ['analytics', 'api', 'aws', 'big data', 'busines intelligence', 'clustering', 
                                'data', 'database', 'data mining', 'hadoop',
                                'hypothesis test', 'internet', 'nosql', 
                                'predictive',  'r', 'sql', 'tableau', 'text mining',
                                'visualuzation'],

             }

    
    # Initializie score counters for each area
    nlp = []
    ml = []
    dl = []
    stats = []
    frontend = []
    data = []
    backend = []

    # Create an empty list where the scores will be stored
    scores = dict()

    # text =  ['R', 'Keras', 'Pandas', 'Nlp', 'Eda', 'Ai', 'Numpy', 'Matplotlib', 'Sql', 'Python', 'Natural language processing', 'Deep learning', 'Seaborn', 'Ml']
    # text = [i.lower() for i in text]
    # Obtain the scores for each area

    text = details['skills']
    text = [i.lower() for i in text]

    for area in terms.keys():

        if area == 'Natural Language Processing':
            for word in terms[area]:
                if word in text:
                   nlp.append(word)
            scores[area] = len(nlp)

        elif area == 'Machine Learning':
            for word in terms[area]:
                if word in text:
                    ml.append(word)
            scores[area] = len(ml)

        elif area == 'Deep Learning':
            for word in terms[area]:
                if word in text:
                    dl.append(word)
            scores[area] = len(dl)

        elif area == 'Statitcs':
            for word in terms[area]:
                if word in text:
                    stats.append(word)
            scores[area] = len(stats)

        elif area == 'Front End':
            for word in terms[area]:
                if word in text:
                    frontend.append(word)
            scores[area] = len(frontend)

        elif area == 'Back End':
            for word in terms[area]:
                if word in text:
                    backend.append(word)
            scores[area] = len(backend)

        elif area == 'Data analytics':
            for word in terms[area]:
                if word in text:
                    data.append(word)
            scores[area] = len(data)

    maxval = max(scores, key=scores.get)
    ans = []
    count = scores[maxval]

    for k, v in scores.items():
        if v == count:
            ans.append(k)

    print(ans)

    return ans
