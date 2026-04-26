from pathlib import Path

import atom_parser as ap


def main():
    print("Hello from atom-format!")
    ap.parse_atom_file(Path("./atom.xml"))


if __name__ == "__main__":
    main()
