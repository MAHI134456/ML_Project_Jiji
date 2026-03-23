import streamlit as st
import joblib
import pandas as pd
import numpy as np

# --- Load trained pipelines ---
reg_pipeline = joblib.load("models/reg_pipeline.pkl")
clf_pipeline = joblib.load("models/clf_pipeline.pkl")

st.set_page_config(page_title="Smartphone Price Predictor", layout="centered")
st.title("📱 Smartphone Price Predictor")

st.markdown("### Enter smartphone features:")

# --- User input ---
brand = st.selectbox("Brand", ["Samsung", "iPhone"])
storage = st.selectbox("Storage (GB)", [64, 128, 256, 512])
condition = st.selectbox("Condition", ["New", "Used"])
location = st.selectbox("Location", ["Bole", "Nifas Silk", "Other"])
model_name = st.selectbox("Model", ["iPhone 14 Pro", "Galaxy S23 Ultra", "Galaxy s26 256"])

# --- Button to predict ---
if st.button("Predict"):
    # --- Prepare input as DataFrame (strings, same columns as training) ---
    X_input = pd.DataFrame(
        [[brand, location, model_name, condition, storage]],
        columns=["Brand", "Location", "Model", "Condition", "Storage"]
    )

    # --- Predict price ---
    log_price = reg_pipeline.predict(X_input)[0]  # pipeline predicts log-price
    price = np.exp(log_price)  # convert back to actual price

    # --- Predict classification ---
    class_pred = clf_pipeline.predict(X_input)[0]

    # --- Display results ---
    st.markdown("###  Predicted Price")
    st.write(f" {price:,.0f} ETB")

    st.markdown("###  Price Category")
    if class_pred == 1:
        st.success("Expensive")
    else:
        st.info("Affordable")