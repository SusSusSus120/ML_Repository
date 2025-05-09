# -*- coding: utf-8 -*-
"""Danny M - ML Tweets.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1dYCooZtpmrm94DV7V5KAva0UJPGDZWgv
"""

#Danny Mendelson

#imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

#upload data
train = pd.read_csv('/kaggle/input/nlp-getting-started/train.csv')
test  = pd.read_csv('/kaggle/input/nlp-getting-started/test.csv')
submission = pd.read_csv('/kaggle/input/nlp-getting-started/sample_submission.csv')

# Class balance
print(train['target'].value_counts(normalize=True))

# Tweet length distribution
train['text_len'] = train['text'].str.split().apply(len)
sns.histplot(train, x='text_len', hue='target', element='step', stat='density')
plt.title('Tweet Word Count by Class')
plt.show()

lemmatizer = WordNetLemmatizer()
stops = set(stopwords.words('english'))

def clean_text(doc):
    doc = doc.lower()
    doc = re.sub(r'http\S+|www\.\S+', ' ', doc)             # URLs
    doc = re.sub(r'@\w+|#', ' ', doc)                      # mentions & hashtags
    doc = re.sub(r'[^a-z\s]', ' ', doc)                    # non-letters
    tokens = [lemmatizer.lemmatize(w) for w in doc.split() if w not in stops and len(w)>2]
    return ' '.join(tokens)

train['clean'] = train['text'].apply(clean_text)
test['clean']  = test['text'].apply(clean_text)

#feature extraction
tfidf = TfidfVectorizer(ngram_range=(1,2), max_features=20_000)
X = tfidf.fit_transform(train['clean'])
y = train['target']

# Hold-out split
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Baseline: Logistic Regression
clf = LogisticRegression(max_iter=1_000)
clf.fit(X_train, y_train)

# Validation performance
y_pred = clf.predict(X_val)
print(classification_report(y_val, y_pred))\

clf.fit(X, y)
X_test = tfidf.transform(test['clean'])
test_preds = clf.predict(X_test)

submission['target'] = test_preds
submission.to_csv('submission.csv', index=False)