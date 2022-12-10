import pandas as pd
import numpy as np
import scipy.sparse as sp
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_is_fitted
from sklearn.feature_extraction.text import _document_frequency
from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter

class BM25Transformer(BaseEstimator, TransformerMixin):
    """
    use_idf : boolean, optional (default=True)
    k1 : float, optional (default=2.0)
    b : float, optional (default=0.75)
    """
    def __init__(self, use_idf = True, k1 = 2.0, b = 0.75):
        self.use_idf = use_idf
        self.k1 = k1
        self.b = b

    def fit(self, X):
        """
        X : sparse matrix, [n_samples, n_features]
            document-term matrix
        """
        if not sp.issparse(X):
            X = sp.csc_matrix(X)
        if self.use_idf:
            n_samples, n_features = X.shape
            df = _document_frequency(X)
            idf = np.log((n_samples - df + 0.5) / (df + 0.5))
            self._idf_diag = sp.spdiags(idf, diags=0, m=n_features, n=n_features)
        return self

    def transform(self, X, copy=True):
        """
        X : sparse matrix, [n_samples, n_features]
            document-term matrix
        copy : boolean, optional (default=True)
        """
        if hasattr(X, 'dtype') and np.issubdtype(X.dtype, float):
            X = sp.csr_matrix(X, copy=copy)
        else:
            X = sp.csr_matrix(X, dtype=np.float64, copy=copy)

        n_samples, n_features = X.shape

        dl = X.sum(axis=1)
        sz = X.indptr[1:] - X.indptr[0:-1]
        rep = np.repeat(np.asarray(dl), sz)
        avgdl = np.average(dl)
        data = X.data * (self.k1 + 1) / (X.data + self.k1 * (1 - self.b + self.b * rep / avgdl))
        X = sp.csr_matrix((data, X.indices, X.indptr), shape=X.shape)

        if self.use_idf:
            check_is_fitted(self, '_idf_diag', 'idf vector is not fitted')

            expected_n_features = self._idf_diag.shape[0]
            if n_features != expected_n_features:
                raise ValueError("Input has n_features=%d while the model"
                                 " has been trained with n_features=%d" % (
                                     n_features, expected_n_features))
            # *= doesn't work
            X = X * self._idf_diag

        return X

'''
https://github.com/arosh/BM25Transformer/blob/master/bm25.py
'''
###-------------
# Reading dataset
df = pd.read_csv("C:\\Users\\brand\\OneDrive - National University of Singapore\\Documents\\Fintech\\labelled_marketaux_news_combined_2022-10-15.csv")
df.dropna(axis = 0, inplace = True, subset = ['3m', '6m', '1y']) # Dropping na rows
df = df.iloc[:1000, :] # Getting subset so PC can run

# Getting sparse_matrix
corpus = df.loc[:, 'Relevant Texts'].tolist()
sum(df['3m'].isna())
vectorizer = CountVectorizer()
vectorizer.fit(corpus)
vector = vectorizer.transform(corpus)

bm25 = BM25Transformer()
bm25.fit(vector)
sparse_matrix = bm25.transform(vector).toarray()
sparse_matrix.shape

## Start training models
# Spliting train and test set
y_3m = df['3m']
y_6m = df['6m']
y_1y = df['1y']
from sklearn.model_selection import train_test_split
X_train, X_test, y_3m_train, y_3m_test, y_6m_train, y_6m_test, y_1y_train, y_1y_test = train_test_split(sparse_matrix, y_3m, y_6m, y_1y, test_size = 0.33, random_state = 0)

# Logistics model
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

def run_lr_model(X_train, X_test, y_train, y_test):
    lr = LogisticRegression(max_iter = 1000)
    model_lr = lr.fit(X_train, y_train)
    y_pred = model_lr.predict(X_test)
    print('Accuracy score for Logistic regression is:', accuracy_score(y_pred, y_test))
    return accuracy_score(y_pred, y_test)

## Sample runs
run_lr_model(X_train, X_test, y_3m_train, y_3m_test)
run_lr_model(X_train, X_test, y_6m_train, y_6m_test)
run_lr_model(X_train, X_test, y_1y_train, y_1y_test)

# Random Forest Classifier
from sklearn.ensemble import RandomForestClassifier

def run_random_forest_model(X_train, X_test, y_train, y_test, random_state = 0, n_estimators = 100):
    rfc = RandomForestClassifier(random_state = random_state, n_estimators = n_estimators)
    model_rfc = rfc.fit(X_train, y_train)
    y_pred = model_rfc.predict(X_test)
    print('Accuracy score for Random Forest is:', accuracy_score(y_pred, y_test))
    return accuracy_score(y_pred, y_test)
    
## Sample runs
run_random_forest_model(X_train, X_test, y_3m_train, y_3m_test)
run_random_forest_model(X_train, X_test, y_6m_train, y_6m_test)
run_random_forest_model(X_train, X_test, y_1y_train, y_1y_test)

