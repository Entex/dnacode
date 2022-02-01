# DNA Code

Simple program to convert text to a DNA string and vice versa.

## Usage
```
usage: dnacode.py [-h] [-d] [-b] [--separator SEPARATOR] [--force] [--ascii] [--version] [message]

DNA Code encoder/decoder

positional arguments:
  message               Message used in encoding/decoding

options:
  -h, --help            show this help message and exit
  -d                    Decode message instead of encode
  -b                    Encode/decode from or to binary (auto detec in decode mode)
  --separator SEPARATOR
                        Set separator, DEFAULT=' ' (space)
  --force               skip validation and try to force a result
  --ascii               use extended ascii representation instead of 6-bit [a-zA-Z0-9 .]
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

This allowes for 64 characters: a-z, A-Z, 0-9, (space) and (dot).

To extend this to 8-bit use `--ascii` flag to enable extended ascii
