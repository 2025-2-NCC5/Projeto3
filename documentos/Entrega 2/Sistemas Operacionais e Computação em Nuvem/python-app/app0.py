# train_classifier.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib
#import _mysql_connector

df = pd.read_pickle("processed.pkl")
HORIZON = 12
df["cpu_future"] = df["cpu_percent"].shift(-HORIZON)
df = df.dropna()
df["high"] = (df["cpu_future"] > 80).astype(int)

X = df.drop(columns=["cpu_future","high"])
y = df["high"]

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)
pred = clf.predict(X_test)
print(classification_report(y_test, pred))
joblib.dump(clf, "rf_cpu_classifier.pkl")
