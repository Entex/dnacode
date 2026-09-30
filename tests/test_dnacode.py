import contextlib
import io
import unittest

from dnacode import Codec, DNACodeError, ExitCode, decode, encode, main

WEIRD = "wéird chäråçtërs ïñ âscîi #%&/()=@©£$|\\[]}{"


class RoundTripTest(unittest.TestCase):
    def test_6bit(self):
        self.assertEqual(encode("Hello world"), "GAC ACA AGT AGT ATG TTG CCG ATG CAC AGT AAT")
        self.assertEqual(decode("GAC ACA AGT AGT ATG TTG CCG ATG CAC AGT AAT"), "Hello world")

    def test_ascii(self):
        self.assertEqual(encode("DNA", ascii=True), "GAGA GATC GAAG")
        self.assertEqual(decode(encode(WEIRD, ascii=True), ascii=True), WEIRD)

    def test_binary(self):
        self.assertEqual(encode("DNA", ascii=True, binary=True), "01000100 01001110 01000001")
        self.assertEqual(encode("Hi", binary=True), "010010 000100")
        # Binary input is auto-detected when decoding
        self.assertEqual(decode("010010 000100"), "Hi")
        self.assertEqual(decode("01000100 01001110 01000001", ascii=True), "DNA")

    def test_separator(self):
        self.assertEqual(encode("ab cd", separator=","), "AAA,AAC,TTG,AAG,AAT")
        self.assertEqual(decode("AAAAAC", separator=""), "ab")

    def test_lowercase_dna(self):
        self.assertEqual(decode("gac aga"), "Hi")

    def test_remap_agct(self):
        codec = Codec(agct="11100100")
        self.assertEqual(encode("Hi", codec, binary=True), "101101 111011")
        self.assertEqual(decode("101101 111011", codec), "Hi")

    def test_remap_charset(self):
        codec = Codec(charset="ZYXWVUTSRQPONMLKJIHGFEDCBAzyxwvutsrqponmlkjihgfedcba0987654321._")
        self.assertEqual(encode("Hi", codec), "CAG GGT")
        self.assertEqual(decode("CAG GGT", codec), "Hi")


class ValidationTest(unittest.TestCase):
    def assertFails(self, code, func, *args, **kwargs):
        with self.assertRaises(DNACodeError) as ctx:
            func(*args, **kwargs)
        self.assertEqual(ctx.exception.exit_code, code)

    def test_codec(self):
        self.assertFails(ExitCode.INVALID_AGCT_LENGTH, Codec, agct="1110010")
        self.assertFails(ExitCode.INVALID_AGCT, Codec, agct="0a1b0c1d")
        self.assertFails(ExitCode.DUPLICATE_AGCT, Codec, agct="11111111")
        self.assertFails(ExitCode.INVALID_CHARSET_LENGTH, Codec, charset="abc")
        self.assertFails(ExitCode.DUPLICATE_CHARSET, Codec, charset="a" * 64)

    def test_encode(self):
        self.assertFails(ExitCode.INVALID_6BIT_MESSAGE, encode, "Hi!")
        self.assertFails(ExitCode.INVALID_ASCII_MESSAGE, encode, "日本", ascii=True)

    def test_decode(self):
        self.assertFails(ExitCode.INVALID_BINARY, decode, "0101 012")
        self.assertFails(ExitCode.ODD_BINARY_LENGTH, decode, "010")
        self.assertFails(ExitCode.INVALID_DNA, decode, "GAC AGX")
        self.assertFails(ExitCode.INVALID_DNA_LENGTH_6BIT, decode, "GACA")
        self.assertFails(ExitCode.INVALID_DNA_LENGTH_ASCII, decode, "GAC", ascii=True)

    def test_force(self):
        self.assertEqual(encode("Hi!", force=True), "GAC AGA")
        self.assertEqual(decode("GAC AGX", force=True), "H")
        self.assertEqual(decode("010", force=True), "")


class CliTest(unittest.TestCase):
    def run_main(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = main(list(argv))
        return code, out.getvalue(), err.getvalue()

    def test_encode_decode(self):
        self.assertEqual(self.run_main("Hi"), (0, "GAC AGA\n", ""))
        self.assertEqual(self.run_main("-d", "GAC AGA"), (0, "Hi\n", ""))

    def test_error(self):
        self.assertEqual(self.run_main("Hi!")[:1], (ExitCode.INVALID_6BIT_MESSAGE,))


if __name__ == "__main__":
    unittest.main()
