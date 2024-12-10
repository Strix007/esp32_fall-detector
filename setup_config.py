import configparser
import os

# Configuration file name
CONFIG_FILE = "settings.cfg"

def ask_for_variables():
    """
    Prompt the user for required configuration variables and save them to a file.
    """
    config = configparser.ConfigParser()

    # ESP32 Configuration
    config['ESP32'] = {
        'server_url': input("Enter ESP32 server URL (e.g., ws://192.168.0.106:12345): ")
    }

    # Google API Configuration
    config['GOOGLE_API'] = {
        'api_key': input("Enter Google API Key: "),
        'geolocation_url': input("Enter Geolocation URL (or leave blank for default): ") or "https://www.googleapis.com/geolocation/v1/geolocate?key={GOOGLE_API_KEY}",
        'reverse_geocode_url': input("Enter Reverse Geocode URL (or leave blank for default): ") or "https://maps.googleapis.com/maps/api/geocode/json"
    }

    # Twilio API Configuration
    config['TWILIO'] = {
        'account_sid': input("Enter Twilio Account SID: "),
        'auth_token': input("Enter Twilio Auth Token: "),
        'phone_number': input("Enter Twilio phone number (e.g., +17755998955): "),
        'sos_recipient_phone_number': input("Enter SOS recipient phone number: ")
    }

    # Constants
    config['CONSTANTS'] = {
        'fall_threshold': input("Enter fall threshold (default: 0.25): ") or "0.25",
        'rolling_window_size': input("Enter rolling window size (default: 5): ") or "5",
        'no_fall_reset_count': input("Enter no-fall reset count (default: 1): ") or "1",
        'fall_geolocation_trigger': input("Enter fall geolocation trigger (default: 100): ") or "100",
        'gravitational_acceleration': input("Enter gravitational acceleration (default: 9.8): ") or "9.8",
        'csv_file': input("Enter CSV file name (default: fall_detection_data.csv): ") or "fall_detection_data.csv"
    }

    # Save configuration to file
    with open(CONFIG_FILE, 'w') as file:
        config.write(file)

    print(f"Configuration saved to {CONFIG_FILE}.")

if __name__ == "__main__":
    if os.path.exists(CONFIG_FILE):
        print(f"Configuration file {CONFIG_FILE} already exists.")
        overwrite = input("Do you want to overwrite it? (y/n): ").strip().lower()
        if overwrite == 'y':
            ask_for_variables()
        else:
            print("Setup skipped. Using existing configuration.")
    else:
        ask_for_variables()
