import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import sys
import streamlit as st
import base64

# Set giá trị session_state trước khi import app
st.session_state['username'] = 'congthanh'
st.session_state['authentication_status'] = True
st.session_state['name'] = "Công Thành"

# Thêm thư mục gốc vào sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock load_tests trước khi import app
with patch("builtins.open", mock_open(read_data='{"tests": []}')), patch("os.path.exists", return_value=True):
    from pages import app

class TestVoiceSelection(unittest.TestCase):

    @patch("pages.app.client.synthesize_speech")
    @patch("pages.app.detect")
    @patch("streamlit.markdown")
    def test_generate_and_play_audio(self, mock_markdown, mock_detect, mock_synthesize_speech):
        # Mock detect language
        mock_detect.return_value = "en"

        # Mock response từ Google TTS API
        mock_audio_content = b"fake_audio_content"
        mock_synthesize_speech.return_value = MagicMock(audio_content=mock_audio_content)

        # Input test
        test_text = "Hello, this is a test message."

        # Gọi hàm cần test
        app.generate_and_play_audio(test_text, gender="Male", voice_selected="Wavenet")

        # Kiểm tra synthesize_speech gọi 1 lần
        mock_synthesize_speech.assert_called_once()

        # Kiểm tra markdown chứa thẻ audio chính xác
        audio_base64 = base64.b64encode(mock_audio_content).decode('utf-8')
        expected_audio_tag = f'<audio autoplay="true" src="data:audio/wav;base64,{audio_base64}">'
        mock_markdown.assert_called_once_with(expected_audio_tag, unsafe_allow_html=True)

if __name__ == "__main__":
    unittest.main()
