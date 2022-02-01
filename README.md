# DNA Code

Simple program to encode text to a DNA string and vice versa.

## Disclaimer
This is not a DNA/RNA Sequence translator of nucleotide to protein sequences or any of the sorts. This program only encodes (and decodes) text into DNA-like sequences.

## Usage
```
usage: dnacode [-h] [-a] [-d] [-b] [-s SEPARATOR] [--remap-agct AGCT] [--remap-6bit MAP6BIT] [--force] [--version] [message]

DNA Code encoder/decoder

positional arguments:
  message               Message used in encoding/decoding

optional arguments:
  -h, --help            show this help message and exit
  -a, --ascii           use extended ascii representation instead of 6-bit [a-zA-Z0-9 .]
  -d, --decode          Decode message instead of encode
  -b, --binary          Encode/decode from or to binary (auto detect in decode mode)
  -s SEPARATOR, --separator SEPARATOR
                        Set separator, DEFAULT=' ' (space)
  --remap-agct AGCT     Remap the binary representation of A, G, C and T. Example input 01101100. (only works with -b)
  --remap-6bit MAP6BIT  Remap 6bit represenation with another characterset (64 characters). (only works with 6bit)
  --force               skip validation and try to force a result
  --version             show program's version number and exit
```

Example encoding:

`python3 dnacode.py "Hello world"`

output:

`GAC ACA AGT AGT ATG TTG CCG ATG CAC AGT AAT`


Example decoding:

`python3 dnacode.py -d "GAC ACA AGT AGT ATG TTG CCG ATG CAC AGT AAT"`

output:

`Hello world`

## Enable more characters
By default dnacode uses a 6-bit representation of the DNA sequence. 

This allows for 64 characters, by default: a-z, A-Z, 0-9, (space) and (dot).
To change the mapping use `--remap-6bit` this flag expects 64 characters.

To extend the number of characters to 8-bit use `--ascii` flag to enable extended ascii. *Note, remap 6bit does not work with ascii.

Example encoding:

`python3 dnacode.py --ascii "wéird chäråçtërs ïñ âscîi #%&/()=@©£$|\[]}{"`

output:

`GTGT TCCG GCCG GTAC GCGA ACAA GCAT GCCA TCGA GTAC TCGG TCGT GTGA TCCT GTAC GTAT ACAA TCTT TTAG ACAA TCAC GTAT GCAT TCTC GCCG ACAA ACAT ACGG ACGC ACTT ACCA ACCG ATTG GAAA CCCG CCAT ACGA GTTA GGTA GGCT GGTG GTTG GTCT`

Example decoding:

`python3 dnacode.py --ascii -d "GTGT TCCG GCCG GTAC GCGA ACAA GCAT GCCA TCGA GTAC TCGG TCGT GTGA TCCT GTAC GTAT ACAA TCTT TTAG ACAA TCAC GTAT GCAT TCTC GCCG ACAA ACAT ACGG ACGC ACTT ACCA ACCG ATTG GAAA CCCG CCAT ACGA GTTA GGTA GGCT GGTG GTTG GTCT"`

output:
`wéird chäråçtërs ïñ âscîi #%&/()=@©£$|\[]}{`

## How it works

### binary representation (by default)
- A = 00
- G = 01
- C = 10
- T = 11

To change the mapping of binary representation, use `--remap-agct` 
this flag expect a binary number of length 8 where every 2 pair must be unique. For example `01101100`

### 6-bit
The 6-bit conversion by default uses similar index table as base64 but lowercase, UPPERCASE, digits, (space) and (dot). Source: CTF challanges
- a = AAA
- b = AAC
- c = AAG
- d = AAT
- e = ACA
- etc...

*FAQ: Why is it orderd in 00, 10, 01, 11 and not 00, 01, 10, 11? Good question, I have no idea. That just how the CTFs have worked...

### Ascii
The ascii conversion is based on a proposal for encoding ascii in DNA standard(see source for more information). 
The idea is to convert the binary ascii representation of a character into 4 DNA characters (see binary representation above).
The letters `DNA` will thus become
```
01000100 01001110 01000001
 G A G A  G A T C  G A A G
```
I extended this to include the extended ascii table. Source: https://www.aleph.se/Trans/Individual/Body/ascii.html

## works with pipes as well
```bash
echo "Hello pipes" > test.txt
cat test.txt | python3 dnacode.py | python3 dnacode.py -d

output:
Hello pipes
```
