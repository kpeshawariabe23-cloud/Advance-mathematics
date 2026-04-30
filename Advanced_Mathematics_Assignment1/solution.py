import pandas as pd
import numpy as np

# Load dataset
file_path = 'data.csv'
df = pd.read_csv(file_path, low_memory=False, encoding='cp1252')

# Consider NO2 as feature (x)
# Drop NA values from 'no2' column
x = df['no2'].dropna().values

# Roll Number
r = 102303502

# Calculate a_r and b_r
a_r = 0.05 * (r % 7)
b_r = 0.3 * ((r % 5) + 1)

print(f"Roll Number: {r}")
print(f"a_r: {a_r}")
print(f"b_r: {b_r}")

# Transform x into z
z = x + a_r * np.sin(b_r * x)

# Learn parameters of the probability density function (Gaussian)
# p(z) = c * exp(-\lambda(z-\mu)^2)
# We can estimate mu and sigma using Maximum Likelihood Estimation (MLE)
# For a Gaussian, the MLE estimates are the sample mean and sample standard deviation

mu = np.mean(z)
sigma = np.std(z) # Using ddof=0 for MLE

# Calculate lambda and c based on Gaussian PDF formula
# lambda = 1 / (2 * sigma^2)
# c = 1 / (sigma * sqrt(2 * pi))

lambda_param = 1 / (2 * (sigma ** 2))
c = 1 / (sigma * np.sqrt(2 * np.pi))

print("\n--- Estimated Parameters ---")
print(f"mu: {mu}")
print(f"lambda: {lambda_param}")
print(f"c: {c}")

# Save to output file
with open('output_parameters.txt', 'w') as f:
    f.write(f"Roll Number: {r}\n")
    f.write(f"a_r: {a_r}\n")
    f.write(f"b_r: {b_r}\n\n")
    f.write(f"--- Estimated Parameters ---\n")
    f.write(f"mu: {mu}\n")
    f.write(f"lambda: {lambda_param}\n")
    f.write(f"c: {c}\n")

print("\nParameters have been saved to output_parameters.txt")


