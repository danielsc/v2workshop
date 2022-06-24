import argparse
import pandas as pd
import mlflow

parser = argparse.ArgumentParser()
parser.add_argument("--input_csv", default="data/titanic.csv")   # input folder
parser.add_argument("--output_tsv", default="data/titanic.tsv")   # input folder
args = parser.parse_args()

mlflow.log_param("input", args.input_csv)
mlflow.log_param("output", args.output_tsv)

print(f"Converting {args.input_csv} to {args.output_tsv}")
df = pd.read_csv(args.input_csv)

mlflow.log_metric("size", len(df))

df.describe().to_csv("statistics.csv")
mlflow.log_artifact("statistics.csv")
df.describe(include=['O']).to_csv("categorical.csv")
mlflow.log_artifact("categorical.csv")

df.to_csv(args.output_tsv, sep="\t", index=False)


