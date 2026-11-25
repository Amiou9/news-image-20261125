#!/usr/bin/env python3
"""Wednesday 25 November 2026, in one picture.

The picture beside this file, entry.png, is version A (Klasik): a
dense broadsheet front page on cream paper, its serif masthead
reading "Wednesday, 25 November 2026", summing up the world's
news of that day. Its three lead stories are the Shenzhou-24
launch carrying Pakistan's first astronaut to the Tiangong space
station, the Trump tariff threat that sank tech stocks again, and
the hack of the CIA and ODNI unclassified intelligence network.
Thirty-two further stories, each with its own drawn illustration,
and a world map with every story numbered on it, fill the rest
of the page, with a DATE CHECK footer naming the Tuesday
24 November stories left out.

This program only hands that picture over. It reads the bytes,
walks every PNG chunk and proves each checksum, confirms the
picture fits the competition's size limits, and writes an exact
copy where the grader asks for it. Standard library only, no
network, and a second run writes the same bytes as the first.
"""

import os
import struct
import sys
import zlib
from pathlib import Path

NAME = "entry.png"
SIGNATURE = b"\x89PNG\r\n\x1a\n"
LIMIT_BYTES = 1_048_576
LIMIT_SIDE = 1_024


def fail(reason):
    sys.exit(f"{NAME}: {reason}")


def chunks(data):
    """Yield (kind, payload) for every chunk, proving each CRC."""
    if data[:8] != SIGNATURE:
        fail("does not start with the PNG signature")
    pos = 8
    while pos < len(data):
        if pos + 8 > len(data):
            fail("a chunk header is cut short at the end of the file")
        (size,) = struct.unpack(">I", data[pos:pos + 4])
        kind = data[pos + 4:pos + 8]
        end = pos + 12 + size
        if end > len(data):
            fail(f"the {kind.decode('latin-1')} chunk runs past the end of the file")
        body = data[pos + 8:pos + 8 + size]
        (stored,) = struct.unpack(">I", data[pos + 8 + size:end])
        if zlib.crc32(kind + body) & 0xFFFFFFFF != stored:
            fail(f"the {kind.decode('latin-1')} chunk fails its checksum")
        yield kind, body
        pos = end
        if kind == b"IEND":
            if pos != len(data):
                fail("bytes follow the IEND chunk")
            return


def validate(data):
    """Check the whole picture and return its (width, height)."""
    if len(data) > LIMIT_BYTES:
        fail(f"is {len(data)} bytes, over the 1 MiB limit")
    seen_ihdr = seen_idat = seen_iend = False
    width = height = None
    idat = bytearray()
    first = True
    for kind, body in chunks(data):
        if first and kind != b"IHDR":
            fail("the first chunk is not IHDR")
        first = False
        if kind == b"IHDR":
            if seen_ihdr:
                fail("has two IHDR chunks")
            seen_ihdr = True
            if len(body) != 13:
                fail("the IHDR chunk is not 13 bytes long")
            width, height = struct.unpack(">II", body[:8])
            if width == 0 or height == 0:
                fail("the IHDR chunk names a zero width or height")
            depth, colour, comp, filt, interlace = body[8], body[9], body[10], body[11], body[12]
            allowed = {0: (1, 2, 4, 8, 16), 2: (8, 16), 3: (1, 2, 4, 8),
                       4: (8, 16), 6: (8, 16)}
            if colour not in allowed or depth not in allowed[colour]:
                fail("the IHDR chunk pairs an unknown bit depth with its colour type")
            if comp != 0 or filt != 0 or interlace not in (0, 1):
                fail("the IHDR chunk names an unknown compression, filter or interlace method")
        elif kind == b"IDAT":
            if not body:
                fail("an IDAT chunk is empty")
            idat.extend(body)
            seen_idat = True
        elif kind == b"IEND":
            seen_iend = True
    if not seen_ihdr:
        fail("has no IHDR chunk")
    if not seen_idat:
        fail("has no IDAT chunk, so it carries no image data")
    if not seen_iend:
        fail("has no IEND chunk")
    if not data.endswith(b"\x00\x00\x00\x00IEND\xaeB`\x82"):
        fail("does not end with a whole IEND chunk")
    try:
        zlib.decompress(bytes(idat))
    except zlib.error:
        fail("the IDAT image data does not decompress")
    if width > LIMIT_SIDE or height > LIMIT_SIDE:
        fail(f"is {width}x{height}, over the 1024x1024 limit")
    return width, height


def main():
    here = Path(__file__).resolve().parent
    data = (here / NAME).read_bytes()
    width, height = validate(data)
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / NAME
    target.write_bytes(data)
    if target.read_bytes() != data:
        fail("the output copy does not match the source picture")
    print(f"wrote {target} -- {width}x{height}, {len(data)} bytes")


if __name__ == "__main__":
    main()
