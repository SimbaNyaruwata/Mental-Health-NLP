import json
import os
import streamlit as st
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text as text
from tensorflow.keras.models import load_model
from streamlit_login_auth_ui.widgets import __login__
from streamlit_lottie import st_lottie
import requests
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import A4, A3, legal, TABLOID
from reportlab.pdfgen import canvas

from datetime import datetime




# Disable GPU if necessary
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

# Function to create a login object based on user role
def create_login_obj(is_admin):
    auth_token = "admin_auth_token" if is_admin else "courier_auth_token"
    cookie_prefix = "streamlit_login_ui_admin_cookies" if is_admin else "streamlit_login_ui_user_cookies"
    
    return __login__(
        auth_token=auth_token,
        company_name="Shims",
        width=200,
        height=250,
        logout_button_name='Logout',
        hide_menu_bool=False,
        hide_footer_bool=False,
        lottie_url='https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json',
        cookie_prefix=cookie_prefix
    )

# Function to determine if a user is admin based on JSON data
def is_admin_user(json_file, username):
    try:
        with open(json_file, 'r') as file:
            users_data = json.load(file)
        
        # Check if the username matches an admin user in the JSON data
        for user in users_data:
            if user.get('username') == username:
                return user.get('role') == "admin"
                
        return False
        
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error accessing JSON file: {e}")
        return False

def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Admin logic
def admin_logic(__login_obj):
    st.markdown('<h1 style="font-size:32px;">Mental Health NLP System (Admin)</h1>', unsafe_allow_html=True)
    username = __login_obj.get_username()  # Get the admin username
    
    lottie_admin_animation = load_lottie_url("https://lottie.host/7fbc394e-113d-4e09-ac49-d8de2a6e685a/X73Vfky0wN.json")
    st_lottie(lottie_admin_animation, height=175, key="admin_animation")
    st.write(f"Welcome, {username}")
    # Admin-specific features would go here

     # Load user data from user_db.json
    try:
        user_data = pd.read_json("user_db.json")
    except FileNotFoundError:
        st.error("User data not found.")
        return
    
    # Button to download CSV report
    if st.button("Download CSV Report"):
        csv_data = user_data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download as CSV",
            data=csv_data,
            file_name="user_data_report.csv",
            mime="text/csv"
        )
    
    # Button to download PDF report
    if st.button("Download PDF Report"):
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=TABLOID)
        
        # Add user data to PDF
        pdf.drawString(100, 750, "User Data Report")
        pdf.drawString(100, 730, f"Admin: {username}")
        
        y_position = 700
        for i, row in user_data.iterrows():
            row_text = f"Username: {row['username']}, Phone: {row['phone']}, Address: {row['address']}, Sentiment: {row['sentiment']}, Login Time: {row['login_time']}"
            pdf.drawString(100, y_position, row_text)
            y_position -= 20
            if y_position < 100:  # Start new page if space runs out
                pdf.showPage()
                y_position = 750
        
        pdf.save()
        buffer.seek(0)
        
        # Create a download button for the PDF
        st.download_button(
            label="Download as PDF",
            data=buffer,
            file_name="user_data_report.pdf",
            mime="application/pdf"
        )
# User logic
def user_logic(username):
    st.markdown('<h1 style="font-size:32px;">Mental Health NLP System</h1>', unsafe_allow_html=True)
    lottie_animation = load_lottie_url("https://lottie.host/7fbc394e-113d-4e09-ac49-d8de2a6e685a/X73Vfky0wN.json")
    st_lottie(lottie_animation, height=175, key="user_animation")
    
    custom_objects = {'KerasLayer': hub.KerasLayer}
    model_path = 'C:/Users/tapiw/Documents/Projects/Sharon/Mental Health NLP/mental_health_model.h5'
    model = load_model(model_path, custom_objects=custom_objects)

    text_input = st.text_input('Enter your mental health sentiment:')
    result = st.empty()

    sentiment_mapping = {
        0: 'Anxiety', 1: 'Bipolar', 2: 'Depression',
        3: 'Normal', 4: 'Personality disorder', 5: 'Stress', 6: 'Suicidal'
    }

    support_recommendations = {
        'Anxiety': 'Consider practicing mindfulness, relaxation exercises, or seeking therapy.',
        'Bipolar': 'Please consult a mental health professional for a proper diagnosis and treatment plan.',
        'Depression': 'Reach out to a therapist or counselor. Consider joining support groups.',
        'Normal': 'Your mental health appears to be stable, which is fantastic! Remember to continue prioritising your well being by maintaining a healthy routine, staying connected with friends and family',
        'Personality disorder': 'Consult with a mental health expert to explore therapeutic options like DBT or CBT.',
        'Stress': 'Try stress management techniques like meditation, yoga, or talking to someone.',
        'Suicidal': 'Seek immediate support from a crisis helpline: Samaritans 080 12 333 333 or a trusted professional. You are not alone.'
    }
    def make_prediction(text):
        input_tensor = tf.convert_to_tensor([text])
        outputs = model.predict(input_tensor)
        sentiment_numeric = tf.argmax(outputs, axis=1).numpy()[0]
        sentiment_status = sentiment_mapping.get(sentiment_numeric, "Unknown")
        return sentiment_status
    
    if st.button('Submit'):
        sentiment = make_prediction(text_input)
        st.write(f'Sentiment: {sentiment}')
        recommendation = support_recommendations.get(sentiment, "No specific recommendation available.")
        st.write(f"Support Recommendation: {recommendation}")

        save_user_details(username, sentiment)

def save_user_details(username: str, sentiment: str) -> None:
    """
    Saves the details of a logged-in user, including username, address, phone, and login time,
    to 'user_db.json' for later viewing by an admin.
    """
    # Load user details from _secret_auth_.json
    try:
        with open('_secret_auth_.json', 'r') as auth_file:
            users_data = json.load(auth_file)

        # Find the user's information in the file
        user_info = next((user for user in users_data if user.get("username") == username), None)
        if user_info is None:
            print(f"User '{username}' not found in _secret_auth_.json.")
            return
        
        # Prepare the new user data with current time and date
        new_user_data = {
            'username': user_info['username'],
            'phone': user_info.get('phone', 'N/A'),
            'address': user_info.get('address', 'N/A'),
            'sentiment':sentiment,
            'login_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Append this data to user_db.json
        with open("user_db.json", "r+") as user_db_file:
            try:
                authorized_user_data = json.load(user_db_file)
            except json.JSONDecodeError:
                authorized_user_data = []

            # Add new data and write it back to the file
            authorized_user_data.append(new_user_data)
            user_db_file.seek(0)
            json.dump(authorized_user_data, user_db_file, indent=4)

    except FileNotFoundError:
        print("One of the JSON files was not found.")
    except json.JSONDecodeError:
        print("Error reading JSON data.")

# Main function to handle user login and role-based display
def main():
    json_file = '_secret_auth_.json'
    __login_obj = create_login_obj(is_admin=False)  # Create general login object initially
    LOGGED_IN = __login_obj.build_login_ui()
    
    if LOGGED_IN:
        username = __login_obj.get_username()
        is_admin = is_admin_user(json_file, username)
        
        #st.write(f"Logged-in user: {username}")
        #st.write(f"Is Admin: {is_admin}")

         # Save user details to user_db.json upon login
        

        # Admin or user logic based on role
        if is_admin:
            admin_logic(__login_obj)
        else:
            user_logic(username)

# Run the main function
main()


