# handler.py
import socket
import threading
from Config import BUFFER_SIZE
from Logger import Logger
from Filter import filter_manager
from Cache import cache

class ProxyHandler(threading.Thread):
    def __init__(self, sock: socket.socket, addr):
        super().__init__(daemon=True)
        self.sock = sock
        self.addr = addr


    def run(self):
        try:
            req = self._recv_request()
            if not req:
                return
            first = req.split(b"\n")[0].decode(errors="ignore")
            parts = first.split()
            if len(parts) < 3:
                return
            method, url, ver = parts[0], parts[1], parts[2]
            if filter_manager.is_blocked(url):
                self.send_error("403 Forbidden")
                Logger.log(self.addr[0], method, url, "403")
                return
            if method.upper() == "CONNECT":
                self.handle_https(url)
            else:
                self.handle_http(method.upper(), url, req)
        except Exception:
            pass
        finally:
            try: self.sock.close()
            except: pass


    def _recv_request(self) -> bytes:
        try:
            return self.sock.recv(BUFFER_SIZE)
        except Exception:
            return b""


    def send_error(self, msg: str):
        body = f"<h1>{msg}</h1>"
        resp = f"HTTP/1.1 {msg}\r\nContent-Length: {len(body)}\r\n\r\n{body}"
        try:
            self.sock.sendall(resp.encode())
        except Exception:
            pass


    def handle_https(self, url: str):
        host, port = (url.split(':') if ':' in url else (url, 443))
        try:
            port = int(port)
        except:
            port = 443
        try:
            remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            remote.connect((host, port))
            self.sock.sendall(b"HTTP/1.1 200 Connection Established\r\n\r\n")
            Logger.log(self.addr[0], "CONNECT", url, "200")
            t1 = threading.Thread(target=self.pipe, args=(self.sock, remote))
            t2 = threading.Thread(target=self.pipe, args=(remote, self.sock))
            t1.start(); t2.start(); t1.join(); t2.join()
        except Exception:
            Logger.log(self.addr[0], "CONNECT", url, "502")
            try:
                self.send_error("502 Bad Gateway")
            except:
                pass


    def pipe(self, src: socket.socket, dst: socket.socket):
        try:
            while True:
                data = src.recv(BUFFER_SIZE)
                if not data: break
                dst.sendall(data)
        except Exception:
            pass
        finally:
            try: src.close()
            except: pass
            try: dst.close()
            except: pass


    def handle_http(self, method: str, url: str, req_bytes: bytes):
        if method == "GET":
            cached = cache.get(url)
            if cached:
                try:
                    self.sock.sendall(cached)
                    Logger.log(self.addr[0], method, url, "200 (cached)")
                except Exception:
                    pass
                return
        host = url.split('://')[-1].split('/')[0].split(':')[0]
        port = 80
        try:
            remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            remote.connect((host, port))
            remote.sendall(req_bytes)
            full = b""
            while True:
                data = remote.recv(BUFFER_SIZE)
                if not data:
                    break
                full += data
                try:
                    self.sock.sendall(data)
                except Exception:
                    pass
            try:
                header_line = full.split(b"\r\n", 1)[0].decode(errors="ignore")
                if method == "GET" and header_line.startswith("HTTP/1.1 200"):
                    cache.save(url, full)
            except Exception:
                pass
            Logger.log(self.addr[0], method, url, "200")
            remote.close()
        except Exception:
            Logger.log(self.addr[0], method, url, "502")
            try:
                self.send_error("502 Bad Gateway")
            except:
                pass
