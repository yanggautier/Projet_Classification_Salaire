import pandas as pd
import pickle
import seaborn as sns; sns.set(style="ticks", color_codes=True)
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.metrics import accuracy_score


data = pd.read_csv("C:/Users/Utilisateur/Desktop/Projet/Flask/csv/Prepo.csv", sep=';', encoding="utf-8-sig")

X = data.drop('Classe de salaire par an', axis=1)
y = data['Classe de salaire par an']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

model = RandomForestClassifier(n_estimators=100)
model_name = "RandomForestClassifier"

model.fit(X_train, y_train)
y_pred = model.predict(X_test)
score = cross_val_score(model, X_train, y_train)
accuracy = accuracy_score(y_test, y_pred)

print("Model: ", model_name)
print('Cross mean score: ', score.mean())
print('Accuracy: ', accuracy * 100)

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

pickle.dump(grid, open('model.pkl', 'wb'))

# model = pickle.load(open('model.pkl','rb'))
# print(model.predict([[2, 9, 6]]))