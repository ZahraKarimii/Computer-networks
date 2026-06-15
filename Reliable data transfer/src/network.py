import random


PROB_DROP = 0.1      
PROB_CORRUPT = 0.1  

def simulate_channel(packet_bytes):

    if random.random() < PROB_DROP:
        print(">> Network: Packet DROPPED!")
        return None 
        

    if random.random() < PROB_CORRUPT:
        print(">> Network: Packet CORRUPTED!")
        byte_list = bytearray(packet_bytes)
        idx = random.randint(0, len(byte_list) - 1)
        byte_list[idx] = byte_list[idx] ^ 0xFF 
        return bytes(byte_list)
        
    return packet_bytes