import pandas as pd
import numpy as np
import string
import joblib

# from sklearn.datasets import make_blobs
from sklearn import datasets, preprocessing
from matplotlib import pyplot

def make_features(**kwargs):
    scaler = preprocessing.MinMaxScaler(feature_range=(0.01, 0.99))
    X, y = datasets.make_blobs(
        n_samples=kwargs.get('n_samples', 9),
        n_features=kwargs.get('n_features', 26),
        centers=kwargs.get('centers', 2),
        random_state=kwargs.get('random_state', 42),
    )
    # print(X.min(), X.max())
    X = scaler.fit_transform(X)
    # print(X.min(), X.max())
    for i in range(X.shape[0]):
        X[i, i] = np.nan
    # print(X.min(), X.max())
    X.shape
    return X, y

def make_scores_matrix(**kwargs):
    X, y = make_features(**kwargs)
    scores = pd.DataFrame(X, index=list(string.ascii_uppercase[:X.shape[0]]), columns=list(string.ascii_uppercase[:X.shape[1]]))
    return scores

def make_ranks_matrix(**kwargs):
    scores = make_scores_matrix(**kwargs)
    ranks = scores.rank(axis=1, ascending=False)
    return ranks

def make_fullranks_table(**kwargs):
    scores = make_scores_matrix(**kwargs)
    ranks = make_ranks_matrix(**kwargs)
    fullranks = pd.merge(
        left=scores.stack().to_frame(name='Score'),
        right=ranks.stack().to_frame(name='rank'),
        left_index=True,
        right_index=True
    ).reset_index().rename(columns={'level_0': 'seed', 'level_1': 'NodeNames'}).dropna(how='any')
    return fullranks

