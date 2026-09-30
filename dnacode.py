#!/usr/bin/env python3
"""Encode text to DNA-like sequences and back."""

import argparse
import itertools
import re
import string
import sys
from collections import Counter
from collections.abc import Iterator, Sequence
from dataclasses import dataclass, field
from enum import IntEnum

__version__ = "1.2.0"

BASES = "AGCT"
DEFAULT_AGCT = "00011011"  # A=00, G=01, C=10, T=11
DEFAULT_6BIT_CHARSET = string.ascii_letters + "1234567890 ."

# Codons in the order AAA, AAC, AAG, AAT, ACA, ... (as used by the CTFs)
CODONS = ["".join(codon) for codon in itertools.product("ACGT", repeat=3)]


class ExitCode(IntEnum):
    """Process exit codes, kept compatible with earlier versions."""

    OK = 0
    INVALID_BINARY = 255
    ODD_BINARY_LENGTH = 254
    INVALID_DNA = 252
    INVALID_DNA_LENGTH_6BIT = 251
    INVALID_6BIT_MESSAGE = 250
    INVALID_ASCII_MESSAGE = 249
    INVALID_DNA_LENGTH_ASCII = 248
    INVALID_AGCT_LENGTH = 247
    INVALID_AGCT = 246
    DUPLICATE_AGCT = 245
    INVALID_CHARSET_LENGTH = 244
    DUPLICATE_CHARSET = 243


class DNACodeError(Exception):
    def __init__(self, message: str, exit_code: ExitCode) -> None:
        super().__init__(message)
        self.exit_code = exit_code


def chunks(text: str, size: int) -> Iterator[str]:
    """Split text into pieces of `size` characters (the last may be shorter)."""
    return (text[i : i + size] for i in range(0, len(text), size))


def duplicates(values: Sequence[str]) -> list[str]:
    return [value for value, count in Counter(values).items() if count > 1]


@dataclass
class Codec:
    """Mappings between DNA bases, binary and the 6-bit character set."""

    agct: str = DEFAULT_AGCT
    charset: str = DEFAULT_6BIT_CHARSET
    base_to_bits: dict[str, str] = field(init=False, repr=False)
    bits_to_base: dict[str, str] = field(init=False, repr=False)
    codon_to_char: dict[str, str] = field(init=False, repr=False)
    char_to_codon: dict[str, str] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        if len(self.agct) != 8:
            raise DNACodeError(
                f"Incorrect length of binary representation of AGCT: {self.agct}",
                ExitCode.INVALID_AGCT_LENGTH,
            )
        if not re.fullmatch(r"[01]{8}", self.agct):
            raise DNACodeError(
                f"Invalid binary representation of AGCT: {self.agct}",
                ExitCode.INVALID_AGCT,
            )
        pairs = list(chunks(self.agct, 2))
        if dupes := duplicates(pairs):
            raise DNACodeError(
                f"Invalid AGCT, found duplicated value(s): {', '.join(dupes)}",
                ExitCode.DUPLICATE_AGCT,
            )

        if len(self.charset) != len(CODONS):
            raise DNACodeError(
                "Invalid characterset for 6-bit representation. "
                f"Expected {len(CODONS)} characters, got {len(self.charset)}",
                ExitCode.INVALID_CHARSET_LENGTH,
            )
        if dupes := duplicates(self.charset):
            raise DNACodeError(
                f"Invalid characterset for 6bit, found duplicated value(s): {', '.join(dupes)}",
                ExitCode.DUPLICATE_CHARSET,
            )

        self.base_to_bits = dict(zip(BASES, pairs, strict=True))
        self.bits_to_base = {bits: base for base, bits in self.base_to_bits.items()}
        self.codon_to_char = dict(zip(CODONS, self.charset, strict=True))
        self.char_to_codon = {char: codon for codon, char in self.codon_to_char.items()}

    # Unknown symbols are skipped, which is what makes --force work.

    def dna_to_binary(self, dna: str) -> str:
        return "".join(self.base_to_bits.get(base, "") for base in dna)

    def binary_to_dna(self, binary: str) -> str:
        return "".join(self.bits_to_base.get(bits, "") for bits in chunks(binary, 2))

    def dna_to_6bit(self, dna: str) -> str:
        return "".join(self.codon_to_char.get(codon, "") for codon in chunks(dna, 3))

    def text_to_dna(self, text: str) -> str:
        return "".join(self.char_to_codon.get(char, "") for char in text)


def ascii_to_binary(text: str, separator: str = "") -> str:
    return separator.join(f"{ord(char):08b}" for char in text)


