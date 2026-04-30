import sys
import pandas as pd
import numpy as np

if len(sys.argv) != 5:
    print("Usage: python topsis.py <InputDataFile> <Weights> <Impacts> <OutputResultFileName>")
    sys.exit(1)

inputFile, weights, impacts, resultFile = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]

try:
    df = pd.read_csv(inputFile)
except FileNotFoundError:
    print("File not Found")
    sys.exit(1)

if len(df.columns) < 3:
    print("Input file must contain three or more columns")
    sys.exit(1)

weights = weights.split(',')
impacts = impacts.split(',')

try:
    data = df.iloc[:, 1:].values.astype(float)
except:
    print("From 2nd to last columns must contain numeric values only")
    sys.exit(1)

n = len(df.columns) - 1
if len(weights) != n or len(impacts) != n:
    print("Number of weights, number of impacts and number of columns must be the same")
    sys.exit(1)

for imp in impacts:
    if imp not in ['+', '-']:
        print("Impacts must be either +ve or -ve")
        sys.exit(1)

weights = [float(w) for w in weights]

norm = data / np.sqrt((data ** 2).sum(axis=0))
weighted = norm * weights

ideal_best = np.where([i == '+' for i in impacts], weighted.max(axis=0), weighted.min(axis=0))
ideal_worst = np.where([i == '+' for i in impacts], weighted.min(axis=0), weighted.max(axis=0))

dist_best = np.sqrt(((weighted - ideal_best) ** 2).sum(axis=1))
dist_worst = np.sqrt(((weighted - ideal_worst) ** 2).sum(axis=1))

score = dist_worst / (dist_best + dist_worst)
df['Topsis Score'] = score
df['Rank'] = df['Topsis Score'].rank(ascending=False).astype(int)

df.to_csv(resultFile, index=False)
