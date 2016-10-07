# -*- coding: utf-8 -*-

import pandas as pd
from pandas import DataFrame, Series
import os
import jieba
from sklearn.feature_extraction.text import CountVectorizer, \
                        TfidfVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.cross_validation import train_test_split
import numpy as np


def main():
    dirname = "./data"
    thumb_up = pd.read_csv(os.path.join(dirname, u'好评.csv'), 
                           index_col=0, usecols=[0, 3, 5],
                           converters = {'score': lambda x: 1,
                                         'comment': lambda x : " ".join(jieba.cut(x))})
    thumb_down = pd.read_csv(os.path.join(dirname, u'差评.csv'), 
                           index_col=0, usecols=[0, 3, 5],
                           converters = {'score': lambda x : -1,
                                         'comment': lambda x : " ".join(jieba.cut(x))})
    thumb_data = pd.concat([thumb_up, thumb_down])
    
    X_train, X_test, Y_train, Y_test = train_test_split(thumb_data['comment'], 
                                                        thumb_data['score'])
    vectorizer = CountVectorizer()
    transformer = TfidfTransformer()
    tf_idf = transformer.fit_transform(vectorizer.fit_transform(X_train))

    clf = MultinomialNB()
    clf.fit(tf_idf.toarray(), Y_train)
    print clf.score(tf_idf.toarray(), Y_train)
    print clf.score(transformer.transform(vectorizer.transform(X_test)).toarray(),
                    Y_test)



if __name__ == "__main__":
    main()
