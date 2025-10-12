from utliti import Preprocessing
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib


p = Preprocessing('drug_consumption.csv')

p.outliers()
p.feature()
p.convert_target()
p.label_encoder()
p.standard_scalar()

X_train, X_test, y_train, y_test = train_test_split(p.x, p.y, test_size=0.2, random_state=42, stratify=p.y)

model1=RandomForestClassifier(random_state=42)
model1.fit(X_train,y_train)
pre=model1.predict(X_test)
print(accuracy_score(y_test,pre))
print(classification_report(y_test,pre))


joblib.dump(model1, "drug_model.pkl")
print("✅ Model saved as 'drug_model.pkl'")