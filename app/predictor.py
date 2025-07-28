
import pandas as pd
import joblib
import numpy as np

# Load model and encoder
model = joblib.load('C:/Users/athul/Documents/AI/models/rice_predictor.pkl')
encoder = joblib.load('C:/Users/athul/Documents/AI/models/encoder.pkl')

def predict_rice_amount(
    num_people: int,
    appetite_level: str,
    meal_type: str,
    guest_present: str,
    side_dishes: int,
    avg_age_group: str
) -> float:
    input_dict = {
        "num_people": [num_people],
        "side_dishes": [side_dishes],
        "appetite_level": [appetite_level],
        "meal_type": [meal_type],
        "guest_present": [guest_present],
        "avg_age_group": [avg_age_group]
    }

    input_df = pd.DataFrame(input_dict)

    # Encode categorical columns
    categorical_cols = ['appetite_level', 'meal_type', 'guest_present', 'avg_age_group']
    encoded = encoder.transform(input_df[categorical_cols])
    encoded_df = pd.DataFrame(encoded, columns=encoder.get_feature_names_out(categorical_cols))

    # Combine with numerical features
    final_input = pd.concat([input_df[['num_people', 'side_dishes']], encoded_df], axis=1)

    prediction = model.predict(final_input)[0]
    return round(prediction, 2)
