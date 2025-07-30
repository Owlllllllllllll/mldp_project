import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load trained model
model = joblib.load('student_prediction_model.pkl')

# App Title & Description
st.set_page_config(page_title="Student Performance Predictor", layout="centered")
st.title("🎓 Student Performance Predictor")
st.markdown("This tool helps to predict whether a student are going to passing or failing based on their learning behaviors and background.")

st.divider()

# --- Sidebar Inputs ---
st.sidebar.header("📋 Enter Student Data")

# Dropdown options
regions = ['East Midlands', 'Ireland', 'London', 'North', 'South East', 'Scotland']
education_levels = ['No Formal qualifications', 'Lower Than A Level', 'Higher Education Qualification', 'Post Graduate Qualification']
age_bands = ['0-35', '35-55', '>55']
imd_bands = list(range(1, 11))  # 1 to 10

# Input fields
gender = st.sidebar.radio('⚧ Gender', ['Male', 'Female'], horizontal=True)
age_band = st.sidebar.selectbox('📅 Age Band', age_bands)
disability = st.sidebar.radio('♿ Disability', ['No', 'Yes'], horizontal=True)
region = st.sidebar.selectbox('📍 Region', regions)
highest_education = st.sidebar.selectbox('🎓 Highest Education Level', education_levels)
studied_credits = st.sidebar.selectbox('📚 Studied Credits', [30, 60, 120, 240])
num_of_prev_attempts = st.sidebar.number_input('🔁 Number of Previous Attempts', min_value=0, max_value=10, value=0)
sum_click = st.sidebar.slider('🖱️ Total Platform Clicks', min_value=0, max_value=20000, value=1000, step=1)
imd_band = st.sidebar.selectbox('🏘️ IMD Band (1 = most deprived, 10 = least)', imd_bands)

# Show note if region is outside England
if region in ['Ireland', 'Scotland']:
    st.sidebar.info("IMD Band applies mainly to regions in England. Select based on your judgment.")


# Calculate engagement level
def calculate_engagement(clicks):
    if clicks <= 100:
        return 'Low'
    elif clicks <= 1000:
        return 'Moderate'
    elif clicks <= 10000:
        return 'High'
    else:
        return 'Very High'

engagement_level = calculate_engagement(sum_click)

# --- Display engagement level live ---
st.subheader("📊 Engagement Summary")
emoji_map = {
    'Low': '😴',
    'Moderate': '🙂',
    'High': '💪',
    'Very High': '🚀'
}
st.metric("Engagement Level", f"{engagement_level} {emoji_map[engagement_level]}")

st.markdown("---")

# --- Predict Button ---
if st.button("🔍 Predict Student Result"):
    # Build input dictionary
    input_data = {
        'imd_band': [imd_band],
        'num_of_prev_attempts': [num_of_prev_attempts],
        'studied_credits': [studied_credits],
        'sum_click': [sum_click],
        'gender_M': [gender == 'Male'],
        'disability_Y': [disability == 'Yes'],
        'engagement_level_Moderate': [engagement_level == 'Moderate'],
        'engagement_level_High': [engagement_level == 'High'],
        'engagement_level_Very High': [engagement_level == 'Very High'],
        'region_East Midlands Region': [region == 'East Midlands'],
        'region_Ireland': [region == 'Ireland'],
        'region_London Region': [region == 'London'],
        'region_North Region': [region == 'North'],
        'region_Scotland': [region == 'Scotland'],
        'region_South East Region': [region == 'South East'],
        'highest_education_No Formal Qualifications': [highest_education == 'No Formal quals'],
        'highest_education_Lower Than A Level': [highest_education == 'Lower Than A Level'],
        'highest_education_Higher Education Qualification': [highest_education == 'HE Qualification'],
        'highest_education_Post Graduate Qualification': [highest_education == 'Post Graduate Qualification'],
        'age_band_35-55': [age_band == '35-55'],
        'age_band_>55': [age_band == '55<=']
    }

    df_input = pd.DataFrame(input_data)
    df_input = df_input.reindex(columns=model.feature_names_in_, fill_value=0)

    prediction = model.predict(df_input)[0]

    label_map = {
        0: "❌ Fail",
        1: "✅ Pass"
    }

    st.success(f"🧠 Predicted Final Result: **{label_map.get(prediction, prediction)}**")

# --- Styling ---

st.markdown(
    """
    <style>
        .stApp {
            background-image: url("https://i0.wp.com/codemyui.com/wp-content/uploads/2019/06/Shooting-Star-Background-in-Pure-CSS-1.gif?fit=880%2C440&ssl=1");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
        }

        /* Optional: Make main content readable */
        .stApp > div:first-child {
            background-color: rgba(0, 0, 0, 0.5);  /* dark translucent overlay */
            padding: 2rem;
            border-radius: 12px;
        }
    </style>
    """,
    unsafe_allow_html=True
)





st.divider()

st.markdown("""
The **Index of Multiple Deprivation (IMD)** ranks areas in England by relative poverty.
If you're not sure of your IMD band, you can find it here:

👉 [Find your IMD rank by postcode](https://imd-by-postcode.opendatacommunities.org/)
""")

