"""
Parser for ATOM XML lang. Adapted from: https://www.ietf.org/rfc/rfc4287.txt
"""

import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

import atom_types as AT

ATOM_BASE = {
    "base": "http://www.w3.org/2005/Atom",
    "lang": "xml",
    "undefinedAttribs": [],
}


def find_atom_entities(el: ET.Element, name: str) -> list[ET.Element]:
    print(f"Finding entities `{name}`, parent: `{el}`")
    return el.findall(
        f"{{*}}{name}", namespaces={"atom": "http://www.w3.org/2005/Atom"}
    )


def find_atom_entity(el: ET.Element, name: str) -> ET.Element | None:
    print(f"Finding entity `{name}`, parent: `{el}`")
    return el.find(f"{{*}}{name}", namespaces={"atom": "http://www.w3.org/2005/Atom"})


def parse_atom_uri(parent: ET.Element) -> AT.AtomUri | None:
    el = find_atom_entity(parent, "uri")
    if el is None:
        return None
    return AT.AtomUri(uri=el.text or "")


def parse_atom_links(parent: ET.Element) -> list[AT.AtomLink]:
    els = find_atom_entities(parent, "link")
    return [
        AT.AtomLink(
            href=AT.AtomUri(uri=el.attrib.get("href") or ""),
            rel=el.attrib.get("rel"),
            type=el.attrib.get("type"),
            hreflang=None,  # TODO
            title=el.attrib.get("title"),
            length=el.attrib.get("length"),
            content=None,  # TODO
        )
        for el in els
    ]


def parse_atom_email(parent: ET.Element) -> AT.AtomEmailAddress | None:
    el = find_atom_entity(parent, "email")
    if el is None:
        return el
    return AT.AtomEmailAddress(email=el.text or "")


def parse_atom_authors(parent: ET.Element) -> list[AT.AtomPerson]:
    els = find_atom_entities(parent, "author")
    return [
        AT.AtomPerson(
            name=find_atom_entity(el, "name").text or ""
            if find_atom_entity(el, "name") is not None
            else "",
            uri=parse_atom_uri(el),
            email=parse_atom_email(el),
            extensionElements=None,
        )
        for el in els
        if find_atom_entity(el, "name") is not None
    ]


def parse_atom_updated(parent: ET.Element) -> AT.AtomDate:
    el = find_atom_entity(parent, "updated")
    if el is None:
        raise ValueError("could not parse file")
    return AT.AtomDate(datetime=datetime.fromisoformat(el.text or ""))


def parse_atom_published(parent: ET.Element) -> AT.AtomDate:
    el = find_atom_entity(parent, "published")
    if el is None:
        raise ValueError("could not parse file")
    return AT.AtomDate(datetime=datetime.fromisoformat(el.text or ""))


def parse_atom_title(parent: ET.Element) -> AT.AtomText:
    el = find_atom_entity(parent, "title")
    if el is None:
        raise ValueError("could not parse file")
    return AT.AtomText(dataType="text", data=el.text or "")


def parse_atom_id(parent: ET.Element) -> AT.AtomId:
    el = find_atom_entity(parent, "id")
    if el is None:
        raise ValueError("could not parse file")
    return AT.AtomId(uri=AT.AtomUri(uri=el.text or ""))


def parse_atom_categories(parent: ET.Element) -> list[AT.AtomCategory]:
    els = find_atom_entities(parent, "category")
    return [
        AT.AtomCategory(
            term=el.attrib.get("term") or "",
            scheme=parse_atom_uri(el),
            label=el.attrib.get("label"),
            content=el.text,
        )
        for el in els
    ]


def parse_atom_content(parent: ET.Element) -> AT.AtomContent:
    el = find_atom_entity(parent, "content")
    return AT.AtomInlineContent(dataType=None, data="")  # TODO


