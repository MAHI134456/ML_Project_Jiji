# Smartphone Price Prediction and Classification

## Project Overview
This project applies machine learning techniques to analyze smartphone listings collected from Jiji Ethiopia. The goal is to build models that can both predict product prices and classify smartphones into price categories.

---

## Objectives
- Predict smartphone prices using Linear Regression.
- Classify smartphones as **Expensive** or **Affordable** using Logistic Regression.
- Perform data collection, cleaning, and exploratory data analysis (EDA).
- Evaluate model performance using appropriate metrics.

---


##  Dataset
- Source: Jiji Ethiopia (web scraped dataset)
- Total Records: **576**
- Features include:
  - Brand
  - Model
  - RAM
  - Storage
  - Condition
  - Location
  - Title (used for feature engineering)

- Target:
  - Price (Regression)
  - Price Category(Class) (Classification)

---

##  Data Preprocessing
- Handled missing values
- Encoded categorical variables
- Applied **log transformation** to reduce skewness in price
- Feature engineering from product titles
- Feature scaling using **StandardScaler**

---

##  Model Development

### 🔹 Regression Model
- Model: Linear Regression  
- RMSE: **10,225.52 ETB**  
- R² Score: **0.8965**

### 🔹 Classification Model
- Model: Logistic Regression  
- Threshold: **85,000 ETB (median-based)**  
- Accuracy: **97.3%**  
- Precision: **98.1%**  
- Recall: **96.4%**  
- F1 Score: **97.3%**

---

##  Deployment
The final system is deployed using **Streamlit**, allowing users to:
- Input smartphone features
- Get predicted price
- Receive category classification (Affordable / Expensive)

---

##  Technologies Used
- Python
- Pandas
- NumPy
- Scikit-learn
- Streamlit
- Matplotlib / Seaborn

---

## How to Run the Project

1. Clone the repository:
```bash
git clone <https://github.com/MAHI134456/ML_Project_Jiji.git>

```
2. Install dependencies:
```bash
pip install -r requirements.txt

```
3. Run the Streamlit app:
```bash 
streamlit run app.py

```