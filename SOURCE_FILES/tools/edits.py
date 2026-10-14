"""Text corrections approved by the client (message of 14 Oct 2026).

Each edit matches on the existing manuscript text, so it is skipped (and reported) when an
updated manuscript no longer contains that text. Nothing else in the author's text is changed.
"""
import re

# (block types, old text, new text, note)
EDITS = {
    'en': [
        # Ch. 1 "1/ / Where..." was already corrected by the author in the 14 Oct manuscript ("1. Where...").
        (('chapter',), r'^Scout: where are the real growth opportunities\?$', 'Scouting: where are the real growth opportunities?',
         'Ch. 13 title: "Scout" -> "Scouting" (matches the table of contents, client request)'),
        (('chapter',), r'^performance culture is no coincidence$', 'Performance culture is no coincidence', 'Ch. 3 title: capital P'),
        (('p',), r'^Price negotiations are usually a sign you were too late$', 'Price negotiations are usually a sign you were too late.',
         'Ch. 21: missing full stop added'),
        (('p',), r'^if you find yourself negotiating price', 'If you find yourself negotiating price', 'Ch. 21: sentence starts with a capital'),
    ],
    'nl': [
        (('label',), r'^Praktijkbeeld$', 'Praktijkvoorbeeld', 'Hoofdstuk 1: label "Praktijkbeeld" -> "Praktijkvoorbeeld"'),
        (('p',), r'^uitspraak van Mark Twain:', 'De uitspraak van Mark Twain:', 'Hoofdstuk 26, Stelling: missing article "De" added'),
    ],
}


def apply(blocks, lang):
    log = []
    for types, pat, new, note in EDITS.get(lang, []):
        hit = False
        for b in blocks:
            if b['t'] not in types: continue
            changed = False
            for key in ('text', 'title', 'raw', 'html'):
                if key in b and isinstance(b[key], str):
                    s = b[key]
                    if key == 'raw':  # "Chapter 13 — Scout: ..." : apply to the part after the dash
                        m = re.match(r'^(.*?[—–-]\s*)(.*)$', s)
                        if m and re.search(pat, m.group(2)):
                            b[key] = m.group(1) + re.sub(pat, new, m.group(2), count=1); changed = True
                        continue
                    if re.search(pat, s):
                        b[key] = re.sub(pat, new, s, count=1); changed = True
            if changed: b['edited'] = note; hit = True
        log.append((note, 'applied' if hit else 'NOT FOUND (text changed in manuscript?)'))
    return log
