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
class AtomUri(AtomEntity):
    uri: str


@dataclass
class AtomEmailAddress(AtomEntity):
    email: str


@dataclass
class AtomText(AtomEntity):
    dataType: str  # text, html, or xhtml
    data: str


@dataclass
class AtomPerson(AtomEntity):
    name: str
    uri: AtomUri | None
    email: AtomEmailAddress | None
    extensionElements: list | None


@dataclass
class AtomInlineContent(AtomEntity):
    dataType: str | None  # can be one of the text dataType or a mimeType
    data: str


@dataclass
class AtomOutOfLineContent(AtomEntity):
    dataType: str | None
    src: str


@dataclass
class AtomId(AtomEntity):
    uri: AtomUri


@dataclass
class AtomCategory(AtomEntity):
    term: str
    scheme: AtomUri | None
    label: str | None
    content: str | None


@dataclass
class AtomGenerator(AtomEntity):
    uri: str | None
    version: str | None
    text: str


@dataclass
class AtomLink(AtomEntity):
    href: AtomUri
    rel: str | AtomUri | None
    type: str | None
    hreflang: str | None
    title: str | None
    length: str | None
    content: str | None


@dataclass
class AtomLogo(AtomEntity):
    uri: AtomUri


@dataclass
class AtomIcon(AtomEntity):
    uri: AtomUri


@dataclass
class AtomDate(AtomEntity):
    datetime: datetime


@dataclass
class AtomSource(AtomEntity):
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
class AtomEntry(AtomEntity):
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
class AtomFeed(AtomEntity):
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
class Atom(AtomEntity):
    feed: AtomFeed