def binary_to_ascii(binary: str) -> str:
    return "".join(chr(int(byte, 2)) for byte in chunks(binary, 8))


def encode(
    message: str,
    codec: Codec | None = None,
    *,
    ascii: bool = False,
    binary: bool = False,
    separator: str = " ",
    force: bool = False,
) -> str:
    codec = codec or Codec()

    if ascii:
        if not force and re.search(r"[^\x00-\xFF]", message):
            raise DNACodeError(
                "Invalid message: May only contain extended ascii characters",
                ExitCode.INVALID_ASCII_MESSAGE,
            )
        if binary:
            return ascii_to_binary(message, separator)
        dna = codec.binary_to_dna(ascii_to_binary(message))
        return separator.join(chunks(dna, 4))

    if not force and not set(message) <= codec.char_to_codon.keys():
        allowed = "[a-zA-Z0-9 .]" if codec.charset == DEFAULT_6BIT_CHARSET else f"[{codec.charset}]"
        raise DNACodeError(
            f"Invalid message: May only contain {allowed}, use --ascii if you need more characters",
            ExitCode.INVALID_6BIT_MESSAGE,
        )
    dna = codec.text_to_dna(message)
    if binary:
        return separator.join(chunks(codec.dna_to_binary(dna), 6))
    return separator.join(chunks(dna, 3))


def decode(
    message: str,
    codec: Codec | None = None,
    *,
    ascii: bool = False,
    binary: bool = False,
    separator: str = " ",
    force: bool = False,
) -> str:
    codec = codec or Codec()
    if separator:
        message = message.replace(separator, "")

    # Binary input is auto-detected
    if binary or re.search(r"[01]", message):
        if not force:
            if re.search(r"[^01]", message):
                raise DNACodeError(f"Invalid binary: {message}", ExitCode.INVALID_BINARY)
            if len(message) % 2:
                raise DNACodeError(
                    f"Invalid binary, odd number of digits: {message}",
                    ExitCode.ODD_BINARY_LENGTH,
                )
        message = codec.binary_to_dna(message)

    dna = message.upper()
    if not force:
        if re.search(r"[^ACGT]", dna):
            raise DNACodeError(f"Invalid DNA string: {dna}", ExitCode.INVALID_DNA)
        if ascii and len(dna) % 4:
            raise DNACodeError(f"Invalid DNA string: {dna}", ExitCode.INVALID_DNA_LENGTH_ASCII)
        if not ascii and len(dna) % 3:
            raise DNACodeError(f"Invalid DNA string: {dna}", ExitCode.INVALID_DNA_LENGTH_6BIT)

    if ascii:
        return binary_to_ascii(codec.dna_to_binary(dna))
    return codec.dna_to_6bit(dna)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="dnacode", description="DNA Code encoder/decoder")
    parser.add_argument(
        "-a",
        "--ascii",
        action="store_true",
        help="use extended ascii representation instead of 6-bit [a-zA-Z0-9 .]",
    )
    parser.add_argument("-d", "--decode", action="store_true", help="Decode message instead of encode")
    parser.add_argument(
        "-b",
        "--binary",
        action="store_true",
        help="Encode/decode from or to binary (auto detect in decode mode)",
    )
    parser.add_argument("-s", "--separator", default=" ", help="Set separator, DEFAULT=' ' (space)")
    parser.add_argument(
        "--remap-agct",
        dest="agct",
        default=DEFAULT_AGCT,
        help="Remap the binary representation of A, G, C and T. Example input 01101100.",
    )
    parser.add_argument(
        "--remap-6bit",
        dest="charset",
        default=DEFAULT_6BIT_CHARSET,
        help="Remap 6-bit representation with another characterset (64 characters). (only works with 6-bit)",
    )
    parser.add_argument("--force", action="store_true", help="skip validation and try to force a result")
    parser.add_argument(
        "message",
        nargs="?",
        help="Message used in encoding/decoding (read from stdin if omitted)",
    )
    parser.add_argument("--version", action="version", version=f"DNA Code {__version__}")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    message = args.message
    if not message and not sys.stdin.isatty():
        message = "\n".join(sys.stdin.read().splitlines())
    if not message:
        parser.print_help()
        return ExitCode.OK

    convert = decode if args.decode else encode
    try:
        codec = Codec(agct=args.agct, charset=args.charset)
        result = convert(
            message,
            codec,
            ascii=args.ascii,
            binary=args.binary,
            separator=args.separator,
            force=args.force,
        )
    except DNACodeError as error:
        print(error, file=sys.stderr)
        return error.exit_code

    print(result)
    return ExitCode.OK


if __name__ == "__main__":
    sys.exit(main())
