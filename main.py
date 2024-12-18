import streamlit as st
import streamlit_authenticator as stauth
import streamlit_authenticator as stauth
import mysql.connector
import datetime
import re
import streamlit as st
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities.hasher import Hasher
from streamlit_authenticator.utilities import (CredentialsError,
                                               ForgotError,
                                               Hasher,
                                               LoginError,
                                               RegisterError,
                                               ResetError,
                                               UpdateError)



# MySQL Connection Parameters
HOST = st.secrets['HOST']  # Use 'localhost' for local MySQL
USER =  st.secrets['USER'] # Default MySQL username
PASSWORD =  st.secrets['PASSWORD']  # Replace with your MySQL root password
DATABASE = st.secrets['DATABASE']


st.set_page_config(page_title="LINA CHATBOT", page_icon="🐱", initial_sidebar_state='collapsed')
st.title(":blue[LINA] CHATBOT~")

st.markdown("""

    <style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:ital,wght@0,200..1000;1,200..1000&family=Open+Sans:ital,wght@0,300..800;1,300..800&family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap');        
        body{
            font-family: "Nunito", Helvetica Neue, sans-serif;
            font-weight: 400;
            font-size: 1rem;
            line-height: 1.75;

        }
        h1{
        text-align: center;
        }
        .st-emotion-cache-1jicfl2 {
            padding: 2rem 3rem 1rem;
        }
    

        h1, h2, h3, h4, h5, h6 {
            font-family: "Nunito", Helvetica Neue, sans-serif;
        }
        
        p, div, span {
            font-family: "Nunito", Helvetica Neue, sans-serif;
        }

        [data-testid="stBaseButton-secondaryFormSubmit"]{
        width: 100%;
        }
    
        [data-testid="stBaseButton-secondaryFormSubmit]{
        width: 100%;
        }


    </style>
""", unsafe_allow_html=True)

# Function to create connection to MySQL
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE,
            auth_plugin='mysql_native_password',
            charset   = 'utf8mb4',
            collation = 'utf8mb4_unicode_ci',
        )
        print("Connected to MySQL")
        return connection
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return None

# Function to insert user into MySQL
def insert_user(name, email, username, password):
    """
    Inserts Users into the MySQL database.
    :param email:
    :param username:
    :param password:
    :return: User ID Upon successful Creation
    """
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        date_joined = str(datetime.datetime.now())
        cursor.execute("INSERT INTO users (name, email, username, password, date_joined) VALUES (%s, %s, %s, %s, %s)", 
                       (name, email, username, password, date_joined))
        connection.commit()
        cursor.close()
        connection.close()
    else:
        st.error("Could not connect to the database.")

# Function to fetch all users from MySQL
def fetch_users():
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        cursor.close()
        connection.close()
        return users
    return []

# Function to get user emails from MySQL
def get_user_emails():
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT email FROM users")
        emails = [email[0] for email in cursor.fetchall()]
        cursor.close()
        connection.close()
        return emails
    return []

# Function to get user usernames from MySQL
def get_usernames():
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT username FROM users")
        usernames = [username[0] for username in cursor.fetchall()]
        cursor.close()
        connection.close()
        return usernames
    return []

# Email validation function (same as before)
def validate_email(email):
    pattern = r"^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
    return bool(re.match(pattern, email))

# Username validation function (same as before)
def validate_username(username):
    pattern = "^[a-zA-Z0-9]*$"
    return bool(re.match(pattern, username))

# Signup function (same as before but using MySQL)

def sign_up():
    with st.form(key='signup_form', clear_on_submit=True):
        st.subheader('Sign Up')
        name = st.text_input('Name', placeholder='Enter Your Name')
        email = st.text_input('Email', placeholder='Enter Your Email')
        username = st.text_input('Username', placeholder='Enter Your Username')
        password1 = st.text_input('Password', placeholder='Enter Your Password', type='password')
        password2 = st.text_input('Confirm Password', placeholder='Confirm Your Password', type='password')

        if name:
            if email:
                if validate_email(email):
                    if email not in get_user_emails():
                        if validate_username(username):
                            if username not in get_usernames():
                                if len(username) >= 2:
                                    if len(password1) >= 6:
                                        if password1 == password2:
                                            # Add User to DB
                                            hashed_password = Hasher.hash(password1)
                                            insert_user(name, email, username, hashed_password)
                                            st.success('Account created successfully!!')
                                            st.balloons()
                                        else:
                                            st.warning('Passwords Do Not Match')
                                    else:
                                        st.warning('Password is too Short')
                                else:
                                    st.warning('Username Too short')
                            else:
                                st.warning('Username Already Exists')

                        else:
                            st.warning('Invalid Username')
                    else:
                        st.warning('Email Already exists!!')
                else:
                    st.warning('Invalid Email')
       

        btn1, bt2, btn3, btn4, btn5 = st.columns(5)

        with btn3:
            st.form_submit_button('Sign Up')


# Đảm bảo lấy dữ liệu từ fetch_users()
def log_in():
    try:
        users = fetch_users()
        if users:  # Kiểm tra xem dữ liệu người dùng có hợp lệ không
            emails = []
            usernames = []
            passwords = []
            names = []

            for user in users:
                emails.append(user[2])  # Sử dụng chỉ số (0) để lấy email từ tuple
                usernames.append(user[1])  # Sử dụng chỉ số (1) để lấy username
                passwords.append(user[3])  # Sử dụng chỉ số (2) để lấy password
                names.append(user[5])

            credentials = {'usernames': {}}
            for index in range(len(emails)):
                credentials['usernames'][usernames[index]] = {
                    'username': usernames[index], 
                    'password': passwords[index],  
                    'email': emails[index],
                    'name': names[index] 
            }
            # Cấu hình Authentication
            
            Authenticator = stauth.Authenticate(credentials, cookie_name='Streamli1', key='abcdef', cookie_expiry_days=4)

            try:
                Authenticator.login("main", fields={'form': ':green[login]'})
            except Exception as e:
                st.error(e)
            # Thêm điều kiện kiểm tra nếu trả về None
            if st.session_state.authentication_status:
                st.success("Login Successful")
                st.switch_page("pages/app.py")
            elif st.session_state.authentication_status != None and st.session_state.authentication_status == False:
                st.error("Wrong email or password")
            
        
    except Exception as e:
        st.error(f"An error occurred: {e}")
        raise 
                
            

                
        

option = st.sidebar.selectbox("Navigate", ["Login", "Sign up"] , key="nav_selectbox")

# Chọn "Sign up" sẽ hiển thị form đăng ký
if option == "Sign up":
    sign_up()
elif option == "Login":
    log_in()

