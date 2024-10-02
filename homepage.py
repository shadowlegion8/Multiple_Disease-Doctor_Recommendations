import streamlit as st
from streamlit_option_menu import option_menu

# Set page configuration
st.set_page_config(
    page_title="Homepage - Disease Prediction & Doctor Recommendation",
    layout="wide",
    page_icon="icons.jpg"
)

# Sidebar navigation
with st.sidebar:
    selected = option_menu(
        'Navigation',
        ['Home', 'Multiple Disease Prediction & Doctor Recommendation'],
        icons=['house', 'activity'],
        default_index=0
    )

# Home page content
if selected == 'Home':
    st.title('Welcome to the Disease Prediction & Doctor Recommendation System')
    st.write("This application helps you predict the likelihood of certain diseases based on your input "
             "and provides recommendations for doctors based on the predicted diseases. "
             "Please select the appropriate option from the sidebar to get started.")

    st.markdown("---")
    st.write("Developed by Abdul Malik Khan")
