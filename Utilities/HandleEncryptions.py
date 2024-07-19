import json
import hashlib

def readFile(file_path):
    with open(file_path, 'rb') as file:
        return file.read()

def decode(buf):
    decoded_bytes = bytearray()
    for i, b in enumerate(buf):
        decoded_bytes.append(b - (21 + (i - 14) % 6))
    decoded_str = decoded_bytes.decode('utf-8')
    return decoded_str[14:]  # Remove the first 14 characters

def parseJSON(decoded_str):
    return json.loads(decoded_str)

def saveJSONToFile(json_data, output_file_path):
    with open(output_file_path, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)

def readAndDecodeSave(input_file_path, output_file_path):
    file_content = readFile(input_file_path)
    decoded_content = decode(file_content)
    json_data = parseJSON(decoded_content)
    saveJSONToFile(json_data, output_file_path)
    print(f"Decoded JSON data has been saved to {output_file_path}")

def encode_string(string):
    return string.encode('utf-8')

def hash2(num):
    loc4 = 3988292384
    for _ in range(8):
        if num & 1:
            num = (num >> 1) ^ loc4
        else:
            num = num >> 1
    return num

def hash1(buf):
    hash_val = 0
    for b in buf:
        hash_val = ((hash_val >> 8) & 16777215) ^ hash2((hash_val ^ b) & 255)
    if hash_val < 0:
        hash_val = 4294967295 + hash_val + 1
    hash_str = hex(hash_val)[2:]
    return hash_str.zfill(8)

def encode(json_str):
    buf = encode_string(json_str)
    header = "DGDATA" + hash1(buf)
    buf = bytearray(buf)
    for i in range(len(buf)):
        buf[i] = (buf[i] + 21 + i % 6) % 256
    encoded_header = encode_string(header)
    encoded_buf = encoded_header + buf
    return encoded_buf

def save_encoded_file(encoded_buf, file_path):
    with open(file_path, 'wb') as file:
        file.write(encoded_buf)

def readAndEncodeSave(input_json_file_path, output_save_file_path):
    with open(input_json_file_path, 'r') as file:
        json_str = file.read()

    encoded_buf = encode(json_str)

    save_encoded_file(encoded_buf, output_save_file_path)
    print(f"Encoded data has been saved to {output_save_file_path}")

if __name__ == "__main__":
    input_file_path = "Profile.save" 
    output_file_path = "decoded_profile.json" 
    input_json_file_path = "decoded_profile.json"  
    output_save_file_path = "ProfileC.save"

    readAndDecodeSave(input_file_path, output_file_path)
    readAndEncodeSave(input_json_file_path, output_save_file_path)
