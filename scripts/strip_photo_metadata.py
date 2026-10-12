#!/usr/bin/env python3
"""Remove JPEG EXIF/XMP/IPTC/comments without recompressing image scan data."""
import argparse
from pathlib import Path


def strip_metadata(data: bytes) -> bytes:
    if not data.startswith(b'\xff\xd8'):
        raise ValueError('Only JPEG is supported')
    result = bytearray(data[:2])
    position = 2
    while position < len(data):
        start = position
        if data[position] != 0xFF:
            raise ValueError('Invalid JPEG marker')
        while position < len(data) and data[position] == 0xFF:
            position += 1
        if position >= len(data):
            raise ValueError('Truncated marker')
        marker = data[position]
        position += 1
        if marker == 0xD9:
            result.extend(data[start:position])
            return bytes(result)  # Drop trailing data after EOI.
        if marker == 0x01 or 0xD0 <= marker <= 0xD7:
            result.extend(data[start:position])
            continue
        if position + 2 > len(data):
            raise ValueError('Truncated segment')
        length = int.from_bytes(data[position:position + 2], 'big')
        end = position + length
        if length < 2 or end > len(data):
            raise ValueError('Invalid segment length')
        payload = data[position + 2:end]
        app = 0xE0 <= marker <= 0xEF
        keep = not app and marker != 0xFE
        keep |= marker == 0xE0 and payload.startswith(b'JFIF\x00')
        keep |= marker == 0xE2 and payload.startswith(b'ICC_PROFILE\x00')
        keep |= marker == 0xEE and payload.startswith(b'Adobe')
        if keep:
            result.extend(data[start:end])
        position = end
        if marker == 0xDA:
            scan_start = position
            while position < len(data):
                if data[position] != 0xFF:
                    position += 1
                    continue
                next_byte = position + 1
                while next_byte < len(data) and data[next_byte] == 0xFF:
                    next_byte += 1
                if next_byte >= len(data):
                    raise ValueError('Truncated scan')
                if data[next_byte] == 0 or 0xD0 <= data[next_byte] <= 0xD7:
                    position = next_byte + 1
                    continue
                break
            result.extend(data[scan_start:position])
    raise ValueError('Missing JPEG end marker')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('destination', type=Path)
    args = parser.parse_args()
    cleaned = strip_metadata(args.source.read_bytes())
    if args.source.resolve() == args.destination.resolve():
        raise ValueError('Write to a separate destination; preserve your original')
    args.destination.write_bytes(cleaned)
    print('JPEG metadata removed; compressed pixel data preserved.')


if __name__ == '__main__':
    main()
