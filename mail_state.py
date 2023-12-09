import socket
import ssl
import os
import json
import time
import threading

# Đọc cấu hình từ file config
with open('config.json', 'r') as file:
    config = json.load(file)

SMTP_SERVER = config.get('SMTP', 'server')
SMTP_PORT = int(config.get('SMTP', 'port'))
POP3_SERVER = config.get('POP3', 'server')
POP3_PORT = int(config.get('POP3', 'port'))
USERNAME = config.get('Account', 'username')
PASSWORD = config.get('Account', 'password')

# ... (các phần khác của mã)

# Đường dẫn đến file lưu trạng thái email
state_filename = 'email_state.json'

def auto_fetch_email(interval, email_state):
    while True:
        # Kết nối với máy chủ POP3
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as pop3_socket:
            pop3_socket.connect((POP3_SERVER, POP3_PORT))

            # Xác thực với máy chủ POP3
            receive_data = pop3_socket.recv(1024).decode()
            print(receive_data)

            pop3_socket.sendall(b"USER " + USERNAME.encode() + b"\r\n")
            receive_data = pop3_socket.recv(1024).decode()
            print(receive_data)

            pop3_socket.sendall(b"PASS " + PASSWORD.encode() + b"\r\n")
            receive_data = pop3_socket.recv(1024).decode()
            print(receive_data)

            # Nhận danh sách thư
            pop3_socket.sendall(b"LIST\r\n")
            receive_data = pop3_socket.recv(1024).decode()
            print(receive_data)

            # Lấy danh sách thư
            email_list = []
            while True:
                pop3_socket.sendall(b"RETR\r\n")
                receive_data = pop3_socket.recv(1024).decode()
                if receive_data.startswith("+OK"):
                    email_list.append(receive_data)
                else:
                    break

            # Xử lí trạng thái thư
            for email_id in range(1, len(email_list) + 1):
                if email_id not in email_state:
                    mark_as_unread(email_id, email_state)
                else:
                    mark_as_read(email_id, email_state)

            pop3_socket.sendall(b"QUIT\r\n")
            receive_data = pop3_socket.recv(1024).decode()
            print(receive_data)

        # Lưu trạng thái email sau mỗi lượt tải
        save_email_state(email_state)

        # Đợi khoảng thời gian trước khi tải email tiếp theo
        time.sleep(interval)

def load_email_state():
    if os.path.exists(state_filename):
        with open(state_filename, 'r') as state_file:
            return json.load(state_file)
    else:
        return {}

# Hàm đánh dấu thư đã đọc
def mark_as_read(email_id, email_state):
    # Đánh dấu email là đã đọc
    for i, (sender, subject, is_read) in enumerate(email_state):
        if i + 1 == email_id:
            email_state[i] = (sender, subject, True)
            print(f"Email ID {email_id} marked as read.")
            break

# Hàm đánh dấu thư chưa đọc
def mark_as_unread(email_id, email_state):
    # Đánh dấu email là chưa đọc
    for i, (sender, subject, is_read) in enumerate(email_state):
        if i + 1 == email_id:
            email_state[i] = (sender, subject, False)
            print(f"Email ID {email_id} marked as unread.")
            break

# Hàm lưu trạng thái email vào file
def save_email_state(email_state):
    # Mở file để ghi
    with open(state_filename, 'w') as state_file:
        for email_id, (sender, subject, is_read) in enumerate(email_state, start=1):
            # Xây dựng định dạng dòng trong file
            line_format = "{status} {sender}, {subject}\n"
            status = "" if is_read else "(chưa đọc)"
            line = line_format.format(status=status, sender=sender, subject=subject)

            # Ghi dòng vào file
            state_file.write(line)

    print(f"Email state saved to {state_filename}")

# Hàm xử lí email và lưu trạng thái nếu có lệnh yêu cầu đọc mail
def process_and_mark_as_read(email_id, pop3_socket):
    # Xử lý nội dung email ở đây
    # Ví dụ: In ra nội dung email
    pop3_socket.sendall(f"RETR {email_id}\r\n".encode())
    email_content = receive_all_data(pop3_socket).decode()
    print(f"Received email ID {email_id}: {email_content}")

    # Đánh dấu email đã đọc
    mark_as_read(email_id, email_state)

    # Lưu trạng thái email
    save_email_state(email_state)

# Hàm nhận toàn bộ nội dung của email
def receive_all_data(socket):
    # Nhận toàn bộ dữ liệu từ socket
    data = b""
    while True:
        chunk = socket.recv(1024)
        if not chunk:
            break
        data += chunk
    return data

# Chương trình chính
if __name__ == "__main__":
    # ... (các phần khác của mã)

    # Đọc trạng thái email từ file
    email_state = load_email_state()

    # Bắt đầu thread tự động tải email
    interval = int(config.get('Autoload', 'interval')) # Lưu thời gian tải tự động được cài đặt trong file cấu hình
    auto_fetch_thread = threading.Thread(target=auto_fetch_email, args=(interval, email_state))
    auto_fetch_thread.start()

    # Gửi/nhận email và xử lý trạng thái theo yêu cầu từ người dùng
    # ...

    # Chờ thread tự động tải email kết thúc khi thoát chương trình
    auto_fetch_thread.join()

    # Lưu trạng thái email khi tắt chương trình
    save_email_state(email_state)