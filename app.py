import os
import pickle
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu


# Set page configuration
st.set_page_config(
    page_title="Multiple Disease Prediction & Doctor Recommendation",
    layout="wide",
    page_icon="🧑‍⚕️"
)

# Caching data to prevent reloading on every interaction
@st.cache_resource
def load_doctors_data():
    doctors_df_path = os.path.join('dataset', 'doctors.datasets.csv')
    try:
        return pd.read_csv(doctors_df_path)
    except FileNotFoundError:
        st.error("Doctors dataset file not found.")
        return pd.DataFrame()

doctors_df = load_doctors_data()

# Load models and cache them
@st.cache_resource
def load_models():
    models = {}
    model_files = {
        'diabetes': 'diabetes_model.sav',
        'heart_disease': 'heart_disease_model.sav',
        'parkinsons': 'parkinsons_model.sav'
    }
    for model_name, model_file in model_files.items():
        model_path = os.path.join('saved_models', model_file)
        try:
            with open(model_path, 'rb') as f:
                models[model_name] = pickle.load(f)
        except FileNotFoundError:
            st.error(f"{model_name.capitalize()} model file not found.")
            models[model_name] = None
    return models

models = load_models()

# Define doctor recommendation function
def get_doctor_recommendation(disease):
    disease_to_specialization = {
        'Diabetes': 'Endocrinologist',
        'Heart Disease': 'Cardiologist',
        'Parkinson\'s Disease': 'Neurologist'
    }
    specialization = disease_to_specialization.get(disease)
    
    if specialization is None:
        return 'Consult a general physician for further advice.'
    
    if doctors_df.empty or 'Specialization' not in doctors_df.columns:
        return "Doctors dataset is empty or missing 'Specialization' column."
    
    matching_doctors = doctors_df[doctors_df['Specialization'] == specialization]
    
    if matching_doctors.empty:
        return f"No doctors found for specialization: {specialization}"
    
    doctor_info = matching_doctors.iloc[0]
    return f"Doctor: {doctor_info.get('Name', 'N/A')}, Contact: {doctor_info.get('Contact', 'N/A')}, Hospital: {doctor_info.get('Hospital', 'N/A')}"

# Function to handle user input with selectors
def get_select_input(label, options, key, placeholder="Select an option"):
    return st.selectbox(label, options, key=key, placeholder=placeholder)

# Sidebar navigation
with st.sidebar:
    st.header("Select Prediction Type")
    selected = option_menu(
        'Multiple Disease Prediction System',
        ['Diabetes Prediction', 'Heart Disease Prediction', "Parkinson's Prediction"],
        icons=['activity', 'heart', 'person'],
        default_index=0
    )

# Diabetes Prediction Page
if selected == 'Diabetes Prediction':
    st.title('Diabetes Prediction using ML')
    st.write("Enter the required information and click on 'Predict' to get the results.")

    with st.expander("Input Details"):
        col1, col2, col3 = st.columns(3)
        with col1:
            Pregnancies = get_select_input('Number of Pregnancies', list(range(0, 21)), key='Pregnancies')
        with col2:
            Glucose = get_select_input('Glucose Level', list(range(0, 201)), key='Glucose')
        with col3:
            BloodPressure = get_select_input('Blood Pressure value', list(range(0, 181)), key='BloodPressure')
        with col1:
            SkinThickness = get_select_input('Skin Thickness value', list(range(0, 101)), key='SkinThickness')
        with col2:
            Insulin = get_select_input('Insulin Level', list(range(0, 901)), key='Insulin')
        with col3:
            BMI = get_select_input('BMI value', [round(x * 0.1, 1) for x in range(0, 601)], key='BMI')
        with col1:
            DiabetesPedigreeFunction = get_select_input('Diabetes Pedigree Function value', [round(x * 0.01, 2) for x in range(0, 251)], key='DiabetesPedigreeFunction')
        with col2:
            Age = get_select_input('Age of the Person', list(range(0, 121)), key='Age')

    if st.button('Diabetes Test Result'):
        with st.spinner('Processing your request...'):
            user_input = [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]
            
            if models['diabetes']:
                diab_prediction = models['diabetes'].predict([user_input])
                diab_diagnosis = 'The person is diabetic' if diab_prediction[0] == 1 else 'The person is not diabetic'
                st.success(diab_diagnosis)
                
                if diab_prediction[0] == 1:
                    doctor_recommendation = get_doctor_recommendation('Diabetes')
                    st.info(f"Recommended Doctor: {doctor_recommendation}")
            else:
                st.error("Diabetes model is not loaded.")

