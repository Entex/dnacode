# DNA Code

## Description
Simple program to convert ascii to a DNA string and vice versa.

## Usage
```
usage: dnacode.py [-h] [-d] [-b] [--separator SEPARATOR] [--force]
                  [message]

DNA Code encoder/decoder

positional arguments:
  message               Message used in encoding/decoding

options:
  -h, --help            show this help message and exit
  -d                    Decode message instead of encode
  -b                    Encode/decode from or to binary (auto detec in
                        decode mode)
  --separator SEPARATOR
                        Set separator, DEFAULT=' ' (space)
  --force               skip validation and try to force a result
```

Example encoding:

`python3 dnacode.py "Hello world"`

output:

`GAC ACA AGT AGT ATG TTG CCG ATG CAC AGT AAT`


Example decoding:

`python3 dnacode.py -d "GAC ACA AGT AGT ATG TTG CCG ATG CAC AGT AAT"`

output:

`Hello world`
