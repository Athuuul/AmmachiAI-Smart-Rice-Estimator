import streamlit as st
from predictor import predict_rice_amount
from utils.voice import speak_malayalam
import time
from fractions import Fraction

st.set_page_config(page_title="AmmachiAI 🍚", page_icon="👵", layout="centered")

st.title("👵 AmmachiAI: Smart Rice Estimator")
st.markdown("##### _“Choru ethra venamennu ariyilla? Ammachi parayatte!”_")
st.divider()

# Fraction formatting
def format_fraction(value):
    rounded = round(value * 4) / 4  # Round to nearest ¼
    whole = int(rounded)
    frac = rounded - whole

    if frac == 0:
        return f"{whole}"
    else:
        fraction_str = str(Fraction(frac).limit_denominator(4))
        return f"{whole} {fraction_str}" if whole > 0 else f"{fraction_str}"

# Malayalam formatting
def format_malayalam(cups):
    mapping = {
        0.25: "ക്വാർട്ടർ", 0.5: "അര", 0.75: "മുക്കാൽ", 1.0: "ഒന്ന്",
        1.25: "ഒന്നു ക്വാർട്ടർ", 1.5: "ഒന്നു അര", 1.75: "ഒന്നു മുക്കാൽ",
        2.0: "രണ്ട്", 2.25: "രണ്ടു ക്വാർട്ടർ", 2.5: "രണ്ടു അര", 2.75: "രണ്ടു മുക്കാൽ",
        3.0: "മൂന്നു", 3.25: "മൂന്നു ക്വാർട്ടർ", 3.5: "മൂന്നു അര", 3.75: "മൂന്നു മുക്കാൽ",
        4.0: "നാലു", 4.25: "നാലു ക്വാർട്ടർ", 4.5: "നാലു അര", 4.75: "നാലു മുക്കാൽ",
        5.0: "അഞ്ചു"
    }
    rounded = round(cups * 4) / 4
    return mapping.get(rounded, f"{rounded:.2f}")

# Inputs
num_people = st.slider("👨‍👩‍👧‍👦 Number of People", 1, 20, 4)
appetite = st.selectbox("🍴 Appetite Level", ["Low", "Medium", "High"])
meal_type = st.selectbox("🍱 Meal Type", ["Lunch", "Dinner", "Sadhya", "Breakfast"])
guest = st.radio("🎁 Guest Present?", ["Yes", "No"], horizontal=True)
side_dishes = st.slider("🥗 Number of Side Dishes", 1, 6, 3)
age_group = st.selectbox("🎂 Average Age Group", ["Youth", "Adult", "Senior", "Mixed"])
rice_type = st.radio("🍚 Rice Type", ["White Rice", "Kerala Matta Rice"], horizontal=True)

# Prediction
if st.button("🧠 Predict Rice Quantity"):
    rice_amount = predict_rice_amount(
        num_people=num_people,
        appetite_level=appetite,
        meal_type=meal_type,
        guest_present=guest,
        side_dishes=side_dishes,
        avg_age_group=age_group
    )

    st.success(f"🍚 You need approximately **{rice_amount:.2f} grams** of raw rice.")

    rice_per_cup = 200  # grams per cup
    cups = rice_amount / rice_per_cup
    water_cups = cups * 2 if rice_type == "White Rice" else cups * 2.5

    rice_frac = format_fraction(cups)
    water_frac = format_fraction(water_cups)
    rice_ml = format_malayalam(cups)
    water_ml = format_malayalam(water_cups)

    st.markdown("### 🧂 Cooking Estimate:")
    st.markdown(f"""
    - 🍚 **Rice:** {rice_frac} cups  
    - 💧 **Water:** {water_frac} cups  
    """)

    # Malayalam voice line
    st.markdown("---")
    st.markdown("👵 **Ammachi Says:**")

    if rice_amount > 800:
        quote = "എത്രയൊ കുറയുന്നു! ഒരു സദ്യയ്ക്ക് വേണ്ടിയാണോ ഇത്രയും?"
    elif rice_amount < 300:
        quote = "ഇതുകൊണ്ട് നിനക്ക് മതിയാകും എന്നെ വിശ്വാസം വരില്ല."
    else:
        quote = "നന്നായി കണക്കാക്കി. ചോറിനൊപ്പം പുള്ളിശേരി കൂടി വേണമോ?"

    # Add rice/water Malayalam line
    rice_line = f"{rice_ml} കപ്പ് അരിയും {water_ml} കപ്പ് വെള്ളവുമാണ് വേണ്ടത്."
    full_message = quote + " " + rice_line

    st.info(f"“{full_message}”")

    audio_path = speak_malayalam(full_message)
    with open(audio_path, 'rb') as audio_file:
        st.audio(audio_file.read(), format='audio/mp3')
