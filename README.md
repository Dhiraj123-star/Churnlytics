# Churn Prediction API 📊

This API provides a solution for predicting customer churn based on their subscription details. It uses machine learning models to predict whether a customer is likely to churn (leave) based on various factors like contract type, payment method, internet service, and more.

## Core Features 🚀

1. **Churn Prediction** 🔮:
   - The API predicts the likelihood of a customer churning based on their attributes, such as contract type, tenure, payment method, and more.
   - Predictions are made using a trained machine learning model.

2. **Batch Prediction** 📥:
   - Users can upload a CSV file containing multiple customer records.
   - The API processes the CSV and returns predictions for each customer in the dataset.

3. **Model and Encoder Management** 🔧:
   - The API supports loading and using a pre-trained machine learning model and encoders.
   - If a new category is encountered in the data (e.g., a new contract type), the model will classify it as 'UNKNOWN', preventing errors from unseen labels.
   - The encoders are updated after every prediction batch to ensure they reflect the most recent data.

4. **Error Handling** ⚠️:
   - Comprehensive error handling to guide users if there are missing columns or issues during prediction.
   - Provides clear messages when required columns are missing or if there is a problem with the model or encoders.

## API Endpoints 🔌

### 1. **GET `/`**
   - **Description**: A welcome endpoint to test if the API is running.
   - **Response**: Returns a simple message: `{"message": "Welcome to the Churn Prediction API"}`.

### 2. **POST `/predict_batch`**
   - **Description**: Upload a CSV file containing customer data for churn prediction.
   - **Request**: A CSV file must be uploaded with the following required columns:
     - `gender`, `SeniorCitizen`, `Partner`, `Dependents`, `tenure`, 
     - `PhoneService`, `MultipleLines`, `InternetService`, `OnlineSecurity`, 
     - `OnlineBackup`, `DeviceProtection`, `TechSupport`, `StreamingTV`, 
     - `StreamingMovies`, `Contract`, `PaperlessBilling`, `PaymentMethod`, 
     - `MonthlyCharges`, `TotalCharges`.
   - **Response**: Returns a list of predictions for each customer, including their churn status (1 for churn, 0 for no churn).

## How It Works 🛠️

1. **Data Transformation** 🧹:
   - The incoming data is cleaned and transformed to match the input requirements of the machine learning model. 
   - Categorical variables are encoded using pre-trained encoders.
   - If the model encounters a category that was not seen during training, it assigns it the value `'UNKNOWN'` to avoid errors.
   
2. **Churn Prediction** 📉:
   - The transformed data is passed into the machine learning model, which predicts whether a customer will churn or not.
   
3. **Updating Encoders** 🔄:
   - After processing each batch, the encoders are updated to reflect any new categories found in the incoming data.
   - The updated encoders are saved to ensure they are available for future predictions.

## Error Handling 🚨

- **Missing Columns**: If the uploaded file does not contain all required columns, the API will return a `400` error with a message listing the missing columns.
- **Prediction Errors**: If any error occurs during prediction (e.g., missing or invalid data), the API will return a `400` error with details about the issue.
- **Model/Encoder Issues**: If the model or encoders cannot be loaded, the API will return a `500` error indicating an internal issue.

## Getting Started 🏃‍♂️

1. **Install dependencies**:
   - Install required libraries via `pip`:
     ```bash
     pip install -r requirements.txt
     ```

2. **Set up the environment**:
   - Create a `.env` file to store the paths for the trained model and encoders:
     ```env
     MODEL_PATH=path_to_your_model
     ENCODER_PATH=path_to_your_encoders
     ```

3. **Run the API**:
   - Start the FastAPI server using Uvicorn:
     ```bash
     uvicorn main:app --reload
     ```
   - The API will be accessible at `http://localhost:8000`.

4. **Test the API**:
   - Use a tool like [Postman](https://www.postman.com/) or [cURL](https://curl.se/) to test the endpoints, or directly interact with the Swagger UI at `http://localhost:8000/docs`.

## Conclusion 🎯

This Churn Prediction API allows businesses to leverage machine learning to make data-driven decisions about customer retention. By predicting churn, businesses can take proactive measures to improve customer satisfaction and reduce churn rates.

