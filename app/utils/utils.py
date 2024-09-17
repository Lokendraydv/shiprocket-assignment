from geopy.geocoders import Nominatim
import pickle
import re
import logging
import pandas as pd


geolocator = Nominatim(user_agent="address_quality_classifier")

with open("model/calassification_model.pkl", "rb") as file:
    model = pickle.load(file)

def validate_address(address, city, state, pincode):
    try:
        location = geolocator.geocode(f"{address}, {city}, {state}, {pincode}")
        return location is not None
    except Exception as e:
        print(f"Geocoding error: {e}")
        return False
    
def validate_pincode(pincode):
    return re.match(r'^\d{6}$', pincode) is not None

def extract_features(address, city, state, pincode):
    if not address or not city or not state or not pincode or not validate_pincode(pincode):
        return pd.DataFrame([{'Address_Valid': False, 'Address_Length': 0, 'Pincode_Length': 0}])
    
    features = {
        'Address_Valid': bool(validate_address(address, city, state, pincode)),
        'Address_Length': len(address),
        'Pincode_Length': len(pincode),
    }
    return pd.DataFrame([features])


#Model training functions:-

def validate_address(address, city, state, pincode):
    try:
        location = geolocator.geocode(f"{address}, {city}, {state}, {pincode}")
        return location is not None
    except Exception as e:
        logging.error(f"Geocoding error: {e}")
        return False

def validate_pincode(pincode):
    return re.match(r'^\d{6}$', pincode) is not None

def standardize_address(address):
    address = str(address)
    return ' '.join(address.split()).title()

def train_validate_address(row):
        try:
            al = int(row['Address_Length'])
        except ValueError:
            al = 0  
        
        if al <= 10:
            row['Quality'] = 'Bad'
            row['Address_Valid'] = False
        elif 10 < al < 22:
            row['Quality'] = 'Medium'
            row['Address_Valid'] = False
        else:
            row['Quality'] = 'Good'
            row['Address_Valid'] = True
        
        return row

def preprocess_address(df):
    df['address'] = df['address'].apply(standardize_address)
    df['city'] = df['city'].apply(standardize_address)
    df['state'] = df['state'].apply(standardize_address)
    df['Address_Valid'] = df.apply(lambda row: validate_address(row['address'], row['city'], row['state'], row['pincode']), axis=1)
    df['Complete_Address'] = df[['address', 'city', 'state', 'pincode']].notna().all(axis=1)
    df['Address_Length'] = df['address'].apply(len)
    df['City_Length'] = df['city'].apply(len)
    df['State_Length'] = df['state'].apply(len)
    df['Pincode_Length'] = df['pincode'].apply(lambda x: len(str(x)))
    
    def classify_address(row):
        if row['Complete_Address'] and row['Address_Valid']:
            return 'Good'
        elif row['Complete_Address'] or row['Address_Valid']:
            return 'Medium'
        else:
            return 'Bad'

    df['Quality'] = df.apply(classify_address, axis=1)
    df['Quality'] = df['Quality'].replace({'Medium': 'Good', 'Good': 'Medium'})

    df = df.apply(train_validate_address, axis=1)
    df['Address_Valid'] = df['Address_Valid'].replace({True: 1, False: 0})
    df['Address_Length'] = df['Address_Length'].astype(int)
    return df
