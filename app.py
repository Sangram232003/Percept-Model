import numpy as np
import pandas as pd
import kagglehub
import pickle

from sklearn.linear_model import Perceptron
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# Download dataset
path = kagglehub.dataset_download("vatsalrakholiya/perceptron-data")

print("Path to dataset files:", path)


# Load placement dataset
df = pd.read_csv(f"{path}/placement.csv")

print(df.head())
print(df.columns)


# Only 2 features
X = df[['cgpa', 'resume_score']]

# Target
y = df['placed']


# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=41
)


# Create Perceptron
model = Perceptron(
    random_state=41,
    max_iter=1000,
    tol=1e-3
)


# Train
model.fit(X_train, y_train)


# Test
predict = model.predict(X_test)

accuracy = accuracy_score(y_test, predict)

print("Accuracy:", accuracy * 100)


# Show weights
print("Weights:", model.coef_)

# Show intercept
print("Intercept:", model.intercept_)


# Save model
with open("Perceptron.pkl", "wb") as file:
    pickle.dump(model, file)

print("Perceptron.pkl created successfully.")
