# DNA Code

Simple program to encode text to a DNA string and vice versa.

## Disclaimer
This is not a DNA/RNA Sequence translator of nucleotide to protein sequences or any of the sorts. This program only encodes (and decodes) text into DNA-like sequences.

## Usage
```
usage: dnacode [-h] [-a] [-d] [-b] [-s SEPARATOR] [--force] [--version] [message]

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

This allows for 64 characters: a-z, A-Z, 0-9, (space) and (dot).

To extend this to 8-bit use `--ascii` flag to enable extended ascii

Example encoding:

`python3 dnacode.py --ascii "wéird chäråçtërs ïñ âscîi #%&/()=@©£$|\[]}{"`

output:

`GTGT TCCG GCCG GTAC GCGA ACAA GCAT GCCA TCGA GTAC TCGG TCGT GTGA TCCT GTAC GTAT ACAA TCTT TTAG ACAA TCAC GTAT GCAT TCTC GCCG ACAA ACAT ACGG ACGC ACTT ACCA ACCG ATTG GAAA CCCG CCAT ACGA GTTA GGTA GGCT GGTG GTTG GTCT`

Example decoding:

`python3 dnacode.py --ascii -d "GTGT TCCG GCCG GTAC GCGA ACAA GCAT GCCA TCGA GTAC TCGG TCGT GTGA TCCT GTAC GTAT ACAA TCTT TTAG ACAA TCAC GTAT GCAT TCTC GCCG ACAA ACAT ACGG ACGC ACTT ACCA ACCG ATTG GAAA CCCG CCAT ACGA GTTA GGTA GGCT GGTG GTTG GTCT"`

output:
`wéird chäråçtërs ïñ âscîi #%&/()=@©£$|\[]}{`

## How it works
The 6-bit conversion is similar to base64 but lowercase, UPPERCASE, digits, (space) and (dot). Source: CTF challanges

The ascii conversion is based on a proposal for encoding ascii in DNA standard. I extended this to include the extended ascii table. Source: https://www.aleph.se/Trans/Individual/Body/ascii.html

## works with pipes as well
```bash
echo "Hello pipes" > test.txt
cat test.txt | python3 dnacode.py | python3 dnacode.py -d

output:
Hello pipes
```
