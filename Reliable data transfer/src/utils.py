import struct

# Packet Types
TYPE_DATA = 0
TYPE_ACK = 1

def calculate_checksum(data_bytes):
    if len(data_bytes) % 2 == 1:
        data_bytes += b'\x00'
    
    checksum = 0
    for i in range(0, len(data_bytes), 2):
        w = (data_bytes[i] << 8) + (data_bytes[i+1])
        checksum += w
        
    checksum = (checksum >> 16) + (checksum & 0xFFFF)
    checksum = ~checksum & 0xFFFF
    return checksum

def make_packet(pkt_type, seq_num, data=b''):

    length = len(data)
    header_structure = '!BBHH'
    checksum = 0
    
    temp_header = struct.pack(header_structure, pkt_type, seq_num, length, checksum)
    msg = temp_header + data
    
    checksum = calculate_checksum(msg)
    
    final_header = struct.pack(header_structure, pkt_type, seq_num, length, checksum)
    return final_header + data

def extract_packet(packet_bytes):
    if len(packet_bytes) < 6:
        return None, None, None, False
        
    header = packet_bytes[:6]
    payload = packet_bytes[6:]
    
    pkt_type, seq, length, rcv_checksum = struct.unpack('!BBHH', header)

    header_zero_checksum = struct.pack('!BBHH', pkt_type, seq, length, 0)
    calculated_checksum = calculate_checksum(header_zero_checksum + payload)
    
    if calculated_checksum != rcv_checksum:
        return None, None, None, False 
        
    return pkt_type, seq, payload, True 