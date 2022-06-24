import argparse
import pandas

parser = argparse.ArgumentParser()
parser.add_argument("--input_csv", default="data/titanic.csv")   # input folder
parser.add_argument("--output_parquet", default="data/titanic.tsv")   # input folder
args = parser.parse_args()

print(f"Converting {args.input_csv} to {args.output_parquet}")

df = pandas.read_csv(args.input_csv)

df.to_csv(args.output_parquet, sep="\t")
