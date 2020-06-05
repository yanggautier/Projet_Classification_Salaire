import pandas as pd
import pickle
import seaborn as sns; sns.set(style="ticks", color_codes=True)
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

def main():
    data = pd.read_csv('csv/Prepo.csv', sep=';', encoding="utf-8-sig")

    X = data.drop('Classe de salaire par an', axis=1)
    y = data['Classe de salaire par an']

    # ax = sns.heatmap(data.corr())
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    models = [RandomForestClassifier(n_estimators=100), DecisionTreeClassifier(), LogisticRegression(), SVC(),
              KNeighborsClassifier(5), MultinomialNB(), BernoulliNB()]
    models_name = ["RandomForestClassifier", "DecisionTreeClassifier", "LogisticRegression", "SVC",
                   "KNeighborsClassifier", "MultinomialNB", "BernoulliNB"]
    for i in range(len(models)):
        models[i].fit(X_train, y_train)
        y_pred = models[i].predict(X_test)
        scores = cross_val_score(models[i], X_train, y_train)
        accuracy = accuracy_score(y_test, y_pred)

        print("Model: ", models_name[i])
        print('Cross mean score: ', scores.mean())
        print('Accuracy: ', accuracy)
        print()

    # RandomForestClassifier avec GridSearchCV
    param_grid = {
        'n_estimators': [100, 200, 300, 700],
        'max_features': ['auto', 'sqrt', 'log2']
    }
    model = RandomForestClassifier()
    grid = GridSearchCV(estimator=model, param_grid=param_grid, cv=5, scoring='accuracy')
    grid.fit(X_train, y_train)

    print(grid.best_estimator_)
    grid_predictions = grid.predict(X_test)
    print(confusion_matrix(y_test, grid_predictions))
    print(classification_report(y_test, grid_predictions))

    # Decision Tree avec Grid search CV
    params = {'max_leaf_nodes': list(range(2, 100)), 'min_samples_split': [2, 3, 4]}
    grid = GridSearchCV(DecisionTreeClassifier(random_state=42), params, verbose=1, cv=3)
    grid.fit(X_train, y_train)

    print(grid.best_estimator_)
    grid_predictions = grid.predict(X_test)
    print(confusion_matrix(y_test, grid_predictions))
    print(classification_report(y_test, grid_predictions))

    # SVC avec Grid search CV
    # kernels = ['Polynomial', 'RBF', 'Sigmoid', 'Linear']

    param_grid = {'C': [0.1, 1, 10, 100], 'gamma': [1, 0.1, 0.01, 0.001], 'kernel': ['rbf', 'poly', 'sigmoid']}

    grid = GridSearchCV(SVC(), param_grid, refit=True, verbose=2)
    grid.fit(X_train, y_train)

    print(grid.best_estimator_)
    grid_predictions = grid.predict(X_test)
    print(confusion_matrix(y_test, grid_predictions))
    print(classification_report(y_test, grid_predictions))

    # LogisticRegression avec GridSearchCV

    model = LogisticRegression()
    params = {'penalty': ['l1', 'l2'], 'C': [0.001, 0.01, 0.1, 1, 10, 100, 1000]}
    grid = GridSearchCV(estimator=model, param_grid=params)

    grid.fit(X_train, y_train)

    print(grid.best_estimator_)
    grid_predictions = grid.predict(X_test)
    print(confusion_matrix(y_test, grid_predictions))
    print(classification_report(y_test, grid_predictions))

    # KNeighborsClassifier avec Grid search CV

    k_range = list(range(1, 15))
    weight_options = ["uniform", "distance"]

    param_grid = dict(n_neighbors=k_range, weights=weight_options)
    # print (param_grid)
    knn = KNeighborsClassifier()

    grid = GridSearchCV(knn, param_grid, cv=10, scoring='accuracy')
    grid.fit(X_train, y_train)

    print(grid.best_estimator_)
    grid_predictions = grid.predict(X_test)
    print(confusion_matrix(y_test, grid_predictions))
    print(classification_report(y_test, grid_predictions))

    pickle.dump(RandomForestClassifier, open('model.pkl', 'wb'))

    model = pickle.load(open('model.pkl','rb'))
    print(model.predict([[1.8]]))

if __name__ == '__main__':
    main()