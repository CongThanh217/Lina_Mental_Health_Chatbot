import mysql.connector
import datetime
import re
import streamlit as st
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities.hasher import Hasher


# MySQL Connection Parameters
HOST = 'localhost'  # Use 'localhost' for local MySQL
USER = 'root'  # Default MySQL username
PASSWORD = 'Thanh8c123'  # Replace with your MySQL root password
DATABASE = 'user_management'  

# Function to create connection to MySQL
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )
        print("Connected to MySQL")
        return connection
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return None

# Function to insert user into MySQL
def insert_user(email, username, password):
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
        cursor.execute("INSERT INTO users (email, username, password, date_joined) VALUES (%s, %s, %s, %s)", 
                       (email, username, password, date_joined))
        connection.commit()
        cursor.close()
        connection.close()
        st.success('Account created successfully!!')
        st.balloons()
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
    pattern = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
    return bool(re.match(pattern, email))

# Username validation function (same as before)
def validate_username(username):
    pattern = "^[a-zA-Z0-9]*$"
    return bool(re.match(pattern, username))

# Signup function (same as before but using MySQL)
def sign_up():
    with st.form(key='signup', clear_on_submit=True):
        st.subheader(':green[Sign Up]')
        email = st.text_input(':blue[Email]', placeholder='Enter Your Email')
        username = st.text_input(':blue[Username]', placeholder='Enter Your Username')
        password1 = st.text_input(':blue[Password]', placeholder='Enter Your Password', type='password')
        password2 = st.text_input(':blue[Confirm Password]', placeholder='Confirm Your Password', type='password')

        if email:
            if validate_email(email):
                if email not in get_user_emails():
                    if validate_username(username):
                        if username not in get_usernames():
                            if len(username) >= 2:
                                if len(password1) >= 6:
                                    if password1 == password2:
                                        # Add User to MySQL DB
                                        hashed_passwords = Hasher.hash(password2)
                                        insert_user(email, username, hashed_passwords)
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

