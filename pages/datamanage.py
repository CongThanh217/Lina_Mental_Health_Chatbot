import mysql.connector

# Kết nối đến cơ sở dữ liệu MySQL
def get_user_id_from_username(username):
    try:
        # Thiết lập kết nối đến MySQL
        connection = mysql.connector.connect(
            host='localhost',          # Địa chỉ máy chủ MySQL
            user='root',      # Tên người dùng MySQL
            password='Thanh8c123',  # Mật khẩu MySQL
            database='user_management'   # Tên cơ sở dữ liệu
        )
        
        # Tạo con trỏ để thực hiện truy vấn
        cursor = connection.cursor()

        # Truy vấn lấy user_id từ username
        query = "SELECT user_id FROM users WHERE username = %s"
        cursor.execute(query, (username,))

        # Lấy kết quả truy vấn
        result = cursor.fetchone()  # Lấy một dòng kết quả (vì username là duy nhất)

        if result:
            return result[0]  # Lấy user_id (cột đầu tiên trong kết quả)
        else:
            return None  # Nếu không tìm thấy username

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

    finally:
        # Đảm bảo đóng kết nối
        if connection.is_connected():
            cursor.close()
            connection.close()


## lấy thông tin user từ user_id
def get_sessions_by_user_id(user_id):
    try:
        connection = mysql.connector.connect(
            host='localhost',          # Địa chỉ máy chủ MySQL
            user='root',      # Tên người dùng MySQL
            password='Thanh8c123',  # Mật khẩu MySQL
            database='user_management'   # Tên cơ sở dữ liệu
        )
        
        # Tạo con trỏ để thực hiện truy vấn
        cursor = connection.cursor()

        # Truy vấn các session_id và message_summary
        query = "SELECT session_id, summary FROM session WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        sessions = cursor.fetchall()

        if sessions:
            return sessions
        else:
            return []
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()