# Heart Disease Prediction Page
if selected == 'Heart Disease Prediction':
    st.title('Heart Disease Prediction using ML')
    st.write("Enter the required information and click on 'Predict' to get the results.")

    with st.expander("Input Details"):
        col1, col2, col3 = st.columns(3)
        with col1:
            age = get_select_input('Age', list(range(0, 121)), key='age')
        with col2:
            sex = get_select_input('Sex', [0, 1], key='sex')  # 0: Female, 1: Male
        with col3:
            cp = get_select_input('Chest Pain types', [0, 1, 2, 3], key='cp')
        with col1:
            trestbps = get_select_input('Resting Blood Pressure', list(range(0, 201)), key='trestbps')
        with col2:
            chol = get_select_input('Serum Cholesterol in mg/dl', list(range(100, 601)), key='chol')
        with col3:
            fbs = get_select_input('Fasting Blood Sugar > 120 mg/dl', [0, 1], key='fbs')
        with col1:
            restecg = get_select_input('Resting Electrocardiographic results', [0, 1, 2], key='restecg')
        with col2:
            thalach = get_select_input('Maximum Heart Rate achieved', list(range(50, 251)), key='thalach')
        with col3:
            exang = get_select_input('Exercise Induced Angina', [0, 1], key='exang')
        with col1:
            oldpeak = get_select_input('ST depression induced by exercise', [round(x * 0.1, 1) for x in range(0, 61)], key='oldpeak')
        with col2:
            slope = get_select_input('Slope of the peak exercise ST segment', [0, 1, 2], key='slope')
        with col3:
            ca = get_select_input('Major vessels colored by fluoroscopy', [0, 1, 2, 3], key='ca')
        with col1:
            thal = get_select_input('Thalassemia', [0, 1, 2], key='thal')

    if st.button('Heart Disease Test Result'):
        with st.spinner('Processing your request...'):
            user_input = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]
            
            if models['heart_disease']:
                heart_prediction = models['heart_disease'].predict([user_input])
                heart_diagnosis = 'The person has heart disease' if heart_prediction[0] == 1 else 'The person does not have heart disease'
                st.success(heart_diagnosis)
                
                if heart_prediction[0] == 1:
                    doctor_recommendation = get_doctor_recommendation('Heart Disease')
                    st.info(f"Recommended Doctor: {doctor_recommendation}")
            else:
                st.error("Heart disease model is not loaded.")

