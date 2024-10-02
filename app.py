import os
import pickle
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import base64

# Set page configuration
st.set_page_config(
    page_title="Disease Prediction & Doctor Recommendation",
    layout="wide",
    page_icon="icons.jpg"
)

# Adding custom CSS for background image using base64
def set_background_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        st.markdown(
            f"""
            <style>
            .stApp {{
                background: url('data:image/png;base64,{encoded_image}');
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
                height: 100vh;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

# Set background image
set_background_image('Images/doctor.png')

# Load doctors data
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
        'diabetes_disease': 'diabetes_disease_model.sav',
        'heart_disease': 'heart_disease_model.sav',
        'parkinsons_disease': 'parkinsons_disease_model.sav'
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
        'Multiple Disease Prediction & Doctor Recommendation System',
        ['Home', 'Diabetes Disease Prediction', 'Heart Disease Prediction', "Parkinson's Disease Prediction", "Symptom-based Prediction"],
        icons=['house', 'activity', 'heart', 'person', 'stethoscope'],
        default_index=0
    )

# Home Page Content
if selected == 'Home':
    st.title('Welcome to the Disease Prediction & Doctor Recommendation System')
    st.write("This application helps you predict the likelihood of certain diseases based on your input "
             "and provides recommendations for doctors based on the predicted diseases. "
             "Please select the appropriate option from the sidebar to get started.")
    st.write("Developed by Abdul Malik Khan")

# Symptom-based Prediction Page
if selected == 'Symptom-based Prediction':
    st.title('Symptom-based Disease Prediction')

    # Define symptoms for each disease
    diabetes_disease_symptoms = ['Frequent urination', 'Increased thirst', 'Unexplained weight loss', 'Fatigue', 'Blurred vision']
    heart_disease_symptoms = ['Chest pain', 'Shortness of breath', 'Fatigue', 'Swollen legs/feet', 'Irregular heartbeat']
    parkinsons_disease_symptoms = ['Tremors', 'Slowed movement', 'Rigid muscles', 'Impaired posture', 'Speech changes']

    st.write("Select the symptoms you're experiencing:")

    with st.expander("Input Symptoms"):
        selected_diabetes_disease_symptoms = st.multiselect('Diabetes Symptoms', diabetes_disease_symptoms, key='diabetes_disease_symptoms')
        selected_heart_disease_symptoms = st.multiselect('Heart Disease Symptoms', heart_disease_symptoms, key='heart_disease_symptoms')
        selected_parkinsons_symptoms = st.multiselect("Parkinson's Disease Symptoms", parkinsons_disease_symptoms, key='parkinsons_disease_symptoms')

    # Symptom-based Disease Prediction
    if st.button('Predict Disease based on Symptoms'):
        with st.spinner('Processing your request...'):
            disease = None
            if len(selected_diabetes_disease_symptoms) >= 3:
                disease = 'Diabetes'
            elif len(selected_heart_disease_symptoms) >= 3:
                disease = 'Heart Disease'
            elif len(selected_parkinsons_symptoms) >= 3:
                disease = 'Parkinson\'s Disease'

            if disease:
                st.success(f"You may have {disease} based on the selected symptoms.")
                doctor_recommendation = get_doctor_recommendation(disease)
                st.info(f"Recommended Doctor: {doctor_recommendation}")
            else:
                st.error("Not enough symptoms selected for a disease prediction. Please select at least three symptoms for one of the diseases.")
    st.markdown("---")
    st.write("Developed by Abdul Malik Khan")

# Diabetes Prediction Page
if selected == 'Diabetes Disease Prediction':
    st.title('Diabetes Disease Prediction using ML')
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
            
            if models['diabetes_disease']:
                diab_prediction = models['diabetes_disease'].predict([user_input])
                diab_diagnosis = 'The person is diabetic' if diab_prediction[0] == 1 else 'The person is not diabetic'
                st.success(diab_diagnosis)
                
                if diab_prediction[0] == 1:
                    doctor_recommendation = get_doctor_recommendation('Diabetes')
                    st.info(f"Recommended Doctor: {doctor_recommendation}")
            else:
                st.error("Diabetes disease model is not loaded.")

    st.markdown("---")  # Optional: Adds a horizontal line for separation
    st.write("Developed by Abdul Malik Khan")  # Your name                 

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
            chol = get_select_input('Serum Cholesterol', list(range(0, 601)), key='chol')
        with col3:
            fbs = get_select_input('Fasting Blood Sugar', [0, 1], key='fbs')  # 0: < 120 mg/dl, 1: > 120 mg/dl
        with col1:
            restecg = get_select_input('Resting ECG results', [0, 1, 2], key='restecg')  # 0: Normal, 1: Abnormal, 2: ST-T wave abnormality
        with col2:
            thalach = get_select_input('Maximum Heart Rate Achieved', list(range(0, 201)), key='thalach')
        with col3:
            exang = get_select_input('Exercise Induced Angina', [0, 1], key='exang')  # 0: No, 1: Yes
        with col1:
            oldpeak = get_select_input('Oldpeak', [round(x * 0.1, 1) for x in range(0, 101)], key='oldpeak')
        with col2:
            slope = get_select_input('Slope of the Peak Exercise ST Segment', [0, 1, 2], key='slope')
        with col3:
            ca = get_select_input('Number of Major Vessels Colored by Fluoroscopy', [0, 1, 2, 3], key='ca')
        with col1:
            thal = get_select_input('Thalassemia', [0, 1, 2, 3], key='thal')
        with col2:
            target = get_select_input('Target Variable (Heart Disease)', [0, 1], key='target')  # 0: No, 1: Yes

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

    st.markdown("---")  # Optional: Adds a horizontal line for separation
    st.write("Developed by Abdul Malik Khan")  # Your name 

# Parkinson's Disease Prediction Page
if selected == "Parkinson's Disease Prediction":
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

            if models['parkinsons_disease']:
                parkinsons_prediction = models['parkinsons_disease'].predict([user_input])
                parkinsons_diagnosis = 'The person has Parkinson\'s disease' if parkinsons_prediction[0] == 1 else 'The person does not have Parkinson\'s disease'
                st.success(parkinsons_diagnosis)

                if parkinsons_prediction[0] == 1:
                    doctor_recommendation = get_doctor_recommendation('Parkinson\'s Disease')
                    st.info(f"Recommended Doctor: {doctor_recommendation}")
            else:
                st.error("Parkinson's disease model is not loaded.")

    st.markdown("---")  # Optional: Adds a horizontal line for separation
    st.write("Developed by Abdul Malik Khan")  # Your name 
