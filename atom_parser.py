"""
Parser for ATOM XML lang. Adapted from: https://www.ietf.org/rfc/rfc4287.txt
"""

from pathlib import Path

import atom_types as at


def parse_atom_file(file: Path) -> at.Atom:
    raise NotImplementedError("Parsing Atom Files is not implemented yet")
