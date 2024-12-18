import unittest
from unittest.mock import patch, MagicMock
import streamlit as st
import streamlit_authenticator as stauth
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import main
from main import log_in, fetch_users  # Import các hàm cần thiết

class TestLogin(unittest.TestCase):

    @patch('main.fetch_users')
    @patch('main.stauth.Authenticate')
    @patch('streamlit.session_state', autospec=True)  # Mock session_state
    @patch('streamlit.switch_page')  # Mock switch_page để tránh lỗi
    def test_login_successful(self, MockSwitchPage, MockSessionState, MockAuthenticator, MockFetchUsers):
        # Mock dữ liệu người dùng
        MockFetchUsers.return_value = [
            ('1', 'user1', 'user1@example.com', 'password1', 'some_other_data', 'User One'),
            ('2', 'user2', 'user2@example.com', 'password2', 'some_other_data', 'User Two')
        ]

        # Mock hành vi của stauth.Authenticate
        mock_authenticator = MagicMock()
        MockAuthenticator.return_value = mock_authenticator
        mock_authenticator.login.return_value = True  # Đăng nhập thành công

        # Thiết lập session_state giả lập
        MockSessionState.authentication_status = True

        # Gọi hàm đăng nhập
        log_in()

        # Kiểm tra xem trạng thái đăng nhập có thành công không
        self.assertEqual(MockSessionState.authentication_status, True)
        mock_authenticator.login.assert_called_once()  # Kiểm tra xem hàm login đã được gọi
        MockSwitchPage.assert_called_once_with("pages/app.py")  # Kiểm tra xem switch_page đã được gọi

    @patch('main.fetch_users')
    @patch('main.stauth.Authenticate')
    @patch('streamlit.session_state', autospec=True)  # Mock session_state
    @patch('streamlit.switch_page')  # Mock switch_page để tránh lỗi
    def test_login_failed(self, MockSwitchPage, MockSessionState, MockAuthenticator, MockFetchUsers):
        # Mock dữ liệu người dùng
        MockFetchUsers.return_value = [
            ('1', 'user1', 'user1@example.com', 'password1', 'some_other_data', 'User One'),
            ('2', 'user2', 'user2@example.com', 'password2', 'some_other_data', 'User Two')
        ]

        # Mock hành vi của stauth.Authenticate
        mock_authenticator = MagicMock()
        MockAuthenticator.return_value = mock_authenticator
        mock_authenticator.login.return_value = False  # Đăng nhập thất bại

        # Thiết lập session_state giả lập
        MockSessionState.authentication_status = False

        # Gọi hàm đăng nhập
        log_in()

        # Kiểm tra xem trạng thái đăng nhập có đúng không
        self.assertEqual(MockSessionState.authentication_status, False)
        mock_authenticator.login.assert_called_once()  # Kiểm tra xem hàm login đã được gọi
        MockSwitchPage.assert_not_called()  # Kiểm tra xem switch_page không được gọi

    @patch('main.fetch_users')
    @patch('main.stauth.Authenticate')
    @patch('streamlit.session_state', autospec=True)  # Mock session_state
    @patch('streamlit.switch_page')  # Mock switch_page để tránh lỗi
    def test_no_users_in_db(self, MockSwitchPage, MockSessionState, MockAuthenticator, MockFetchUsers):
        # Mock không có người dùng trong cơ sở dữ liệu
        MockFetchUsers.return_value = []

        # Mock hành vi của stauth.Authenticate
        mock_authenticator = MagicMock()
        MockAuthenticator.return_value = mock_authenticator

        # Gọi hàm đăng nhập khi không có người dùng
        log_in()

        # Kiểm tra xem có thông báo lỗi hay không
        mock_authenticator.login.assert_not_called()  # Kiểm tra xem login không được gọi
        MockSwitchPage.assert_not_called()  # Kiểm tra xem switch_page không được gọi

if __name__ == '__main__':
    unittest.main()
