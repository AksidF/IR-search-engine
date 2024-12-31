def vb_decode_bits_to_numbers(bit_string):
    numbers = []
    current_number = 0
    for i in range(0, len(bit_string), 8):  # Process each 8-bit chunk
        byte = bit_string[i:i+8]
        if byte.startswith('1'):  # If the MSB is 1, this is the last byte of the current number
            current_number = current_number * 128 + int(byte[1:], 2)
            numbers.append(current_number)
            current_number = 0  # Reset for the next number
        else:  # Continuation byte
            current_number = current_number * 128 + int(byte[1:], 2)
    return numbers

def vb_decode_file_to_numbers(filename):
    decoded_data = []
    with open(filename, 'r') as file:
        for line in file:
            bit_string = line.strip()
            numbers = vb_decode_bits_to_numbers(bit_string)
            decoded_data.append(numbers)
    return decoded_data

def vb_decode_to_doc_ids(numbers):
    doc_ids = [numbers[0]]
    for gap in numbers[1:]:
        doc_ids.append(doc_ids[-1] + gap)
    return doc_ids

def decode_vb_encoded_file_to_doc_ids(filename):
    decoded_numbers = vb_decode_file_to_numbers(filename)
    doc_ids_list = [vb_decode_to_doc_ids(numbers) for numbers in decoded_numbers]
    return doc_ids_list

def vb_decode_line_to_doc_ids(filename, line_index):
    with open(filename, 'r') as file:
        for current_index, line in enumerate(file):
            if current_index == line_index:
                bit_string = line.strip()
                numbers = vb_decode_bits_to_numbers(bit_string)
                return vb_decode_to_doc_ids(numbers)
    raise IndexError(f"Line index {line_index} out of range in the file.")

