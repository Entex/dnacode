#/usr/bin/env python3
import argparse
import re
import sys

parser = argparse.ArgumentParser(description="DNA Code encoder/decoder")

parser.add_argument("-d", dest="decode", action="store_true", help="Decode message instead of encode")
parser.add_argument("-b", dest="binary", action="store_true", help="Encode/decode from or to binary (auto detec in decode mode)")
parser.add_argument("--separator", dest="separator", type=str, default=' ', help="Set separator, DEFAULT=' ' (space)")

parser.add_argument("--force", dest="force", action="store_true", help="skip validation and try to force a result")

parser.add_argument("--ascii", dest="ascii", action="store_true", help="use extended ascii representation instead of 6-bit [a-zA-Z0-9 .]")

parser.add_argument("message", nargs='?', type=str, help="Message used in encoding/decoding")
parser.add_argument("message_stdin", nargs='?', type=argparse.FileType('r'), default=sys.stdin, help=argparse.SUPPRESS) 

parser.add_argument('--version', action='version', version='DNA Code 1.1.1')

args = parser.parse_args()

# Force stupid stdin to work
input_message = ""
if not sys.stdin.isatty():
    input_message = "".join(args.message_stdin.read().splitlines())
if not input_message or input_message == "":
    input_message = args.message
if not input_message or input_message == "":
    parser.print_help()
    exit(0)

def convert_binary_to_dna(binary):
    dna = ''
    for bc in [binary[i:i+2] for i in range(0, len(binary), 2)]:
        if bc == '00': dna += 'A'
        elif bc == '01': dna += 'G'
        elif bc == '10': dna += 'C'
        elif bc == '11': dna += 'T'
    return dna

def convert_dna_to_6bit(dna_code):
    message = ""
    for dc in [dna_code[i:i+3] for i in range(0, len(dna_code), 3)]:
        if dc == 'AAA': message += 'a'
        elif dc == 'AAC': message += 'b'
        elif dc == 'AAG': message += 'c'
        elif dc == 'AAT': message += 'd'
        elif dc == 'ACA': message += 'e'
        elif dc == 'ACC': message += 'f'
        elif dc == 'ACG': message += 'g'
        elif dc == 'ACT': message += 'h'
        elif dc == 'AGA': message += 'i'
        elif dc == 'AGC': message += 'j'
        elif dc == 'AGG': message += 'k'
        elif dc == 'AGT': message += 'l'
        elif dc == 'ATA': message += 'm'
        elif dc == 'ATC': message += 'n'
        elif dc == 'ATG': message += 'o'
        elif dc == 'ATT': message += 'p'
        elif dc == 'CAA': message += 'q'
        elif dc == 'CAC': message += 'r'
        elif dc == 'CAG': message += 's'
        elif dc == 'CAT': message += 't'
        elif dc == 'CCA': message += 'u'
        elif dc == 'CCC': message += 'v'
        elif dc == 'CCG': message += 'w'
        elif dc == 'CCT': message += 'x'
        elif dc == 'CGA': message += 'y'
        elif dc == 'CGC': message += 'z'
        elif dc == 'CGG': message += 'A'
        elif dc == 'CGT': message += 'B'
        elif dc == 'CTA': message += 'C'
        elif dc == 'CTC': message += 'D'
        elif dc == 'CTG': message += 'E'
        elif dc == 'CTT': message += 'F'
        elif dc == 'GAA': message += 'G'
        elif dc == 'GAC': message += 'H'
        elif dc == 'GAG': message += 'I'
        elif dc == 'GAT': message += 'J'
        elif dc == 'GCA': message += 'K'
        elif dc == 'GCC': message += 'L'
        elif dc == 'GCG': message += 'M'
        elif dc == 'GCT': message += 'N'
        elif dc == 'GGA': message += 'O'
        elif dc == 'GGC': message += 'P'
        elif dc == 'GGG': message += 'Q'
        elif dc == 'GGT': message += 'R'
        elif dc == 'GTA': message += 'S'
        elif dc == 'GTC': message += 'T'
        elif dc == 'GTG': message += 'U'
        elif dc == 'GTT': message += 'V'
        elif dc == 'TAA': message += 'W'
        elif dc == 'TAC': message += 'X'
        elif dc == 'TAG': message += 'Y'
        elif dc == 'TAT': message += 'Z'
        elif dc == 'TCA': message += '1'
        elif dc == 'TCC': message += '2'
        elif dc == 'TCG': message += '3'
        elif dc == 'TCT': message += '4'
        elif dc == 'TGA': message += '5'
        elif dc == 'TGC': message += '6'
        elif dc == 'TGG': message += '7'
        elif dc == 'TGT': message += '8'
        elif dc == 'TTA': message += '9'
        elif dc == 'TTC': message += '0'
        elif dc == 'TTG': message += ' '
        elif dc == 'TTT': message += '.'
    return message

