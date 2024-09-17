from flask import request, jsonify
from app.utils import utils


def classify():
    try:
        data = request.get_json()
        address = data.get('Address', '')
        city = data.get('City', '')
        state = data.get('State', '')
        pincode = data.get('Pincode', '')

        if not address or not city or not state or not pincode:
            return jsonify({"Quality": "Bad"}), 400
        
        if not utils.validate_pincode(pincode):
            return jsonify({"Quality": "Bad"}), 400
        
        features = utils.extract_features(address, city, state, pincode)
        
        # Convert Address_Length to integer
        features['Address_Length'] = features['Address_Length'].astype(int)
        features['Address_Valid'] = features['Address_Valid'].replace({True: 1, False: 0})
        print(features)
        prediction = utils.model.predict(features)
        
        
        return jsonify({"Quality": prediction[0]})

    except Exception as e:
        return jsonify({'error': str(e)}), 400