def parse_atom_contributors(parent: ET.Element) -> list[AT.AtomPerson]:
    els = find_atom_entities(parent, "contributor")
    return [
        AT.AtomPerson(
            name=find_atom_entity(el, "name").text or ""
            if find_atom_entity(el, "name") is not None
            else "",
            uri=parse_atom_uri(el),
            email=parse_atom_email(el),
            extensionElements=None,
        )
        for el in els
        if find_atom_entity(el, "name") is not None
    ]


def parse_atom_rights(parent: ET.Element) -> AT.AtomText | None:
    el = find_atom_entity(parent, "rights")
    if el is None:
        return el
    return AT.AtomText(dataType="text", data=el.text or "")


def parse_atom_summary(parent: ET.Element) -> AT.AtomText | None:
    el = find_atom_entity(parent, "summary")
    if el is None:
        return el
    return AT.AtomText(dataType="text", data=el.text or "")


def parse_atom_subtitle(parent: ET.Element) -> AT.AtomText | None:
    el = find_atom_entity(parent, "subtitle")
    if el is None:
        return el
    return AT.AtomText(dataType="text", data=el.text or "")


def parse_atom_generator(parent: ET.Element) -> AT.AtomGenerator | None:
    el = find_atom_entity(parent, "generator")
    if el is None:
        return el
    return AT.AtomGenerator(
        uri=el.attrib.get("uri"), version=el.attrib.get("version"), text=el.text or ""
    )


def parse_atom_icon(parent: ET.Element) -> AT.AtomIcon | None:
    el = find_atom_entity(parent, "icon")
    if el is None:
        return el
    return AT.AtomIcon(uri=parse_atom_uri(el))


def parse_atom_logo(parent: ET.Element) -> AT.AtomLogo | None:
    el = find_atom_entity(parent, "logo")
    if el is None:
        return el
    return AT.AtomLogo(uri=parse_atom_uri(el))


def parse_atom_source(parent: ET.Element) -> AT.AtomSource | None:
    el = find_atom_entity(parent, "source")
    if el is None:
        return el
    return AT.AtomSource(
        authors=parse_atom_authors(el),
        categories=parse_atom_categories(el),
        contributors=parse_atom_contributors(el),
        generator=parse_atom_generator(el),
        icon=parse_atom_icon(el),
        id=parse_atom_id(el),
        links=parse_atom_links(el),
        logo=parse_atom_logo(el),
        rights=parse_atom_rights(el),
        subtitle=parse_atom_subtitle(el),
        title=parse_atom_title(el),
        updated=parse_atom_updated(el),
        extensionElements=None,
    )


def parse_atom_entries(parent: ET.Element) -> list[AT.AtomEntry]:
    els = find_atom_entities(parent, "entry")
    return [
        AT.AtomEntry(
            authors=parse_atom_authors(el),
            categories=parse_atom_categories(el),
            content=parse_atom_content(el),
            contributors=parse_atom_contributors(el),
            id=parse_atom_id(el),
            links=parse_atom_links(el),
            published=parse_atom_published(el),
            rights=parse_atom_rights(el),
            source=parse_atom_source(el),
            summary=parse_atom_summary(el),
            title=parse_atom_title(el),
            updated=parse_atom_updated(el),
            extensionElements=None,
        )
        for el in els
    ]


def parse_atom_feed(el: ET.Element) -> AT.AtomFeed:
    return AT.AtomFeed(
        authors=parse_atom_authors(el),
        categories=parse_atom_categories(el),
        contributors=parse_atom_contributors(el),
        generator=parse_atom_generator(el),
        icon=parse_atom_icon(el),
        id=parse_atom_id(el),
        links=parse_atom_links(el),
        logo=parse_atom_logo(el),
        rights=parse_atom_rights(el),
        subtitle=parse_atom_subtitle(el),
        title=parse_atom_title(el),
        updated=parse_atom_updated(el),
        extensionElements=None,
        entries=parse_atom_entries(el),
    )


def parse_atom_file(file: Path) -> AT.Atom:
    with open(file, "r") as atom_file:
        feed_el = ET.fromstring(atom_file.read())
        feed = parse_atom_feed(feed_el)
        print(feed)
        return AT.Atom(feed=feed)
