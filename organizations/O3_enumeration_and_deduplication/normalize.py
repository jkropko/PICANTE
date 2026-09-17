#!/usr/bin/env python3
"""
normalize.py — shared normalization for O3 enumeration.

Everything here is DETERMINISTIC and REVERSIBLE in the sense that matters:
the raw value is always retained on the record alongside the normalized one.
Normalization exists to make records comparable, never to replace what a
frame actually said.

WHAT THIS MODULE MUST NOT DO
    Decide anything. `us_location_guess` returns UNKNOWN freely and is used
    only to keep a record inside or outside a frame's declared boundary; it
    is NOT criterion C2, which is a human determination made at O4 from the
    organization's own materials. Wiring this function to C2 would silently
    replace a registered human judgment with a string match.
"""
from __future__ import annotations

import re
import unicodedata

SCRIPT_VERSION = "1.0.0"

# --------------------------------------------------------------------- names

# Stripped before comparison. Deliberately short: these are corporate-form
# suffixes only. Words that change what an organization IS — foundation,
# institute, lab, network — are never stripped, because "X Foundation" and
# "X" can be different entities and merging them is a human call.
_LEGAL_SUFFIXES = {
    "inc", "incorporated", "llc", "l l c", "ltd", "limited", "corp",
    "corporation", "co", "pbc", "plc", "gmbh", "nonprofit", "non profit",
    "501c3", "501 c 3",
}

_PUNCT = re.compile(r"[^\w\s]", re.UNICODE)
_WS = re.compile(r"\s+")


def strip_accents(s: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c)
    )


def normalize_name(raw: str | None) -> str:
    """Comparison key for an organization name. Never displayed, never stored
    in place of the verbatim name."""
    if not raw:
        return ""
    s = strip_accents(str(raw)).lower()
    s = s.replace("&", " and ")
    s = _PUNCT.sub(" ", s)
    s = _WS.sub(" ", s).strip()
    if s.startswith("the "):
        s = s[4:]
    tokens = [t for t in s.split(" ") if t]
    while tokens and tokens[-1] in _LEGAL_SUFFIXES:
        tokens.pop()
    return " ".join(tokens)


def name_tokens(raw: str | None) -> frozenset[str]:
    return frozenset(t for t in normalize_name(raw).split(" ") if t)


# ------------------------------------------------------------------- domains

# Multi-label public suffixes we are likely to meet. Not a full PSL; a full
# PSL would be a dependency and this list covers the cases in a US-focused
# frame set. Anything not listed falls back to the last two labels.
_MULTI_SUFFIXES = {
    "co.uk", "org.uk", "ac.uk", "gov.uk", "com.au", "org.au", "co.nz",
    "co.za", "com.br", "org.br", "co.in", "org.in", "com.mx", "gov.in",
}

_SCHEME = re.compile(r"^[a-z][a-z0-9+.\-]*://", re.I)


def registrable_domain(url: str | None) -> str:
    """Host reduced to its registrable domain. Empty string when unusable.

    Two organizations sharing a registrable domain are a strong merge
    candidate — but only a candidate. Shared domains legitimately occur
    across fiscally sponsored projects on a sponsor's site, which is exactly
    the case Rule 1 routes to a human.
    """
    if not url:
        return ""
    s = str(url).strip()
    if not s:
        return ""
    if not _SCHEME.match(s):
        s = "http://" + s
    try:
        host = s.split("://", 1)[1].split("/", 1)[0]
    except IndexError:
        return ""
    host = host.split("@")[-1].split(":")[0].strip().lower().rstrip(".")
    if not host or " " in host:
        return ""
    if host.startswith("www."):
        host = host[4:]
    labels = [l for l in host.split(".") if l]
    if len(labels) < 2:
        return ""
    last_two = ".".join(labels[-2:])
    if last_two in _MULTI_SUFFIXES and len(labels) >= 3:
        return ".".join(labels[-3:])
    return last_two


# ------------------------------------------------------------------ location

US = "US"
NON_US = "NON_US"
UNKNOWN = "UNKNOWN"

