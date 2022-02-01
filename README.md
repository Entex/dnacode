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
  -b                    Encode/decode from or to binary (auto detect in decode mode)
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

## works with pipes as well
```bash
echo "Hello pipes" > test.txt
cat test.txt | python3 dnacode.py | python3 dnacode.py -d

output:
Hello pipes
```
