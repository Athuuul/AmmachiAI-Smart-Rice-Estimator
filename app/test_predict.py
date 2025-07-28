from predictor import predict_rice_amount

result = predict_rice_amount(
    num_people=4,
    appetite_level="Medium",
    meal_type="Lunch",
    guest_present="Yes",
    side_dishes=3,
    avg_age_group="Adult"
)

print(f"🍚 Predicted rice required: {result} grams")