_US_STATES = {
    "alabama", "alaska", "arizona", "arkansas", "california", "colorado",
    "connecticut", "delaware", "florida", "georgia", "hawaii", "idaho",
    "illinois", "indiana", "iowa", "kansas", "kentucky", "louisiana", "maine",
    "maryland", "massachusetts", "michigan", "minnesota", "mississippi",
    "missouri", "montana", "nebraska", "nevada", "new hampshire", "new jersey",
    "new mexico", "new york", "north carolina", "north dakota", "ohio",
    "oklahoma", "oregon", "pennsylvania", "rhode island", "south carolina",
    "south dakota", "tennessee", "texas", "utah", "vermont", "virginia",
    "washington", "west virginia", "wisconsin", "wyoming",
    "district of columbia", "puerto rico",
}

_US_ABBR = {
    "al", "ak", "az", "ar", "ca", "co", "ct", "de", "fl", "ga", "hi", "id",
    "il", "in", "ia", "ks", "ky", "la", "me", "md", "ma", "mi", "mn", "ms",
    "mo", "mt", "ne", "nv", "nh", "nj", "nm", "ny", "nc", "nd", "oh", "ok",
    "or", "pa", "ri", "sc", "sd", "tn", "tx", "ut", "vt", "va", "wa", "wv",
    "wi", "wy", "dc", "pr",
}

_US_COUNTRY = {"united states", "united states of america", "usa", "us", "u s a", "u s"}

# Non-US signals. Short list of countries that actually appear in these
# frames (CFA carries Poland and Germany; McGovern spans 13 countries).
# A location this list does not recognize is UNKNOWN, not non-US.
_NON_US_COUNTRIES = {
    "afghanistan", "argentina", "australia", "austria", "bangladesh", "belgium",
    "brazil", "bulgaria", "canada", "chile", "china", "colombia", "croatia",
    "czech republic", "czechia", "denmark", "ecuador", "egypt", "estonia",
    "ethiopia", "finland", "france", "germany", "ghana", "greece", "guatemala",
    "hungary", "india", "indonesia", "ireland", "israel", "italy", "japan",
    "jordan", "kenya", "latvia", "lebanon", "liberia", "lithuania", "malawi",
    "malaysia", "mexico", "morocco", "nepal", "netherlands", "new zealand",
    "nigeria", "norway", "pakistan", "peru", "philippines", "poland",
    "portugal", "romania", "rwanda", "senegal", "serbia", "sierra leone",
    "singapore", "slovakia", "slovenia", "south africa", "south korea",
    "korea", "spain", "sri lanka", "sweden", "switzerland", "taiwan",
    "tanzania", "thailand", "tunisia", "turkey", "uganda", "ukraine",
    "united kingdom", "uk", "england", "scotland", "wales", "uruguay",
    "vietnam", "zambia", "zimbabwe",
}


def _loc_tokens(raw: str) -> list[str]:
    s = strip_accents(str(raw)).lower()
    s = s.replace("/", ",").replace("|", ",").replace(";", ",")
    parts = [p.strip() for p in s.split(",")]
    return [_WS.sub(" ", _PUNCT.sub(" ", p)).strip() for p in parts if p.strip()]


def us_location_guess(raw: str | None) -> str:
    """US / NON_US / UNKNOWN from a free-text location string.

    Conservative by construction and asymmetric on purpose: an unrecognized
    string is UNKNOWN, never NON_US, so nothing leaves a frame because this
    function failed to recognize it. Under the boundary rule in frames.json,
    UNKNOWN records stay inside the frame and a human settles them at O4.
    """
    if raw is None:
        return UNKNOWN
    parts = _loc_tokens(raw)
    if not parts:
        return UNKNOWN
    joined = " ".join(parts)
    for p in parts:
        if p in _US_COUNTRY or p in _US_STATES:
            return US
        if len(p) == 2 and p in _US_ABBR:
            return US
    for p in parts:
        if p in _NON_US_COUNTRIES:
            return NON_US
    # Trailing bare state name inside an unsplit string: "Akron Ohio".
    for state in _US_STATES:
        if joined.endswith(" " + state):
            return US
    return UNKNOWN


def normalize_country(raw: str | None) -> str:
    """Country field reduced for boundary tests. Empty string when blank."""
    if raw is None:
        return ""
    s = _WS.sub(" ", _PUNCT.sub(" ", strip_accents(str(raw)).lower())).strip()
    if not s:
        return ""
    if s in _US_COUNTRY:
        return "united states"
    return s


def is_blank(v) -> bool:
    return v is None or (isinstance(v, str) and not v.strip())
