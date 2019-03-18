#!/usr/bin/env python
'''
Writes out data received from websocketd on stdin as 
png frames.
'''
# Taken from https://gist.github.com/iandanforth/0ed987bfddf8205b8a23

import time
import base64
import binascii
from sys import stdin, stdout

# From http://stackoverflow.com/a/9807138
def decode_base64(data):
    """Decode base64, padding being optional.

    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.

    """
    missing_padding = 4 - len(data) % 4
    if missing_padding:
        data += str(b'='* missing_padding)
    return base64.b64decode(data)

def main():
    '''
    As each frame is received write it to a .png file
    '''

    frames = 0
    while True:

        received_val = stdin.readline()
        # Right pad filenames so they can be sorted
        filename = str(time.time()).ljust(13, "0") + ".png"
        with open(filename, 'wb') as file_handle:
            try:
                file_handle.write(decode_base64(received_val))
                frames += 1
                if frames % 10 == 0:
                    print("Captured %d frames ..." % frames)
                    stdout.flush()
            except binascii.Error:
                # Ignore malformed data urls
                continue

if __name__ == '__main__':
    main()