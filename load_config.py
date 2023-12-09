import json

def load_config(filename):
    try:
        with open(filename, 'r') as config_file:
            config_data = json.load(config_file)
            return config_data
    except FileNotFoundError:
        print(f"File {filename} not found.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in {filename}: {e}")

if __name__ == "__main__":
    config_filename = 'config.json'

    config_data = load_config(config_filename)

    if config_data:
        # Hiển thị thông tin từ file cấu hình
        print("GENERAL:")
        print("Username:", config_data.get('Account', {}).get('username'))
        print("Password:", config_data.get('Account', {}).get('password'))
        #print("MailServer:", config_data.get('SMTP', {}).get('server'))???
        print("SMTP Port:", config_data.get('SMTP', {}).get('port'))
        print("POP3 Port:", config_data.get('POP3', {}).get('port'))        
        print("Autoload:", config_data.get('AutoFetch', {}).get('interval'))
        print("\n")
        print("FILTER:")
        print("From_address:", config_data.get('Filter', {}).get('from_address'), " - To folder: Project")
        print("Subject_keyword:", config_data.get('Filter', {}).get('subject_keyword'), " - To folder: Important")
        print("Content_keyword:", config_data.get('Filter', {}).get('content_keyword'), " - To folder: Work")