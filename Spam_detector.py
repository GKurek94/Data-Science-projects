import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split


def spam_detector(df):

    def best_classifier(dicts):
        for e in dicts:
            if dicts[e] == max(dicts.values()):
                return e

    # Loading data and splitting the data
    df = pd.read_csv(df)
    train_data, test_data, train_target, test_target = train_test_split(df['text'], df['label_num'], test_size=0.8)

    # Vectorizer
    tfidf = TfidfVectorizer(ngram_range=(1, 2), min_df=2)
    x_train = tfidf.fit_transform(train_data)
    x_test = tfidf.transform(test_data)

    # Logistic Regression
    log_reg = LogisticRegression(random_state=0)
    log_reg.fit(x_train, train_target)
    y_pred_log = log_reg.predict(x_test)
    cm_log = confusion_matrix(test_target, y_pred_log)
    recall_log = cm_log[0][0] / (cm_log[0][1] + cm_log[0][0])

    # Multinomial Naive Bayes
    classifier_multi = MultinomialNB()
    classifier_multi.fit(x_train, train_target)
    y_pred = classifier_multi.predict(x_test)
    cm_multi = confusion_matrix(test_target, y_pred)
    recall_multi = cm_multi[0][0] / (cm_multi[0][1] + cm_multi[0][0])

    # Decision Tree Classifier
    classifier_tree = DecisionTreeClassifier(max_depth=2, random_state=0)
    classifier_tree.fit(x_train, train_target)
    y_pred_tree = classifier_tree.predict(x_test)
    cm_tree = confusion_matrix(test_target, y_pred_tree)
    recall_tree = cm_tree[0][0] / (cm_tree[0][1] + cm_tree[0][0])

    # Linear SVC
    classifier_svc = SVC(C=1.0, kernel='linear')
    classifier_svc.fit(x_train, train_target)
    y_pred_svc = classifier_svc.predict(x_test)
    cm_svc = confusion_matrix(test_target, y_pred_svc)
    recall_svc = cm_svc[0][0] / (cm_svc[0][1] + cm_svc[0][0])

    # Dictionary of algorithm names and their values in that case
    dict_of_algorithms = {
        "LogisticRegression": recall_log,
        "MultinomialNB": recall_multi,
        "DecisionTreeClassifier": recall_tree,
        "LinearSVC": recall_svc}

    results = {
        "LogisticRegression": recall_log,
        "MultinomialNB": recall_multi,
        "DecisionTreeClassifier": recall_tree,
        "LinearSVC": recall_svc,
        "TfidfVectorizer": tfidf,
        "Best Classifier": best_classifier(dict_of_algorithms),
        "Best value": max(recall_svc, recall_log, recall_tree, recall_multi),
    }
    return results


print(spam_detector('C:/Users/gkure/OneDrive/Pulpit/Python/spam_ham_dataset.csv'))
