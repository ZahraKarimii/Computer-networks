import socket
import utils
import network

class RDTSocket:
    def __init__(self, local_addr, timeout=1.0):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(local_addr)
        self.sock.settimeout(timeout) 
        self.seq_num = 0 
        self.target_addr = None 
        self.last_ack_sent = 1

    def connect(self, address):
        self.target_addr = address

    def send(self, data):
        sndpkt = utils.make_packet(utils.TYPE_DATA, self.seq_num, data)
        while True:
            packet_to_send = network.simulate_channel(sndpkt)
            if packet_to_send:
                self.sock.sendto(packet_to_send, self.target_addr)
            
            print(f"[Send] Seq={self.seq_num} sent. Waiting for ACK...")
            
            try:
                rcv_bytes, _ = self.sock.recvfrom(1024)
                pkt_type, rcv_seq, _, is_valid = utils.extract_packet(rcv_bytes)

                if is_valid and pkt_type == utils.TYPE_ACK and rcv_seq == self.seq_num:
                    print(f"[Send] ACK {rcv_seq} received correctly. Moving on.\n")
                    self.seq_num = 1 - self.seq_num 
                    break 
                else:
                    print("[Send] Garbage or Wrong ACK received. Ignore.")
            
            except socket.timeout:
                print("[Send] Timeout! Resending packet...")
                continue

    def recv(self):
        while True:
            try:
                rcv_bytes, addr = self.sock.recvfrom(2048)
            except socket.timeout:
                continue

            pkt_type, rcv_seq, payload, is_valid = utils.extract_packet(rcv_bytes)
            
            if not is_valid:
                print("[Recv] Corrupt packet! Resending Last ACK.")
                continue 
            
            if pkt_type == utils.TYPE_DATA:
                if rcv_seq == self.seq_num:
                    print(f"[Recv] Packet {rcv_seq} OK. Sending ACK.")
                    
                    ack_pkt = utils.make_packet(utils.TYPE_ACK, self.seq_num)
                    ack_to_send = network.simulate_channel(ack_pkt)
                    if ack_to_send:
                        self.sock.sendto(ack_to_send, addr)
                    
                    self.last_ack_sent = self.seq_num
                    self.seq_num = 1 - self.seq_num
                    return payload, addr 

                else:
                    print(f"[Recv] Duplicate Packet {rcv_seq}. Resending ACK {rcv_seq}.")
                    ack_pkt = utils.make_packet(utils.TYPE_ACK, rcv_seq)
                    ack_to_send = network.simulate_channel(ack_pkt)
                    if ack_to_send:
                        self.sock.sendto(ack_to_send, addr)

    def close(self):
        self.sock.close()