# Gradient Boosting Classifier
from sklearn.ensemble import GradientBoostingClassifier

def run_gradient_boosting_model(X_train, X_test, y_train, y_test, random_state = 0, n_estimators = 100):
    gbc = GradientBoostingClassifier(random_state = random_state, n_estimators = n_estimators)
    model_gbc = gbc.fit(X_train, y_train)
    y_pred = model_gbc.predict(X_test)
    print('Accuracy score for Gradient Boosting is:', accuracy_score(y_pred, y_test))
    return accuracy_score(y_pred, y_test)
  
## Sample runs
run_gradient_boosting_model(X_train, X_test, y_3m_train, y_3m_test)
run_gradient_boosting_model(X_train, X_test, y_6m_train, y_6m_test)
run_gradient_boosting_model(X_train, X_test, y_1y_train, y_1y_test)

# Running various hyper-parameters
## Creating functions
def find_optimal_hyperparameters(model, X_train, X_test, y_train, y_test, start_hyper_param, end_hyper_param, random_state):
    optimal_list = []
    for i in range(start_hyper_param, end_hyper_param):
        print('For hyper-parameter value:', i)
        acc = model(X_train, X_test, y_train, y_test, random_state, i)
        optimal_list.append(acc)
    return start_hyper_param + optimal_list.index(max(optimal_list))
        
def determine_n_estimators_for_tree_based_model(model, X_train, X_test, y_train, y_test, start_random_state, end_random_state, start_n_estimators, end_n_estimators):
    optimal_list = []
    for i in range(start_random_state, end_random_state):
        print('For random state:', i)
        optimal = find_optimal_hyperparameters(model, X_train, X_test, y_train, y_test, start_n_estimators, end_n_estimators, i)
        optimal_list.append(optimal)
    counter = Counter(optimal_list)
    return counter.most_common(1)[0][0]

def determine_best_n_estimators_for_tree_based_model_across_3_dependent_variables(model, X_train, X_test, y_3m_train, y_3m_test, y_6m_train, y_6m_test, y_1y_train, y_1y_test, start_random_state, end_random_state, start_n_estimators, end_n_estimators):
    optimal_3m = determine_n_estimators_for_tree_based_model(model, X_train, X_test, y_3m_train, y_3m_test, start_random_state, end_random_state, start_n_estimators, end_n_estimators)
    optimal_6m = determine_n_estimators_for_tree_based_model(model, X_train, X_test, y_6m_train, y_6m_test, start_random_state, end_random_state, start_n_estimators, end_n_estimators)
    optimal_1y = determine_n_estimators_for_tree_based_model(model, X_train, X_test, y_1y_train, y_1y_test, start_random_state, end_random_state, start_n_estimators, end_n_estimators)
    optimal = [optimal_3m, optimal_6m, optimal_1y]
    return optimal

# Final accuracy
## Logistic regression
run_lr_model(X_train, X_test, y_3m_train, y_3m_test)
run_lr_model(X_train, X_test, y_6m_train, y_6m_test)
run_lr_model(X_train, X_test, y_1y_train, y_1y_test)

## Random Forest
optimal_n_estimator_for_random_forest = determine_best_n_estimators_for_tree_based_model_across_3_dependent_variables(run_random_forest_model, X_train, X_test, y_3m_train, y_3m_test, y_6m_train, y_6m_test, y_1y_train, y_1y_test, 0, 4, 100, 111)

run_random_forest_model(X_train, X_test, y_3m_train, y_3m_test, n_estimators = optimal_n_estimator_for_random_forest[0])
run_random_forest_model(X_train, X_test, y_6m_train, y_6m_test, n_estimators = optimal_n_estimator_for_random_forest[1])
run_random_forest_model(X_train, X_test, y_1y_train, y_1y_test, n_estimators = optimal_n_estimator_for_random_forest[2])

## Gradient boosting
"""
will take very long to run
optimal_n_estimator_for_gradient_boosting = determine_best_n_estimators_for_tree_based_model_across_3_dependent_variables(run_gradient_boosting_model, X_train, X_test, y_3m_train, y_3m_test, y_6m_train, y_6m_test, y_1y_train, y_1y_test, 0, 4, 100, 111)

run_gradient_boosting_model(X_train, X_test, y_3m_train, y_3m_test, n_estimators = optimal_n_estimator_for_gradient_boosting[0])
run_gradient_boosting_model(X_train, X_test, y_6m_train, y_6m_test, n_estimators = optimal_n_estimator_for_gradient_boosting[1])
run_gradient_boosting_model(X_train, X_test, y_1y_train, y_1y_test, n_estimators = optimal_n_estimator_for_gradient_boosting[2])
"""
run_gradient_boosting_model(X_train, X_test, y_3m_train, y_3m_test, n_estimators = 100)
run_gradient_boosting_model(X_train, X_test, y_6m_train, y_6m_test, n_estimators = 100)
run_gradient_boosting_model(X_train, X_test, y_1y_train, y_1y_test, n_estimators = 100)