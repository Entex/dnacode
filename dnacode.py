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

parser.add_argument('--version', action='version', version='DNA Code 1.1.0')

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
        match bc:
            case '00': dna += 'A'
            case '01': dna += 'G'
            case '10': dna += 'C'
            case '11': dna += 'T'
    return dna

def convert_dna_to_6bit(dna_code):
    message = ""
    for dc in [dna_code[i:i+3] for i in range(0, len(dna_code), 3)]:
        match dc:
            case 'AAA': message += 'a'
            case 'AAC': message += 'b'
            case 'AAG': message += 'c'
            case 'AAT': message += 'd'
            case 'ACA': message += 'e'
            case 'ACC': message += 'f'
            case 'ACG': message += 'g'
            case 'ACT': message += 'h'
            case 'AGA': message += 'i'
            case 'AGC': message += 'j'
            case 'AGG': message += 'k'
            case 'AGT': message += 'l'
            case 'ATA': message += 'm'
            case 'ATC': message += 'n'
            case 'ATG': message += 'o'
            case 'ATT': message += 'p'
            case 'CAA': message += 'q'
            case 'CAC': message += 'r'
            case 'CAG': message += 's'
            case 'CAT': message += 't'
            case 'CCA': message += 'u'
            case 'CCC': message += 'v'
            case 'CCG': message += 'w'
            case 'CCT': message += 'x'
            case 'CGA': message += 'y'
            case 'CGC': message += 'z'
            case 'CGG': message += 'A'
            case 'CGT': message += 'B'
            case 'CTA': message += 'C'
            case 'CTC': message += 'D'
            case 'CTG': message += 'E'
            case 'CTT': message += 'F'
            case 'GAA': message += 'G'
            case 'GAC': message += 'H'
            case 'GAG': message += 'I'
            case 'GAT': message += 'J'
            case 'GCA': message += 'K'
            case 'GCC': message += 'L'
            case 'GCG': message += 'M'
            case 'GCT': message += 'N'
            case 'GGA': message += 'O'
            case 'GGC': message += 'P'
            case 'GGG': message += 'Q'
            case 'GGT': message += 'R'
            case 'GTA': message += 'S'
            case 'GTC': message += 'T'
            case 'GTG': message += 'U'
            case 'GTT': message += 'V'
            case 'TAA': message += 'W'
            case 'TAC': message += 'X'
            case 'TAG': message += 'Y'
            case 'TAT': message += 'Z'
            case 'TCA': message += '1'
            case 'TCC': message += '2'
            case 'TCG': message += '3'
            case 'TCT': message += '4'
            case 'TGA': message += '5'
            case 'TGC': message += '6'
            case 'TGG': message += '7'
            case 'TGT': message += '8'
            case 'TTA': message += '9'
            case 'TTC': message += '0'
            case 'TTG': message += ' '
            case 'TTT': message += '.'
    return message

def convert_6bit_to_dna(message):
    dna_code = ""
    for char in message:
        match char:
            case 'a': dna_code += 'AAA'
            case 'b': dna_code += 'AAC'
            case 'c': dna_code += 'AAG'
            case 'd': dna_code += 'AAT'
            case 'e': dna_code += 'ACA'
            case 'f': dna_code += 'ACC'
            case 'g': dna_code += 'ACG'
            case 'h': dna_code += 'ACT'
            case 'i': dna_code += 'AGA'
            case 'j': dna_code += 'AGC'
            case 'k': dna_code += 'AGG'
            case 'l': dna_code += 'AGT'
            case 'm': dna_code += 'ATA'
            case 'n': dna_code += 'ATC'
            case 'o': dna_code += 'ATG'
            case 'p': dna_code += 'ATT'
            case 'q': dna_code += 'CAA'
            case 'r': dna_code += 'CAC'
            case 's': dna_code += 'CAG'
            case 't': dna_code += 'CAT'
            case 'u': dna_code += 'CCA'
            case 'v': dna_code += 'CCC'
            case 'w': dna_code += 'CCG'
            case 'x': dna_code += 'CCT'
            case 'y': dna_code += 'CGA'
            case 'z': dna_code += 'CGC'
            case 'A': dna_code += 'CGG'
            case 'B': dna_code += 'CGT'
            case 'C': dna_code += 'CTA'
            case 'D': dna_code += 'CTC'
            case 'E': dna_code += 'CTG'
            case 'F': dna_code += 'CTT'
            case 'G': dna_code += 'GAA'
            case 'H': dna_code += 'GAC'
            case 'I': dna_code += 'GAG'
            case 'J': dna_code += 'GAT'
            case 'K': dna_code += 'GCA'
            case 'L': dna_code += 'GCC'
            case 'M': dna_code += 'GCG'
            case 'N': dna_code += 'GCT'
            case 'O': dna_code += 'GGA'
            case 'P': dna_code += 'GGC'
            case 'Q': dna_code += 'GGG'
            case 'R': dna_code += 'GGT'
            case 'S': dna_code += 'GTA'
            case 'T': dna_code += 'GTC'
            case 'U': dna_code += 'GTG'
            case 'V': dna_code += 'GTT'
            case 'W': dna_code += 'TAA'
            case 'X': dna_code += 'TAC'
            case 'Y': dna_code += 'TAG'
            case 'Z': dna_code += 'TAT'
            case '1': dna_code += 'TCA'
            case '2': dna_code += 'TCC'
            case '3': dna_code += 'TCG'
            case '4': dna_code += 'TCT'
            case '5': dna_code += 'TGA'
            case '6': dna_code += 'TGC'
            case '7': dna_code += 'TGG'
            case '8': dna_code += 'TGT'
            case '9': dna_code += 'TTA'
            case '0': dna_code += 'TTC'
            case ' ': dna_code += 'TTG'
            case '.': dna_code += 'TTT'
        if not (args.binary): dna_code += args.separator
    return dna_code.strip(args.separator)

def convert_dna_to_binary(dna_code):
    binary = ''
    for i, char in enumerate(dna_code):
        match char:
            case 'A': binary += '00'
            case 'G': binary += '01'
            case 'C': binary += '10'
            case 'T': binary += '11'
    return binary

def convert_ascii_to_binary(message):
    return ''.join([bin(ord(char))[2:].zfill(8) for char in input_message])

def convert_binary_to_ascii(binary):
    message = ''
    for bc in [binary[i:i+8] for i in range(0, len(binary), 8)]:
        message += chr(int(bc, 2))
    return message

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
            print(convert_binary_to_dna(convert_ascii_to_binary(input_message)))
    else:
        pattern = r'[^a-zA-Z0-9 .]'
        if(not args.force and re.search(pattern, input_message)):
            # Invalid characters
            sys.stderr.write("Invalid message: May only contain [a-zA-Z0-9 .]")
            exit(-6)
        dna_code = convert_6bit_to_dna(input_message)
        if(args.binary):
            print("{}".format(convert_dna_to_binary(dna_code).decode()))
        else:
            print(dna_code)
