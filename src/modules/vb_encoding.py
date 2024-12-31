def vb_encode_number_to_bits(number):
    bits = []
    while True:
        bits.insert(0, f'{number % 128:07b}')  # Convert to a 7-bit binary string
        if number < 128:
            break
        number //= 128
    bits[-1] = '1' + bits[-1]  # Mark the last byte with the continuation bit (MSB set to 1)
    bits[:-1] = ['0' + b for b in bits[:-1]]  # Mark other bytes with MSB set to 0
    return ''.join(bits)

def vb_encode_to_bits(numbers):
    bit_stream = ''
    for number in numbers:
        bit_stream += vb_encode_number_to_bits(number)
    return bit_stream

def calculate_gaps(doc_ids):
    gaps = [doc_ids[0]]  # The first gap is the first document ID
    for i in range(1, len(doc_ids)):
        gaps.append(doc_ids[i] - doc_ids[i - 1])
    return gaps

def save_vb_encoded_bits_to_file_multiline(list_of_doc_ids, filename):
    with open(filename, 'w') as file:
        for doc_ids in list_of_doc_ids:
            gaps = calculate_gaps(doc_ids)
            encoded_bits = vb_encode_to_bits(gaps)
            file.write(encoded_bits + '\n')
    print(f"VB encoded data saved to {filename}")

