import sys
import threading
import time
from rdt import RDTSocket

SERVER_IP = '127.0.0.1'
SERVER_PORT = 12000
CLIENT_PORT = 12001

def run_server():
    print("--- SERVER STARTED ---")
    server_socket = RDTSocket((SERVER_IP, SERVER_PORT))
    
    print(f"Listening on {SERVER_PORT}...")
    
    try:
        while True:
            data, client_addr = server_socket.recv()
            msg = data.decode('utf-8')
            print(f">>> Server delivered data: {msg}")

            
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server_socket.close()

def run_client():
    print("--- CLIENT STARTED ---")
    client_socket = RDTSocket((SERVER_IP, CLIENT_PORT))
    client_socket.connect((SERVER_IP, SERVER_PORT))
    
    messages = ["Hello RDT", "Packet 2", "Packet 3", "Final Packet"]
    
    for msg in messages:
        print(f"\n--- Sending: {msg} ---")
        client_socket.send(msg.encode('utf-8'))
        time.sleep(1) 
        
    client_socket.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py [server|client]")
    elif sys.argv[1] == "server":
        run_server()
    elif sys.argv[1] == "client":
        run_client()
    else:
        print("Invalid argument.")