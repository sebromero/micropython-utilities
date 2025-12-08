from micropython_utilities import ESPNowManager

esp_manager = ESPNowManager()
address = esp_manager.start()

def enter_sender_mode():
    peer_mac = input("Enter the MAC address of the peer (format: aa bb cc dd ee ff): ").strip()
        
    while True:
        message = input("Enter message to send: ")
        esp_manager.send_message(peer_mac, message)


def enter_receiver_mode():
    print(f"Listening for messages at address '{address}'...")
    while True:
        host, message = esp_manager.get_message()
        if message:
            print(f"Received from {host}: {message}")

try:
    # Ask user if they want to be sender or receiver
    mode = input("\nEnter 's' to be sender or 'r' to be receiver: ").strip().lower()
    if mode == 's':
        enter_sender_mode()        
    elif mode == 'r':
        enter_receiver_mode()
    else:
        print("Invalid mode selected. Please restart and choose 's' or 'r'.")

finally:
    print("Stopping ESP-NOW manager...")
    esp_manager.stop() # Ensure resources are cleaned up on exit