# Parkinson's Prediction Page
if selected == "Parkinson's Prediction":
    st.title("Parkinson's Disease Prediction using ML")
    st.write("Enter the required information and click on 'Predict' to get the results.")

    with st.expander("Input Details"):
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            fo = get_select_input('MDVP:Fo(Hz)', [round(x * 1.0, 1) for x in range(100, 301)], key='fo')
        with col2:
            fhi = get_select_input('MDVP:Fhi(Hz)', [round(x * 1.0, 1) for x in range(100, 501)], key='fhi')
        with col3:
            flo = get_select_input('MDVP:Flo(Hz)', [round(x * 1.0, 1) for x in range(50, 301)], key='flo')
        with col4:
            jitter_percent = get_select_input('MDVP:Jitter(%)', [round(x * 0.01, 2) for x in range(0, 101)], key='jitter_percent')
        with col5:
            jitter_abs = get_select_input('MDVP:Jitter(Abs)', [round(x * 0.00001, 6) for x in range(0, 101)], key='jitter_abs')
        with col1:
            rap = get_select_input('MDVP:RAP', [round(x * 0.001, 3) for x in range(0, 101)], key='rap')
        with col2:
            ppq = get_select_input('MDVP:PPQ', [round(x * 0.001, 3) for x in range(0, 101)], key='ppq')
        with col3:
            ddp = get_select_input('Jitter:DDP', [round(x * 0.01, 2) for x in range(0, 101)], key='ddp')
        with col4:
            shimmer = get_select_input('MDVP:Shimmer', [round(x * 0.01, 2) for x in range(0, 101)], key='shimmer')
        with col5:
            shimmer_db = get_select_input('MDVP:Shimmer(dB)', [round(x * 0.1, 1) for x in range(0, 101)], key='shimmer_db')
        # Adding missing features
        with col1:
            shimmer_apq3 = get_select_input('Shimmer APQ3', [round(x * 0.01, 2) for x in range(0, 101)], key='shimmer_apq3')
        with col2:
            shimmer_apq5 = get_select_input('Shimmer APQ5', [round(x * 0.01, 2) for x in range(0, 101)], key='shimmer_apq5')
        with col3:
            mdvp_apq = get_select_input('MDVP APQ', [round(x * 0.01, 2) for x in range(0, 101)], key='mdvp_apq')
        with col4:
            nhr = get_select_input('NHR', [round(x * 0.001, 3) for x in range(0, 101)], key='nhr')
        with col5:
            hnr = get_select_input('HNR', [round(x * 1.0, 1) for x in range(0, 501)], key='hnr')
        with col1:
            rpde = get_select_input('RPDE', [round(x * 0.001, 3) for x in range(0, 101)], key='rpde')
        with col2:
            dfa = get_select_input('DFA', [round(x * 0.001, 3) for x in range(0, 101)], key='dfa')
        with col3:
            spread1 = get_select_input('Spread1', [round(x * 0.001, 3) for x in range(0, 101)], key='spread1')
        with col4:
            spread2 = get_select_input('Spread2', [round(x * 0.001, 3) for x in range(0, 101)], key='spread2')
        with col5:
            d2 = get_select_input('D2', [round(x * 0.001, 3) for x in range(0, 101)], key='d2')
        with col1:
            ppe = get_select_input('PPE', [round(x * 0.001, 3) for x in range(0, 101)], key='ppe')
        with col2:
            shimmer_dda = get_select_input('Shimmer DDA', [round(x * 0.01, 2) for x in range(0, 101)], key='shimmer_dda')

    if st.button("Parkinson's Test Result"):
        with st.spinner('Processing your request...'):
            user_input = [
                fo, fhi, flo, jitter_percent, jitter_abs, rap, ppq, ddp, shimmer, shimmer_db,
                shimmer_apq3, shimmer_apq5, mdvp_apq, nhr, hnr, rpde, dfa, spread1, spread2, d2, ppe, shimmer_dda
            ]

            if models['parkinsons']:
                try:
                    # Predict with the model
                    parkinsons_prediction = models['parkinsons'].predict([user_input])
                    parkinsons_diagnosis = 'The person has Parkinson\'s disease' if parkinsons_prediction[0] == 1 else 'The person does not have Parkinson\'s disease'
                    st.success(parkinsons_diagnosis)

                    if parkinsons_prediction[0] == 1:
                        doctor_recommendation = get_doctor_recommendation('Parkinson\'s Disease')
                        st.info(f"Recommended Doctor: {doctor_recommendation}")
                except ValueError as e:
                    st.error(f"Model input error: {e}")
            else:
                st.error("Parkinson's model is not loaded.")
