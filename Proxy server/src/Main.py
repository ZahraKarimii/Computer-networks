
import socket
from Proxy_handler import ProxyHandler
from Config import PORT

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("", PORT))
    s.listen(50)
    print(f"Proxy (with LRU cache) running on port {PORT}")

    try:
        while True:
            c, a = s.accept()
            ProxyHandler(c, a).start()
    except KeyboardInterrupt:
        print("Shutting down proxy...")
    finally:
        s.close()

if __name__ == "__main__":
    main()
