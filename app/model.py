import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import joblib
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# path for the dataset from environment variables
dataset_path = os.getenv("DATASET_PATH")

# Check if the dataset path is set
if dataset_path is None:
    print("Error: DATASET_PATH is not set in the .env file!")
    exit()

# Check if the dataset exists at the specified path
if not os.path.exists(dataset_path):
    print(f"Error: Dataset not found at the path: {dataset_path}")
    exit()

print("Dataset found. Loading...")

# Load dataset using the path from the environment variable
df = pd.read_csv(dataset_path)

# Check current working directory
print("Current Working Directory:", os.getcwd())

# Drop customerID (not useful for prediction)
df.drop("customerID", axis=1, inplace=True)

# Convert TotalCharges to numeric, handle errors
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df.dropna(inplace=True)

# Initialize a dictionary to store the encoders
encoders = {}

# Encode categorical columns
for col in df.select_dtypes(include=["object"]).columns:
    if col != "Churn":
        encoder = LabelEncoder()
        df[col] = encoder.fit_transform(df[col])
        encoders[col] = encoder

# Encode target variable
df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})

# Features and target
X = df.drop("Churn", axis=1)
y = df["Churn"]

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save model and encoders
model_dir = "model"
os.makedirs(model_dir, exist_ok=True)
model_path = os.path.join(model_dir, "churn_model.pkl")
encoder_path = os.path.join(model_dir, "encoders.pkl")

joblib.dump(model, model_path)
joblib.dump(encoders, encoder_path)

print(f"✅ Model saved to {model_path}")
print(f"✅ Encoders saved to {encoder_path}")