def convert_6bit_to_dna(message):
    dna_code = ""
    for char in message:
        if char == 'a': dna_code += 'AAA'
        elif char == 'b': dna_code += 'AAC'
        elif char == 'c': dna_code += 'AAG'
        elif char == 'd': dna_code += 'AAT'
        elif char == 'e': dna_code += 'ACA'
        elif char == 'f': dna_code += 'ACC'
        elif char == 'g': dna_code += 'ACG'
        elif char == 'h': dna_code += 'ACT'
        elif char == 'i': dna_code += 'AGA'
        elif char == 'j': dna_code += 'AGC'
        elif char == 'k': dna_code += 'AGG'
        elif char == 'l': dna_code += 'AGT'
        elif char == 'm': dna_code += 'ATA'
        elif char == 'n': dna_code += 'ATC'
        elif char == 'o': dna_code += 'ATG'
        elif char == 'p': dna_code += 'ATT'
        elif char == 'q': dna_code += 'CAA'
        elif char == 'r': dna_code += 'CAC'
        elif char == 's': dna_code += 'CAG'
        elif char == 't': dna_code += 'CAT'
        elif char == 'u': dna_code += 'CCA'
        elif char == 'v': dna_code += 'CCC'
        elif char == 'w': dna_code += 'CCG'
        elif char == 'x': dna_code += 'CCT'
        elif char == 'y': dna_code += 'CGA'
        elif char == 'z': dna_code += 'CGC'
        elif char == 'A': dna_code += 'CGG'
        elif char == 'B': dna_code += 'CGT'
        elif char == 'C': dna_code += 'CTA'
        elif char == 'D': dna_code += 'CTC'
        elif char == 'E': dna_code += 'CTG'
        elif char == 'F': dna_code += 'CTT'
        elif char == 'G': dna_code += 'GAA'
        elif char == 'H': dna_code += 'GAC'
        elif char == 'I': dna_code += 'GAG'
        elif char == 'J': dna_code += 'GAT'
        elif char == 'K': dna_code += 'GCA'
        elif char == 'L': dna_code += 'GCC'
        elif char == 'M': dna_code += 'GCG'
        elif char == 'N': dna_code += 'GCT'
        elif char == 'O': dna_code += 'GGA'
        elif char == 'P': dna_code += 'GGC'
        elif char == 'Q': dna_code += 'GGG'
        elif char == 'R': dna_code += 'GGT'
        elif char == 'S': dna_code += 'GTA'
        elif char == 'T': dna_code += 'GTC'
        elif char == 'U': dna_code += 'GTG'
        elif char == 'V': dna_code += 'GTT'
        elif char == 'W': dna_code += 'TAA'
        elif char == 'X': dna_code += 'TAC'
        elif char == 'Y': dna_code += 'TAG'
        elif char == 'Z': dna_code += 'TAT'
        elif char == '1': dna_code += 'TCA'
        elif char == '2': dna_code += 'TCC'
        elif char == '3': dna_code += 'TCG'
        elif char == '4': dna_code += 'TCT'
        elif char == '5': dna_code += 'TGA'
        elif char == '6': dna_code += 'TGC'
        elif char == '7': dna_code += 'TGG'
        elif char == '8': dna_code += 'TGT'
        elif char == '9': dna_code += 'TTA'
        elif char == '0': dna_code += 'TTC'
        elif char == ' ': dna_code += 'TTG'
        elif char == '.': dna_code += 'TTT'
    return dna_code

def convert_dna_to_binary(dna_code):
    binary = ''
    for char in dna_code:
        if char == 'A': binary += '00'
        elif char == 'G': binary += '01'
        elif char == 'C': binary += '10'
        elif char == 'T': binary += '11'
    return binary

def convert_ascii_to_binary(message):
    return ''.join([bin(ord(char))[2:].zfill(8) for char in input_message])

def convert_binary_to_ascii(binary):
    return ''.join([chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8)])

if(args.decode):
    input_message = input_message.replace(args.separator, '')
    
    # Check if binary
    pattern = r'[01]'
    if(args.binary or re.search(pattern, input_message)):
        pattern=r'[^01]'
        if(not args.force and re.search(pattern, input_message)):
            # Invalid binary
            sys.stderr.write("Invalid binary: " + input_message)
            exit(-1)
        elif(not args.force and len(input_message) % 2 != 0):
            # Invalid binary length
            sys.stderr.write("Invalid binary, odd number of digits: " + input_message)
            exit(-2)
        
        # decode binary to DNA code
        input_message = convert_binary_to_dna(input_message)

    pattern=r'[^ACGTacgt]'
    dna_code = input_message.replace(args.separator, '').upper()
    if(not args.force and re.search(pattern, dna_code)):
        # Invalid DNA code
        sys.stderr.write("Invalid DNA string: " + dna_code)
        exit(-4)
    elif(not args.force and not args.ascii and len(dna_code) % 3 != 0):
        # Invalid DNA code length
        sys.stderr.write("Invalid DNA string: " + dna_code)
        exit(-5)
    elif(not args.force and args.ascii and len(dna_code) % 4 != 0):
        # Invalid DNA code length (ext-ascii)
        sys.stderr.write("Invalid DNA string: " + dna_code)
        exit(-8)
    
    if(args.ascii):
        print(convert_binary_to_ascii(convert_dna_to_binary(dna_code)))
    else:
        print(convert_dna_to_6bit(dna_code))
else:
    if(args.ascii):
        pattern = r'[^\x00-\xFF]'
        if(not args.force and re.search(pattern, input_message)):
            # Invalid characters
            sys.stderr.write("Invalid message: May only contain extended ascii characters")
            exit(-7)
        if(args.binary):
            print(convert_ascii_to_binary(input_message))
        else:
            binary = convert_ascii_to_binary(input_message)
            dna = convert_binary_to_dna(binary)
            dna_with_separator = args.separator.join([dna[i:i+4] for i in range(0, len(dna), 4)])
            
            print(dna_with_separator)
    else:
        pattern = r'[^a-zA-Z0-9 .]'
        if(not args.force and re.search(pattern, input_message)):
            # Invalid characters
            sys.stderr.write("Invalid message: May only contain [a-zA-Z0-9 .]")
            exit(-6)
        dna_code = convert_6bit_to_dna(input_message)
        if(args.binary):
            print(convert_dna_to_binary(dna_code))
        else:
            dna_with_separator = args.separator.join([dna_code[i:i+3] for i in range(0, len(dna_code), 3)])
            print(dna_with_separator)

