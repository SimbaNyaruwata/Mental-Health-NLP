import streamlit as st
import json
import os
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
from streamlit_cookies_manager import EncryptedCookieManager
#from .utils import check_admin_pass
from .utils import check_usr_pass
from .utils import load_lottieurl
from .utils import check_valid_name
from .utils import check_valid_email
from .utils import check_unique_email
from .utils import check_unique_usr
from .utils import register_new_usr
from .utils import check_email_exists
from .utils import generate_random_passwd
from .utils import send_passwd_in_email
from .utils import change_passwd
from .utils import check_current_passwd
#from app4 import is_admin_user




class __login__:
    """
    Builds the UI for the Login/ Sign Up page.
    """

    def __init__(self, auth_token: str, company_name: str, width, height, logout_button_name: str = 'Logout', hide_menu_bool: bool = False, hide_footer_bool: bool = False, lottie_url: str = "https://assets8.lottiefiles.com/packages/lf20_ktwnwv5m.json", cookie_prefix: str = "streamlit_login_ui_yummy_cookies", key=None ):
        """
        Arguments:
        -----------
        1. self
        2. auth_token : The unique authorization token received from - https://www.courier.com/email-api/
        3. company_name : This is the name of the person/ organization which will send the password reset email.
        4. width : Width of the animation on the login page.
        5. height : Height of the animation on the login page.
        6. logout_button_name : The logout button name.
        7. hide_menu_bool : Pass True if the streamlit menu should be hidden.
        8. hide_footer_bool : Pass True if the 'made with streamlit' footer should be hidden.
        9. lottie_url : The lottie animation you would like to use on the login page. Explore animations at - https://lottiefiles.com/featured
        """
        self.auth_token = auth_token
        self.company_name = company_name
        self.width = width
        self.height = height
        self.logout_button_name = logout_button_name
        self.hide_menu_bool = hide_menu_bool
        self.hide_footer_bool = hide_footer_bool
        self.lottie_url = lottie_url

        self.cookies = EncryptedCookieManager(
        #prefix="streamlit_login_ui_yummy_cookies",
        prefix=cookie_prefix,
        password='9d68d6f2-4258-45c9-96eb-2d6bc74ddbb5-d8f49cab-edbb-404a-94d0-b25b1d4a564b')
       
        if not self.cookies.ready():
            st.stop()   


    def check_auth_json_file_exists(self, auth_filename: str) -> bool:
        """
        Checks if the auth file (where the user info is stored) already exists.
        """
        file_names = []
        for path in os.listdir('./'):
            if os.path.isfile(os.path.join('./', path)):
                file_names.append(path)

        present_files = []
        for file_name in file_names:
            if auth_filename in file_name:
                present_files.append(file_name)
                    
            present_files = sorted(present_files)
            if len(present_files) > 0:
                return True
        return False

    def get_username(self):
                # If the login object is not initialized, set the username dynamically
        

        if st.session_state['LOGOUT_BUTTON_HIT'] == False:
            fetched_cookies = self.cookies
            if '__streamlit_login_signup_ui_username__' in fetched_cookies.keys():
                username=fetched_cookies['__streamlit_login_signup_ui_username__']
                return username
 

    def login_widget(self) -> None:
        """
        Creates the login widget, checks and sets cookies, authenticates the users.
        """

        if 'LOGGED_IN' not in st.session_state:
             st.session_state['LOGGED_IN'] = False

        if 'LOGOUT_BUTTON_HIT' not in st.session_state:
            st.session_state['LOGOUT_BUTTON_HIT'] = False

        # Checks if cookie exists.
        if st.session_state['LOGGED_IN'] == False:
            if st.session_state['LOGOUT_BUTTON_HIT'] == False:
                fetched_cookies = self.cookies
                if '__streamlit_login_signup_ui_username__' in fetched_cookies.keys():
                    if fetched_cookies['__streamlit_login_signup_ui_username__'] != '1c9a923f-fb21-4a91-b3f3-5f18e3f01182':
                        st.session_state['LOGGED_IN'] = True

        if st.session_state['LOGGED_IN'] == False:
            st.session_state['LOGOUT_BUTTON_HIT'] = False 

            del_login = st.empty()
            with del_login.form("Login Form"):
                username = st.text_input("Username", placeholder = 'Your unique username')
                password = st.text_input("Password", placeholder = 'Your password', type = 'password')

                st.markdown("###")
                login_submit_button = st.form_submit_button(label = 'Login')

                if login_submit_button == True:
                    authenticate_user_check = check_usr_pass(username, password)

                    if authenticate_user_check == False:
                        st.error("Invalid Username or Password!")

                    else:
                        st.session_state['LOGGED_IN'] = True
                        self.cookies['__streamlit_login_signup_ui_username__'] = username
                        self.cookies.save()
                        del_login.empty()
                        st.experimental_rerun()

             #   if login_submit_button==True:
             #           authenticate_user_check = check_admin_pass(username, password)
            #          st.session_state['LOGGED_IN_ADMIN'] = True
             # 3          self.cookies['__streamlit_login_signup_ui_username__'] = username
              #          self.cookies.save()
               #         del_login.empty()
                #        st.experimental_rerun()


    def animation(self) -> None:
        """
        Renders the lottie animation.
        """
        lottie_json = load_lottieurl(self.lottie_url)
        st_lottie(lottie_json, width = self.width, height = self.height)


    def sign_up_widget(self) -> None:
        """
        Creates the sign-up widget and stores the user info in a secure way in the _secret_auth_.json file.
        """
        with st.form("Sign Up Form"):
            name_sign_up = st.text_input("Name *", placeholder = 'Please enter your name')
            valid_name_check = check_valid_name(name_sign_up)

            email_sign_up = st.text_input("Email *", placeholder = 'Please enter your email')
            valid_email_check = check_valid_email(email_sign_up)
            unique_email_check = check_unique_email(email_sign_up)
            
            username_sign_up = st.text_input("Username *", placeholder = 'Enter a unique username')
            unique_username_check = check_unique_usr(username_sign_up)
            
            role = 'user'
            

            phonenum_sign_up = st.text_input("Phone number *", placeholder = 'Enter your phone number')
            unique_phonenum_check = check_unique_usr(phonenum_sign_up)

            
            address_sign_up = st.text_input("Address*", placeholder = 'Enter your address username')
            unique_address_check = check_unique_usr(address_sign_up)

            
            gender_sign_up = st.text_input("Gender *", placeholder = 'Male or Female')
            unique_gender_check = check_unique_usr(gender_sign_up)
            
            age_sign_up = st.text_input("Age *", placeholder = 'Enter your age')
            unique_age_check = check_unique_usr(age_sign_up)

            password_sign_up = st.text_input("Password *", placeholder = 'Create a strong password', type = 'password')

            st.markdown("###")
            sign_up_submit_button = st.form_submit_button(label = 'Register')

            if sign_up_submit_button:
                if valid_name_check == False:
                    st.error("Please enter a valid name!")

                elif valid_email_check == False:
                    st.error("Please enter a valid Email!")
                
                elif unique_email_check == False:
                    st.error("Email already exists!")
                
                elif unique_username_check == False:
                    st.error(f'Sorry, username {username_sign_up} already exists!')
                
                elif unique_username_check == None:
                    st.error('Please enter a non - empty Username!')

                if valid_name_check == True:
                    if valid_email_check == True:
                        if unique_email_check == True:
                            if unique_username_check == True:
                                if unique_phonenum_check ==True:
                                    if unique_address_check ==True:
                                        if unique_gender_check == True:
                                            if unique_age_check == True:
                                                register_new_usr(name_sign_up, email_sign_up, username_sign_up, role, phonenum_sign_up, address_sign_up, gender_sign_up, age_sign_up, password_sign_up)
                                st.success("Registration Successful!")


    def forgot_password(self) -> None:
        """
        Creates the forgot password widget and after user authentication (email), triggers an email to the user 
        containing a random password.
        """
        with st.form("Forgot Password Form"):
            email_forgot_passwd = st.text_input("Email", placeholder= 'Please enter your email')
            email_exists_check, username_forgot_passwd = check_email_exists(email_forgot_passwd)

            st.markdown("###")
            forgot_passwd_submit_button = st.form_submit_button(label = 'Get Password')

            if forgot_passwd_submit_button:
                if email_exists_check == False:
                    st.error("Email ID not registered with us!")

                if email_exists_check == True:
                    random_password = generate_random_passwd()
                    send_passwd_in_email(self.auth_token, username_forgot_passwd, email_forgot_passwd, self.company_name, random_password)
                    change_passwd(email_forgot_passwd, random_password)
                    st.success("Secure Password Sent Successfully!")


    def reset_password(self) -> None:
        """
        Creates the reset password widget and after user authentication (email and the password shared over that email), 
        resets the password and updates the same in the _secret_auth_.json file.
        """
        with st.form("Reset Password Form"):
            email_reset_passwd = st.text_input("Email", placeholder= 'Please enter your email')
            email_exists_check, username_reset_passwd = check_email_exists(email_reset_passwd)

            current_passwd = st.text_input("Temporary Password", placeholder= 'Please enter the password you received in the email')
            current_passwd_check = check_current_passwd(email_reset_passwd, current_passwd)

            new_passwd = st.text_input("New Password", placeholder= 'Please enter a new, strong password', type = 'password')

            new_passwd_1 = st.text_input("Re - Enter New Password", placeholder= 'Please re- enter the new password', type = 'password')

            st.markdown("###")
            reset_passwd_submit_button = st.form_submit_button(label = 'Reset Password')

            if reset_passwd_submit_button:
                if email_exists_check == False:
                    st.error("Email does not exist!")

                elif current_passwd_check == False:
                    st.error("Incorrect temporary password!")

                elif new_passwd != new_passwd_1:
                    st.error("Passwords don't match!")
            
                if email_exists_check == True:
                    if current_passwd_check == True:
                        change_passwd(email_reset_passwd, new_passwd)
                        st.success("Password Reset Successfully!")
                

    def logout_widget(self) -> None:
        """
        Creates the logout widget in the sidebar only if the user is logged in.
        """
        if st.session_state['LOGGED_IN'] == True:
            
            

            # Move the logout button below the text
            st.sidebar.markdown("---") 
            st.sidebar.write("""    
            **Mental Health Help Lines**
             - Harare: 0242 798 8555
             - Midlands: 054 798 8567
             - Bulawayo: 0292 223 4567      
             - Manicaland: 020 633 96
             - Mashonaland East: 0772 571 312
             - Mashonland West: 0772 310 361
             - Masvingo: 0712 570 133
             - Matebeleland North: 0292 865 321
             - Matebeleland South: 0292 332 176                                                                
                              
                                                                                                      
            """)
            st.sidebar.markdown("---")
            del_logout = st.sidebar.empty()
            del_logout.markdown("#")
            logout_click_check = del_logout.button(self.logout_button_name)

            if logout_click_check == True:
                st.session_state['LOGOUT_BUTTON_HIT'] = True
                st.session_state['LOGGED_IN'] = False
                self.cookies['__streamlit_login_signup_ui_username__'] = '1c9a923f-fb21-4a91-b3f3-5f18e3f01182'
                del_logout.empty()
                st.experimental_rerun()
        

    def nav_sidebar(self):

        """
        Creates the side navigation bar
            """
        
         # Initialize count if not already initialized
        if not hasattr(self, 'count'):
            self.count = 0  # Initialize count as an instance va
        
        main_page_sidebar = st.sidebar.empty()


        while True:

            count = 0
            with main_page_sidebar:
                selected_option = option_menu(
                    menu_title='Navigation',
                    menu_icon='list-columns-reverse',
                    icons=['box-arrow-in-right', 'person-plus', 'x-circle', 'arrow-counterclockwise'],
                    options=['Login', 'Create Account', 'Forgot Password?', 'Reset Password'],
                    styles={
                        "container": {"padding": "5px"},
                        "nav-link": {"font-size": "14px", "text-align": "left", "margin": "0px"}
                    },
                    key=f"nav_sidebar_{count}"  # Use a unique key for the option_menu
                )

            count +=1  # Increment count for next widget (if needed)

            break

        return main_page_sidebar, selected_option

        

    def hide_menu(self) -> None:
        """
        Hides the streamlit menu situated in the top right.
        """
        st.markdown(""" <style>
        #MainMenu {visibility: hidden;}
        </style> """, unsafe_allow_html=True)
    

    def hide_footer(self) -> None:
        """
        Hides the 'made with streamlit' footer.
        """
        st.markdown(""" <style>
        footer {visibility: hidden;}
        </style> """, unsafe_allow_html=True)

    def build_login_ui(self):
        """
        Brings everything together, calls important functions.
        """
        # Initialize session state if necessary
        if 'LOGGED_IN' not in st.session_state:
            st.session_state['LOGGED_IN'] = False

        if 'LOGOUT_BUTTON_HIT' not in st.session_state:
            st.session_state['LOGOUT_BUTTON_HIT'] = False

        auth_json_exists_bool = self.check_auth_json_file_exists('_secret_auth_.json')

        if not auth_json_exists_bool:
            with open("_secret_auth_.json", "w") as auth_json:
                json.dump([], auth_json)

        # Sidebar navigation
        main_page_sidebar, selected_option = self.nav_sidebar()

        # Handle selected option
        if selected_option == 'Login':
            c1, c2 = st.columns([7, 3])
            with c1:
                self.login_widget()
            with c2:
                if not st.session_state['LOGGED_IN']:
                    self.animation()

        elif selected_option == 'Create Account':
            self.sign_up_widget()

        elif selected_option == 'Forgot Password?':
            self.forgot_password()

        elif selected_option == 'Reset Password':
            self.reset_password()

        # Handle logout widget
        self.logout_widget()

        # Clear sidebar if logged in
        if st.session_state['LOGGED_IN']:
            main_page_sidebar.empty()

        # Hide menu and footer if required
        if self.hide_menu_bool:
            self.hide_menu()

        if self.hide_footer_bool:
            self.hide_footer()

        return st.session_state['LOGGED_IN']


    
    def build_admin_ui(self):
        """
        Brings everything together, calls important functions.
        """
        # Initialize session state if necessary
        if 'LOGGED_IN' not in st.session_state:
            st.session_state['LOGGED_IN'] = False

        if 'LOGOUT_BUTTON_HIT' not in st.session_state:
            st.session_state['LOGOUT_BUTTON_HIT'] = False

        auth_json_exists_bool = self.check_auth_json_file_exists('_secret_auth_.json')

        if not auth_json_exists_bool:
            with open("_secret_auth_.json", "w") as auth_json:
                json.dump([], auth_json)

        # Sidebar navigation
        main_page_sidebar, selected_option = self.nav_sidebar()

        # Handle selected option
        if selected_option == 'Login':
            c1, c2 = st.columns([7, 3])
            with c1:
                self.login_widget()
            with c2:
                if not st.session_state['LOGGED_IN']:
                    self.animation()

        elif selected_option == 'Create Account':
            self.sign_up_widget()

        elif selected_option == 'Forgot Password?':
            self.forgot_password()

        elif selected_option == 'Reset Password':
            self.reset_password()

        # Handle logout widget
        self.logout_widget()

        # Clear sidebar if logged in
        if st.session_state['LOGGED_IN']:
            main_page_sidebar.empty()

        # Hide menu and footer if required
        if self.hide_menu_bool:
            self.hide_menu()

        if self.hide_footer_bool:
            self.hide_footer()

        return st.session_state['LOGGED_IN']


    

# Author: Gauri Prabhakar
# GitHub: https://github.com/GauriSP10/streamlit_login_auth_ui


