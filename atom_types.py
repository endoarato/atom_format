"""
Data types for ATOM XML lang. Adapted from: https://www.ietf.org/rfc/rfc4287.txt
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class AtomEntity:
    base: str
    lang: str
    undefinedAttribs: list


@dataclass
class AtomUri:
    uri: str


@dataclass
class AtomEmailAddress:
    email: str


@dataclass
class AtomText:
    dataType: str  # text, html, or xhtml
    data: str


@dataclass
class AtomPerson:
    name: str
    uri: AtomUri | None
    email: AtomEmailAddress | None
    extensionElements: list | None


@dataclass
class AtomInlineContent:
    dataType: str | None  # can be one of the text dataType or a mimeType
    data: str


@dataclass
class AtomOutOfLineContent:
    dataType: str | None
    src: str


AtomContent = AtomInlineContent | AtomOutOfLineContent


@dataclass
class AtomId:
    uri: AtomUri


@dataclass
class AtomCategory:
    term: str
    scheme: AtomUri | None
    label: str | None
    content: str | None


@dataclass
class AtomGenerator:
    uri: str | None
    version: str | None
    text: str


@dataclass
class AtomLink:
    href: AtomUri
    rel: str | AtomUri | None
    type: str | None
    hreflang: str | None
    title: str | None
    length: str | None
    content: str | None


@dataclass
class AtomLogo:
    uri: AtomUri


@dataclass
class AtomIcon:
    uri: AtomUri


@dataclass
class AtomDate:
    datetime: datetime


@dataclass
class AtomSource:
    authors: list[AtomPerson]
    categories: list[AtomCategory] | None
    contributors: list[AtomPerson] | None
    generator: AtomGenerator | None
    icon: AtomIcon | None
    id: AtomId
    links: list[AtomLink] | None
    logo: AtomLogo | None
    rights: AtomText | None
    subtitle: AtomText | None
    title: AtomText | None
    updated: AtomDate | None
    extensionElements: list | None


@dataclass
class AtomEntry:
    authors: list[AtomPerson] | None
    categories: list[AtomCategory] | None
    content: AtomInlineContent | AtomOutOfLineContent | None
    contributors: list[AtomPerson] | None
    id: AtomId
    links: list[AtomLink] | None
    published: AtomDate | None
    rights: AtomText | None
    source: AtomSource | None
    summary: AtomText | None
    title: AtomText
    updated: AtomDate
    extensionElements: list | None


@dataclass
class AtomFeed:
    authors: list[AtomPerson]
    categories: list[AtomCategory] | None
    contributors: list[AtomPerson] | None
    generator: AtomGenerator | None
    icon: AtomIcon | None
    id: AtomId
    links: list[AtomLink] | None
    logo: AtomLogo | None
    rights: AtomText | None
    subtitle: AtomText | None
    title: AtomText
    updated: AtomDate
    extensionElements: list | None
    entries: list[AtomEntry]


@dataclass
class Atom:
    feed: AtomFeed
