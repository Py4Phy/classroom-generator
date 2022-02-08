# base64 and zcompress encode file
# see https://stackoverflow.com/a/28573360

import base64
import zlib
import pathlib

def encode(code):
    return base64.b16encode(zlib.compress(code))

# use run() to run the code
def run(code):
    return exec(zlib.decompress(base64.b16decode(code)))

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Obfuscate Python code")
    parser.add_argument("filename", metavar="FILE",
                        help="filename with function")
    args = parser.parse_args()

    inp = pathlib.Path(args.filename)

    code = encode(inp.read_bytes())
    print(f"""code = {code}""")



