import textwrap

INITIAL_PERMUTATION_TABLE = [
                            '58 ', '50 ', '42 ', '34 ', '26 ', '18 ', '10 ', '2',
			                '60 ', '52 ', '44 ', '36 ', '28 ', '20 ', '12 ', '4',
			                '62 ', '54 ', '46 ', '38 ', '30 ', '22 ', '14 ', '6', 
			                '64 ', '56 ', '48 ', '40 ', '32 ', '24 ', '16 ', '8', 
			                '57 ', '49 ', '41 ', '33 ', '25 ', '17 ', '9 ', '1',
			                '59 ', '51 ', '43 ', '35 ', '27 ', '19 ', '11 ', '3',
			                '61 ', '53 ', '45 ', '37 ', '29 ', '21 ', '13 ', '5',
			                '63 ', '55 ', '47 ', '39 ', '31 ', '23 ', '15 ', '7'
]

INVERSE_PERMUTATION_TABLE = [
                            '40 ', '8 ', '48 ', '16 ', '56 ', '24 ', '64 ', '32',
			                '39 ', '7 ', '47 ', '15 ', '55 ', '23 ', '63 ', '31',
			                '38 ', '6 ', '46 ', '14 ',  '54 ', '22 ', '62 ', '30',
			                '37 ', '5 ', '45 ', '13 ', '53 ', '21 ', '61 ', '29',
			                '36 ', '4 ', '44 ', '12 ', '52 ', '20 ', '60 ', '28',
			                '35 ', '3 ', '43 ', '11 ', '51 ', '19 ', '59 ', '27', 
			                '34 ', '2 ', '42 ', '10 ', '50 ', '18 ', '58 ', '26',
			                '33 ', '1 ', '41 ', '9 ', '49 ', '17 ', '57 ', '25'
]

PC1_TABLE = [
    57,49,41,33,25,17,9,
    1,58,50,42,34,26,18,
    10,2,59,51,43,35,27,
    19,11,3,60,52,44,36,
    63,55,47,39,31,23,15,
    7,62,54,46,38,30,22,
    14,6,61,53,45,37,29,
    21,13,5,28,20,12,4
]

PC2_TABLE = [
    14,17,11,24,1,5,3,28,
    15,6,21,10,23,19,12,4,
    26,8,16,7,27,20,13,2,
    41,52,31,37,47,55,30,40,
    51,45,33,48,44,49,39,56,
    34,53,46,42,50,36,29,32
]

EXPANSION_TABLE = [
    32,1,2,3,4,5,
    4,5,6,7,8,9,
    8,9,10,11,12,13,
    12,13,14,15,16,17,
    16,17,18,19,20,21,
    20,21,22,23,24,25,
    24,25,26,27,28,29,
    28,29,30,31,32,1
]

