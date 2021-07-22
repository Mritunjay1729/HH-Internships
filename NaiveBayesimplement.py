# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 22:50:41 2021

@author: MRITYUNJAY
Naive Bayes Algorithm Implementation
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

#getting dataset
df = pd.read_csv('mushrooms.csv')
df.columns
df.head(50)

le = LabelEncoder()
pd.set_option("display.maX_columns",5)
pd.set_option("display.maX_rows", 16)
df_encoded = df.apply(le.fit_transform, axis=0)
df_encoded
df = df_encoded.values

x = df[:, 1:]
y = df[:, 0]
x
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.4, random_state=42)

#Prior Probablity
def prior_probablity(y_train, label):
    m  = y_train.shape[0]
    s = np.sum(y_train == label)
    
    return s/m

prior_probablity(y_train, 1)
    
#Conditional Probablity
#likelyhood
#posterior Probabity
def cond_probablity(X_train, y_train, feature_col, feature_label, label):
    X_filtered = X_train[y_train == label]
    num = np.sum(X_filtered[:, feature_col] == feature_label)
    
    denom = X_filtered.shape[0]
    return float(num/denom)

#likelihood
def predict(X_train, y_train, X_test):
    classes = np.unique(y_train)
    n_features = X_train.shape[1]   
    n_values = [np.unique(X_train[i]) for i in range(n_features)]
    n_values
    posterior_prob = []
    for label in classes: #Classes such as spam or not span
        likelihood = 1.0
        for features in range(n_features): #Features of X_train i.e, x1, x2, x3, x4, ... , xn
            cond = cond_probablity(X_train, y_train, features, X_test[features], label)
            likelihood = likelihood * cond
        prior = prior_probablity(y_train, label)
        post = likelihood * prior
        posterior_prob.append(post)
        
    pred = np.argmax(posterior_prob)
    return pred

#Accuracy of th emodel we created
def accuracy(X_train, X_test, y_train, y_test):
    pred = []
    for i in range(0, X_test.shape[0]):
        p = predict(X_train, y_train, X_test[i])
        pred.append(p)
    
    y_pred = np.array(pred)
    acc = sum(y_pred == y_test)/y_test.shape[0]
    
    return acc

accuracy(X_train, X_test, y_train, y_test)
    
            