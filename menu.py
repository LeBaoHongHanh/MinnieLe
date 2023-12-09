class EmailClient:
    # ... (các phương thức và thuộc tính khác)

    def display_menu(self):
        print("Vui lòng chọn Menu:")
        print("1. Để gửi email")
        print("2. Để xem danh sách các email đã nhận")
        print("3. Thoát")

    def run(self):
        while True:
            self.display_menu()
            choice = input("Nhập lựa chọn của bạn: ")

            if choice == '1':
                # Gọi phương thức gửi email ở đây
                pass
            elif choice == '2':
                # Gọi phương thức xem danh sách email ở đây
                pass
            elif choice == '3':
                print("Tạm biệt!")
                break
            else:
                print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")

if __name__ == "__main__":
    client = EmailClient()
    client.load_config()

    client.run()