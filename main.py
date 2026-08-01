import streamlit as st
import pandas as pd
import joblib

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="🏠 New York Room  Prediction",
    layout="wide"
)

# ---------------- LOAD MODEL ----------------
@st.cache_resource
def load_model():
    return joblib.load("newYork_model.pkl")

model = load_model()

# ---------------- TITLE ----------------
st.title("🏠 New York Room  Prediction")
st.markdown("Enter the property details and click **Predict**.")

# ---------------- FORM ----------------
with st.form("prediction_form"):

    col1, col2 = st.columns(2)

    with col1:
        latitude = st.number_input(
            "📍 Latitude",
            value=40.7128,
            format="%.6f"
        )

        longitude = st.number_input(
            "📍 Longitude",
            value=-74.0060,
            format="%.6f"
        )

        price = st.number_input(
            "💲 Price",
            min_value=0.0,
            value=100.0
        )

        minimum_nights = st.number_input(
            "🌙 Minimum Nights",
            min_value=1,
            value=1
        )

        number_of_reviews = st.number_input(
            "⭐ Number of Reviews",
            min_value=0,
            value=0
        )

    with col2:

        reviews_per_month = st.number_input(
            "📈 Reviews Per Month",
            min_value=0.0,
            value=0.0
        )

        calculated_host_listings_count = st.number_input(
            "🏠 Host Listings Count",
            min_value=1,
            value=1
        )

        availability_365 = st.slider(
            "📅 Availability (Days)",
            0,
            365,
            180
        )

        neighbourhood_group = st.selectbox(
            "🏙️ Neighbourhood Group",
            [
                "Bronx",
                "Brooklyn",
                "Manhattan",
                "Queens",
                "Staten Island"
            ]
        )

        neighbourhood = st.text_input(
            "📍 Neighbourhood",
            "Williamsburg"
        )

    submit = st.form_submit_button("🔮 Predict Room Type")

# ---------------- PREDICTION ----------------
if submit:

    input_df = pd.DataFrame({
        "latitude": [latitude],
        "longitude": [longitude],
        "price": [price],
        "minimum_nights": [minimum_nights],
        "number_of_reviews": [number_of_reviews],
        "reviews_per_month": [reviews_per_month],
        "calculated_host_listings_count": [calculated_host_listings_count],
        "availability_365": [availability_365],
        "neighbourhood_group": [neighbourhood_group],
        "neighbourhood": [neighbourhood]
    })

    with st.spinner("🔄 Predicting..."):

        prediction = model.predict(input_df)[0]
       

    st.success("✅ Prediction Completed Successfully")
    print(prediction)

    try:
        prediction = float(prediction)

        st.metric(
            "🏠 Predicted Value",
            f"${prediction:,.2f}"
        )

    except:
        st.metric(
            "🏠 Prediction",
            str(prediction)
        )

    st.subheader("📋 Input Data")
    st.dataframe(input_df, use_container_width=True)

    st.subheader("🤖 Raw Prediction")
    st.write(prediction)

