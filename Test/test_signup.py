import unittest
from unittest.mock import patch, MagicMock
import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import main
from main import sign_up  


class TestSignUp(unittest.TestCase):

    @patch('main.get_user_emails')
    @patch('main.get_usernames')
    @patch('main.validate_email')
    @patch('main.validate_username')
    @patch('main.Hasher.hash')
    @patch('main.insert_user')
    @patch('streamlit.success')  # Mock st.success()
    def test_sign_up_success(self, mock_success, mock_insert_user, mock_hasher, mock_validate_username, mock_validate_email, mock_get_usernames, mock_get_user_emails):
        # Mocks
        mock_get_user_emails.return_value = ['existingemail@example.com']
        mock_get_usernames.return_value = ['existingusername']
        mock_validate_email.return_value = True
        mock_validate_username.return_value = True
        mock_hasher.return_value = 'hashed_password'  # Simulate hashed password

        # Simulate user input
        with patch('streamlit.text_input', side_effect=['John Doe', 'john@example.com', 'johnny', 'password123', 'password123']):
            with patch('streamlit.form_submit_button', return_value=True):
                sign_up()

        # Assert insert_user was called with expected arguments
        mock_insert_user.assert_called_once_with('John Doe', 'john@example.com', 'johnny', 'hashed_password')

        # Assert that st.success was called with the expected message
        mock_success.assert_called_once_with('Account created successfully!!')

    @patch('main.get_user_emails')
    @patch('main.get_usernames')
    @patch('main.validate_email')
    @patch('main.validate_username')
    @patch('streamlit.warning')
    def test_sign_up_email_taken(self, mock_warning, mock_validate_username, mock_validate_email, mock_get_usernames, mock_get_user_emails):
        # Mocks
        mock_get_user_emails.return_value = ['existingemail@example.com']
        mock_get_usernames.return_value = ['existingusername']
        mock_validate_email.return_value = True
        mock_validate_username.return_value = True

        # Simulate user input with existing email
        with patch('streamlit.text_input', side_effect=['John Doe', 'existingemail@example.com', 'johnny', 'password123', 'password123']):
            with patch('streamlit.form_submit_button', return_value=True):
                sign_up()

        # Assert warning is shown for email already exists
        mock_warning.assert_called_once_with('Email Already exists!!')

    @patch('main.get_user_emails')
    @patch('main.get_usernames')
    @patch('main.validate_email')
    @patch('main.validate_username')
    @patch('streamlit.warning')
    def test_sign_up_invalid_email(self, mock_warning, mock_validate_username, mock_validate_email, mock_get_usernames, mock_get_user_emails):
        # Mocks
        mock_get_user_emails.return_value = ['existingemail@example.com']
        mock_get_usernames.return_value = ['existingusername']
        mock_validate_email.return_value = False  # Simulate invalid email
        mock_validate_username.return_value = True

        # Simulate user input with invalid email
        with patch('streamlit.text_input', side_effect=['John Doe', 'invalid-email', 'johnny', 'password123', 'password123']):
            with patch('streamlit.form_submit_button', return_value=True):
                sign_up()

        # Assert warning is shown for invalid email
        mock_warning.assert_called_once_with('Invalid Email')

    @patch('main.get_user_emails')
    @patch('main.get_usernames')
    @patch('main.validate_email')
    @patch('main.validate_username')
    @patch('streamlit.warning')
    def test_sign_up_password_mismatch(self, mock_warning, mock_validate_username, mock_validate_email, mock_get_usernames, mock_get_user_emails):
        # Mocks
        mock_get_user_emails.return_value = ['existingemail@example.com']
        mock_get_usernames.return_value = ['existingusername']
        mock_validate_email.return_value = True
        mock_validate_username.return_value = True

        # Simulate user input with password mismatch
        with patch('streamlit.text_input', side_effect=['John Doe', 'john@example.com', 'johnny', 'password123', 'password456']):
            with patch('streamlit.form_submit_button', return_value=True):
                sign_up()

        # Assert warning is shown for password mismatch
        mock_warning.assert_called_once_with('Passwords Do Not Match')


if __name__ == '__main__':
    unittest.main()
