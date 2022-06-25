import argparse
import pandas as pd
import mlflow
from sklearn.ensemble import GradientBoostingClassifier 
from sklearn.model_selection import train_test_split
from mlflow.models import infer_signature

parser = argparse.ArgumentParser()
parser.add_argument("--input_tsv", default="data/titanic.tsv")   # input folder
parser.add_argument("--output_model", default="data/model")   # input folder
parser.add_argument("--test_json", default="data/test.json")   # input folder
args = parser.parse_args()

mlflow.log_param("input_tsv", args.input_tsv)
mlflow.log_param("output_model", args.output_model)

df = pd.read_csv(args.input_tsv, sep='\t')

df = df.drop(["Name", "Cabin", "Ticket"], axis=1)
cols = ["Age", "Embarked"]
df[cols]=df[cols].fillna(df.mode().iloc[0])
df = pd.get_dummies(df, columns = ["Sex","Embarked"])
df = df.astype("float64")

df.drop(["Survived"], axis=1).head(10).to_json(args.test_json, orient='split')

X_train, X_test, Y_train, Y_test = train_test_split(df.drop(["Survived"], axis=1).values,
                                                    df["Survived"],
                                                    test_size=0.2,
                                                    random_state=42)

grad_boost = GradientBoostingClassifier(n_estimators = 100)
grad_boost.fit(X_train, Y_train)
Y_pred = grad_boost.predict(X_test)
grad_boost.score(X_train, Y_train)
acc_grad_boost = round(grad_boost.score(X_train, Y_train) * 100, 2)

signature = infer_signature(model_input=df.drop(["Survived"], axis=1).head(10))

mlflow.sklearn.save_model(grad_boost, args.output_model, signature=signature)