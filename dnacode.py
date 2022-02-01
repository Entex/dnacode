#!/usr/bin/env python3
import argparse
import re
import sys

parser = argparse.ArgumentParser(description="DNA Code encoder/decoder")


parser.add_argument("-a", "--ascii", dest="ascii", action="store_true", help="use extended ascii representation instead of 6-bit [a-zA-Z0-9 .]")
parser.add_argument("-d", "--decode", dest="decode", action="store_true", help="Decode message instead of encode")
parser.add_argument("-b", "--binary", dest="binary", action="store_true", help="Encode/decode from or to binary (auto detect in decode mode)")
parser.add_argument("-s", "--separator", dest="separator", type=str, default=' ', help="Set separator, DEFAULT=' ' (space)")
parser.add_argument("--force", dest="force", action="store_true", help="skip validation and try to force a result")

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

mapping_dna_to_6bit = {
    'AAA': 'a', 'AAC': 'b', 'AAG': 'c', 'AAT': 'd', 'ACA': 'e', 'ACC': 'f',
    'ACG': 'g', 'ACT': 'h', 'AGA': 'i', 'AGC': 'j', 'AGG': 'k', 'AGT': 'l',
    'ATA': 'm', 'ATC': 'n', 'ATG': 'o', 'ATT': 'p', 'CAA': 'q', 'CAC': 'r',
    'CAG': 's', 'CAT': 't', 'CCA': 'u', 'CCC': 'v', 'CCG': 'w', 'CCT': 'x',
    'CGA': 'y', 'CGC': 'z', 'CGG': 'A', 'CGT': 'B', 'CTA': 'C', 'CTC': 'D',
    'CTG': 'E', 'CTT': 'F', 'GAA': 'G', 'GAC': 'H', 'GAG': 'I', 'GAT': 'J',
    'GCA': 'K', 'GCC': 'L', 'GCG': 'M', 'GCT': 'N', 'GGA': 'O', 'GGC': 'P',
    'GGG': 'Q', 'GGT': 'R', 'GTA': 'S', 'GTC': 'T', 'GTG': 'U', 'GTT': 'V',
    'TAA': 'W', 'TAC': 'X', 'TAG': 'Y', 'TAT': 'Z', 'TCA': '1', 'TCC': '2',
    'TCG': '3', 'TCT': '4', 'TGA': '5', 'TGC': '6', 'TGG': '7', 'TGT': '8',
    'TTA': '9', 'TTC': '0', 'TTG': ' ', 'TTT': '.'
}

mapping_dna_to_binary = {
    'A': '00',
    'G': '01',
    'C': '10',
    'T': '11'
}

def dict_get_key(dictionary, value):
    return list(dictionary.keys())[list(dictionary.values()).index(value)]

def convert_dna_to_binary(dna_code):
    binary = []
    for char in dna_code:
        binary.append(mapping_dna_to_binary[char])
    return ''.join(binary)

def convert_binary_to_dna(binary):
    dna = []
    for bc in [binary[i:i+2] for i in range(0, len(binary), 2)]:
        dna.append(dict_get_key(mapping_dna_to_binary, bc))
    return ''.join(dna)

def convert_dna_to_6bit(dna_code):
    message = []
    for dc in [dna_code[i:i+3] for i in range(0, len(dna_code), 3)]:
        message.append(mapping_dna_to_6bit[dc])
    return ''.join(message)

def convert_6bit_to_dna(message):
    dna_code = []
    for char in message:
        dna_code.append(dict_get_key(mapping_dna_to_6bit, char))
    return ''.join(dna_code)

def convert_ascii_to_binary(message):
    return ''.join([bin(ord(char))[2:].zfill(8) for char in message])

def convert_binary_to_ascii(binary):
    return ''.join([chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8)])

if(args.decode):
    input_message = input_message.replace(args.separator, '')

    # Check if we are decoding a binary
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

    # Remove separator and uppercase everything before decoding
    dna_code = input_message.replace(args.separator, '').upper()

    # Validate DNA string
    pattern=r'[^ACGTacgt]'
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

    # Decode and print
    if(args.ascii):
        print(convert_binary_to_ascii(convert_dna_to_binary(dna_code)))
    else:
        print(convert_dna_to_6bit(dna_code))
else:
    if(args.ascii):

        # Check if message contains bad characters
        pattern = r'[^\x00-\xFF]'
        if(not args.force and re.search(pattern, input_message)):
            # Invalid characters
            sys.stderr.write("Invalid message: May only contain extended ascii characters")
            exit(-7)
        if(args.binary):
            print(convert_ascii_to_binary(input_message))
        else:
            # Encode and print
            binary = convert_ascii_to_binary(input_message)
            dna = convert_binary_to_dna(binary)
            dna_with_separator = args.separator.join([dna[i:i+4] for i in range(0, len(dna), 4)])

            print(dna_with_separator)
    else:

        #Check if message contains bad characters
        pattern = r'[^a-zA-Z0-9 .]'
        if(not args.force and re.search(pattern, input_message)):
            # Invalid characters
            sys.stderr.write("Invalid message: May only contain [a-zA-Z0-9 .], use --ascii if you need more characters")
            exit(-6)

        # Encode and print
        dna_code = convert_6bit_to_dna(input_message)
        if(args.binary):
            print(convert_dna_to_binary(dna_code))
        else:
            dna_with_separator = args.separator.join([dna_code[i:i+3] for i in range(0, len(dna_code), 3)])
            print(dna_with_separator)

