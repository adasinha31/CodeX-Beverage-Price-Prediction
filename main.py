import streamlit as st
from prediction import predict

st.set_page_config(page_title="CodeX Beverage: Price Prediction", layout="wide")

st.title("CodeX Beverage: Price Prediction")

st.markdown("<br>", unsafe_allow_html=True)

# Row 1
col1, col2, col3, col4 = st.columns(4)

with col1:
    age = st.number_input("Age", min_value=1, max_value=100, value=30)

with col2:
    gender = st.selectbox("Gender", ["M", "F", "Other"])

with col3:
    zone = st.selectbox("Zone", ["Urban", "Rural", "Semi-Urban"])

with col4:
    occupation = st.selectbox(
        "Occupation",
        ["Working Professional", "Student", "Entrepreneur", "Retired", "Other"],
    )

# Row 2
col5, col6, col7, col8 = st.columns(4)

with col5:
    income_levels = st.selectbox(
        "Income Level (In L)",
        ["<10L", "10L-15L", "16L-25L", "26L-35L" , ">35L"],
    )

with col6:
    consume_frequency = st.selectbox(
        "Consume Frequency(weekly)",
        ["0-2 times", "3-4 times", "5-7 times"],
    )

with col7:
    current_brand = st.selectbox(
        "Current Brand",
        ["Newcomer", "Established"],
    )

with col8:
    preferable_consumption_size = st.selectbox(
        "Preferable Consumption Size",
        ["Small (250 ml)", "Medium (500 ml)", "Large (1 L)"],
    )

# Row 3
col9, col10, col11, col12 = st.columns(4)

with col9:
    awareness_of_other_brands = st.selectbox(
        "Awareness of other brands",
        ["0 to 1", "2 to 4", "Above 4"],
    )

with col10:
    reasons_for_choosing_brands = st.selectbox(
        "Reasons for choosing brands",
        ["Price", "Taste", "Availability", "Brand Reputation", "Health Benefits"],
    )

with col11:
    flavor_preference = st.selectbox(
        "Flavor Preference",
        ["Traditional", "Fruity", "Citrus", "Mint", "Others"],
    )

with col12:
    purchase_channel = st.selectbox(
        "Purchase Channel",
        ["Online", "Retail Store"],
    )

# Row 4 (3 items)
col13, col14, col15, _ = st.columns(4)

with col13:
    packaging_preference = st.selectbox(
        "Packaging Preference",
        ["Simple","Premium", "Compact & Portable"],
    )

with col14:
    health_concerns = st.selectbox(
        "Health Concerns",
        ["Low (Not very concerned)", "Medium(Moderately health-conscious)", "High (Very concerned)"],
    )

with col15:
    typical_consumption_situations = st.selectbox(
        "Typical Consumption Situations",
        [
            "Active (eg. Sports, gym)",
            "Social Gatherings",
            "Work/Study",
            "Relaxing at Home",
        ],
    )

st.markdown("<br>", unsafe_allow_html=True)


input_data = {
    "age": age,
    "gender": gender,
    "zone": zone,
    "occupation": occupation,
    "income_levels": income_levels,
    "consume_frequency(weekly)": consume_frequency,
    "current_brand": current_brand,
    "preferable_consumption_size": preferable_consumption_size,
    "awareness_of_other_brands": awareness_of_other_brands,
    "reasons_for_choosing_brands": reasons_for_choosing_brands,
    "flavor_preference": flavor_preference,
    "purchase_channel": purchase_channel,
    "packaging_preference": packaging_preference,
    "health_concerns": health_concerns,
    "typical_consumption_situations": typical_consumption_situations,
}

if st.button('Calculate Price Range'):
    prediction = predict(input_data)
    if prediction == 0:
        price_range = '50-100'
    elif prediction == 1:
        price_range = '100-150'
    elif prediction == 2:
        price_range = '150-200'
    elif prediction == 3:
        price_range = '200-250'
    else :
        st.warning('Unable to predict price')

    if price_range:
        st.write(f'Beverage Price Range: {price_range} ')


