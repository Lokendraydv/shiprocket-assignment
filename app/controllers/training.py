from flask import request, jsonify
import pandas as pd
import pickle
from geopy.geocoders import Nominatim
from app.utils import utils
import logging
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import time

geolocator = Nominatim(user_agent="address_quality_classifier")

if not os.path.exists("model"):
    os.makedirs("model")

train_model_path = os.path.join("model","Finetuned_model.pkl")
# Configure logging
# logging.basicConfig(filename='model_training.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def train_model():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if not file.filename.endswith('.csv'):
        return jsonify({"error": "File format not supported"}), 400
    
    try:
        df = pd.read_csv(file)
        
        # Check for required columns
        required_columns = {'address', 'city', 'state', 'pincode'}
        if not required_columns.issubset(df.columns):
            return jsonify({"error": "CSV file must contain columns: address, city, state, pincode"}), 400
        
        # Drop rows with missing required columns
        df.dropna(subset=['address', 'city', 'state', 'pincode'], inplace=True)
        
        # Preprocess data
        df = utils.preprocess_address(df)
        
        features = df[['Address_Valid', 'Address_Length', 'Pincode_Length']]
        labels = df['Quality']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.3, random_state=42)
        
        # Initialize model
        model = RandomForestClassifier()
        
        # Log the start of model training
        start_time = time.time()
        logging.info("Starting model training.")
        
        # Train the model
        model.fit(X_train, y_train)
        
        # Log the end of model training
        end_time = time.time()
        logging.info(f"Model training completed in {end_time - start_time:.2f} seconds.")
        
        # Evaluate the model
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        logging.info(f"Model Accuracy: {accuracy:.4f}")
        
        # Save the model
        with open(train_model_path, 'wb') as file:
            pickle.dump(model, file)
        
        return jsonify({"message": "Model trained and saved successfully", "accuracy": accuracy})

    except Exception as e:
        logging.error(f"Error processing file: {e}")
        return jsonify({"error": str(e)}), 500
