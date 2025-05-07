import pandas as pd
from sklearn.preprocessing import LabelEncoder

def extract_data(file_path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(file_path)
        print(f"Dataset loaded from {file_path}")
        return df
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return None

# Function to encode categorical columns with error handling for unseen labels
def transform_data(df: pd.DataFrame, encoders: dict = None) -> pd.DataFrame:
    df.drop("customerID", axis=1, inplace=True)
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df.dropna(inplace=True)

    # Initialize encoders if not passed
    if encoders is None:
        encoders = {}

    for col in df.select_dtypes(include=["object"]).columns:
        if col != "Churn":
            if col not in encoders:
                encoders[col] = LabelEncoder()
                encoders[col].fit(df[col].unique())  # Fit encoder on all unique values of the column
            
            # Apply transformation while handling unseen labels
            df[col] = encoders[col].transform(df[col].values)

    # Encode the target variable 'Churn'
    df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})
    
    return df, encoders  # Return transformed data and encoders for reuse
