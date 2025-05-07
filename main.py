from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse
import pandas as pd
import joblib
import os
from io import StringIO
from sklearn.preprocessing import LabelEncoder
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Load model and encoders
model_path = os.getenv("MODEL_PATH")
encoder_path = os.getenv("ENCODER_PATH")

# Load the model and encoders
try:
    model = joblib.load(model_path)
    print(f"Model loaded from {model_path}")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

try:
    encoders = joblib.load(encoder_path)
    print(f"Encoders loaded from {encoder_path}")
except Exception as e:
    print(f"Error loading encoders: {e}")
    encoders = None


# Helper to safely transform categorical data
def safe_label_transform(series: pd.Series, encoder: LabelEncoder) -> pd.Series:
    known_classes = set(encoder.classes_)
    return series.apply(lambda val: encoder.transform([val])[0] if val in known_classes else -1)


# Function to transform the data
def transform_data(df: pd.DataFrame, encoders=None) -> pd.DataFrame:
    # Check if 'customerID' exists before dropping it
    if "customerID" in df.columns:
        df.drop("customerID", axis=1, inplace=True)
    
    # Convert 'TotalCharges' to numeric, handle errors
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df.dropna(inplace=True)

    if not encoders:
        encoders = {}

    # Encoding categorical variables
    for col in df.select_dtypes(include=["object"]).columns:
        if col != "Churn":
            if col not in encoders:
                encoder = LabelEncoder()
                encoder.fit(df[col])
                encoders[col] = encoder
            df[col] = safe_label_transform(df[col], encoders[col])
    
    # Encoding target variable
    if "Churn" in df.columns:
        df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})
    
    return df, encoders


@app.get("/")
def read_root():
    return {"message": "Welcome to the Churn Prediction API"}


@app.post("/predict_batch")
async def predict_churn_batch(file: UploadFile = File(...)):
    if model is None or encoders is None:
        raise HTTPException(status_code=500, detail="Model or encoders not loaded.")
    
    try:
        # Read the uploaded CSV file
        file_content = await file.read()
        csv_data = StringIO(file_content.decode("utf-8"))
        df = pd.read_csv(csv_data)

        # Ensure the required columns are in the CSV
        required_columns = [
            "gender", "SeniorCitizen", "Partner", "Dependents", "tenure",
            "PhoneService", "MultipleLines", "InternetService", "OnlineSecurity",
            "OnlineBackup", "DeviceProtection", "TechSupport", "StreamingTV",
            "StreamingMovies", "Contract", "PaperlessBilling", "PaymentMethod",
            "MonthlyCharges", "TotalCharges"
        ]
        
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise HTTPException(status_code=400, detail=f"Missing columns: {', '.join(missing_columns)}")

        # Process the CSV data to match the model's input format
        predictions = []

        # Transform the data
        df, updated_encoders = transform_data(df, encoders)

        for index, row in df.iterrows():
            transformed_data = row.drop("Churn", errors="ignore").tolist()

            churn_prediction = model.predict([transformed_data])
            predictions.append({"index": index, "churn": int(churn_prediction[0])})

        # Update the encoders after prediction
        encoders.update(updated_encoders)

        # Save the updated encoders to persist them
        joblib.dump(encoders, encoder_path)
        print(f"Encoders saved to {encoder_path}")

        return JSONResponse(content={"predictions": predictions})

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error during prediction: {str(e)}")