SBOX = [
[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
[0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
[4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
[15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]
]

PERMUTATION_TABLE = [
    16,7,20,21,29,12,28,17,
    1,15,23,26,5,18,31,10,
	2,8,24,14,32,27,3,9,
    19,13,30,6,22,11,4,25
]

# 1. Adım açık metine karşılık gelen ikili kod
def string_to_binary(plaintext):
    binary_plaintext = ''.join(format(ord(i),'b').zfill(8) for i in plaintext) 
    return binary_plaintext

# 2. Adım IP uygulanması
def apply_initial_permutation(binary_plaintext, PERMUTATION_TABLE=INITIAL_PERMUTATION_TABLE):
    permutated_text = ""
    for index in PERMUTATION_TABLE:
        permutated_text += binary_plaintext[int(index)-1]
    return permutated_text

# 3.Adım L0 ve R0 ayrımı
def split_in_half(binarybits):
    L0 = binarybits[:32]
    R0 = binarybits[32:]
    return L0,R0

# 4.Adım Expansion Table
def apply_expansion(R0,PERMUTATION_TABLE=EXPANSION_TABLE):
    bits48 = ""
    for index in EXPANSION_TABLE:
        bits48 += R0[index-1]
    return bits48

# 5.Adım XOR
def XOR(bits1,bits2):
	xor_result = ""
	for index in range(len(bits1)):
		if bits1[index] == bits2[index]: 
			xor_result += '0'
		else:
			xor_result += '1'
	return xor_result

# 6.Adım SBOX
def split_in_6bits(XOR_48bits):
	list_of_6bits = textwrap.wrap(XOR_48bits,6)
	return list_of_6bits

def get_first_and_last_bit(bits6):
	twobits = bits6[0] + bits6[-1] 
	return twobits

def get_middle_four_bit(bits6):
	fourbits = bits6[1:5] 
	return fourbits

def binary_to_decimal(binarybits):
	decimal = int(binarybits,2)
	return decimal

def decimal_to_binary(decimal):
	binary4bits = bin(decimal)[2:].zfill(4)
	return binary4bits

def sbox_lookup(sboxcount,first_last,middle4):
	d_first_last = binary_to_decimal(first_last)
	d_middle = binary_to_decimal(middle4)
	
	sbox_value = SBOX[sboxcount][d_first_last][d_middle]
	return decimal_to_binary(sbox_value)

# 7.Adım Permutation table
def apply_permutation(sbox_32bits,PERMUTATION_TABLE=PERMUTATION_TABLE):
	
	final_32bits = ""
	for index in PERMUTATION_TABLE:
		final_32bits += sbox_32bits[index-1]
	return final_32bits

###########################################################
# F FONKSYONU
def functionF(pre32bits, key48bits):	
	result = ""
	expanded_left_half = apply_expansion(EXPANSION_TABLE,pre32bits)
	xor_value = XOR(expanded_left_half,key48bits)
	bits6list = split_in_6bits(xor_value)
	for sboxcount, bits6 in enumerate(bits6list):
		first_last = get_first_and_last_bit(bits6)
		middle4 = get_middle_four_bit(bits6)
		sboxvalue = sbox_lookup(sboxcount,first_last,middle4)
		result += sboxvalue
	final32bits = apply_permutation(PERMUTATION_TABLE,result)	
	return final32bits

###########################################################
# ANAHTAR OLUŞTURMA

# 1.Adım PC1
def apply_pc1(key_64bits,PERMUTATION_TABLE=PC1_TABLE):
    key_56bits = ""
    for index in PC1_TABLE:
        key_56bits += key_64bits[index-1]
    return key_56bits

# 2.Adım Left Key ve Right Key ayrımı
def split_in_half(key_56bits):
    left_key = key_56bits[:28]
    right_key = key_56bits[28:]
    return left_key,right_key

# 3.Adım Circular Left Shift
def circular_left_shift(left_key,right_key):
    shifted_left = left_key[1:] + left_key[:1]
    shifted_right = right_key[1:] + right_key[:1]
    shifted = shifted_left + shifted_right
    return shifted

# 4.Adım PC2
def apply_pc2(shifted,PERMUTATION_TABLE=PC2_TABLE):
    key_48bits = ""
    for index in PC2_TABLE:
        keys_48bits += shifted[index-1]
    return key_48bits

# ANAHTAR OLUŞTURMA
def generate_key(key_64bits):
    pc1_out = apply_pc1(key_64bits) 
    C0,D0 = split_in_half(pc1_out)
    shifted = circular_left_shift(C0,D0)
    key = apply_pc2(shifted)
    return key

##################################################33

def hexTobinary(hexdigits):
	binarydigits = ""
	for hexdigit in hexdigits:
		binarydigits += bin(int(hexdigit,16))[2:].zfill(4)
	return binarydigits


def DES_encrypt(message,key):
	cipher = ""

	plaintext_bits = hexTobinary(message)
	key_bits = hexTobinary(key)
	
	roundkeys = generate_key(key_bits)
	
	
	
	p_plaintext = apply_initial_permutation(INITIAL_PERMUTATION_TABLE,plaintext_bits)
	
	L,R = split_in_half(p_plaintext)
	
	for round in range(16):
		newR = XOR(L,functionF(R, roundkeys[round]))
		newL = R
		R = newR
		L = newL
	cipher = apply_initial_permutation(INVERSE_PERMUTATION_TABLE, R+L)
	return cipher




if __name__ == "__main__":
    print(DES_encrypt("kemalozer","21721149"))

