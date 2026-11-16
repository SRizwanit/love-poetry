#!/usr/bin/env python3
"""mylove.txt (WhatsApp export) -> site/index.html (প্রেমের কবিতা)"""
import html, re, sys
from pathlib import Path

# ---------- সেটিংস ----------
SOURCE = Path("mylove.txt")
TEMPLATE = Path("template.html")
OUT_DIR = Path("site")
LINES_PER_BOX = 4
WHATSAPP_NUMBER = "01862464634"   # লোকাল ফরম্যাটে; নিচে আন্তর্জাতিক হয়ে যাবে
COUNTRY_CODE = "880"
SENDER_FILTER = None               # যেমন "লাল টমেটো😍😘" দিলে শুধু তার মেসেজ আসবে
SITE_TITLE = "প্রেমের কবিতা"
# ----------------------------

TS = re.compile(
    r"^[\u200e\u200f]?\[?(\d{1,2}/\d{1,2}/\d{2,4}),?\s+\d{1,2}:\d{2}"
    r"(?:[\s\u202f]*[APap][Mm])?\]?\s*[-–]\s*(.*)$"
)
NOISE = ("<media omitted>", "this message was deleted", "you deleted this message",
         "<this message was edited>", "null")


def parse(text):
    """-> [(date, sender, [lines])]"""
    msgs = []
    for raw in text.splitlines():
        line = raw.replace("\u200e", "").replace("\u200f", "").rstrip()
        m = TS.match(line)
        if m:
            date, rest = m.groups()
            if ": " in rest:
                sender, body = rest.split(": ", 1)
                msgs.append([date, sender.strip(), [body]])
            else:                       # সিস্টেম মেসেজ (encryption notice ইত্যাদি)
                msgs.append(None)
        elif msgs and msgs[-1] is not None:
            msgs[-1][2].append(line)    # বহু-লাইনের মেসেজের পরের লাইন
    return [m for m in msgs if m]


def clean(lines):
    out = [l.strip() for l in lines]
    out = [l for l in out if l and l.lower() not in NOISE]
    return out


def chunk(lines, n=LINES_PER_BOX):
    boxes = [lines[i:i + n] for i in range(0, len(lines), n)]
    if len(boxes) > 1 and len(boxes[-1]) == 1:   # একলা ঝুলে থাকা ১ লাইন আগের বক্সে
        last = boxes.pop()
        boxes[-1] += last
    return boxes


def bn(num):
    return str(num).translate(str.maketrans("0123456789", "০১২৩৪৫৬৭৮৯"))


def main():
    if not SOURCE.exists():
        sys.exit(f"{SOURCE} পাওয়া যায়নি")
    msgs = parse(SOURCE.read_text(encoding="utf-8"))
    cards, n = [], 0
    for date, sender, body in msgs:
        if SENDER_FILTER and sender != SENDER_FILTER:
            continue
        for box in chunk(clean(body)):
            n += 1
            lines = "".join(f"<span>{html.escape(l)}</span>" for l in box)
            cards.append(
                f'<article class="card" id="p{n}">'
                f'<span class="no">{bn(n)}</span>'
                f'<p class="poem">{lines}</p>'
                f'<div class="acts">'
                f'<button class="btn copy" type="button">কপি</button>'
                f'<button class="btn share" type="button">হোয়াটসঅ্যাপে শেয়ার</button>'
                f'</div></article>'
            )
    number = COUNTRY_CODE + WHATSAPP_NUMBER.lstrip("0")
    page = (TEMPLATE.read_text(encoding="utf-8")
            .replace("%%TITLE%%", SITE_TITLE)
            .replace("%%COUNT%%", bn(n))
            .replace("%%WA%%", number)
            .replace("%%CARDS%%", "\n".join(cards)))
    OUT_DIR.mkdir(exist_ok=True)
    (OUT_DIR / "index.html").write_text(page, encoding="utf-8")
    (OUT_DIR / ".nojekyll").touch()
    print(f"✔ {n} টি কবিতার বক্স তৈরি হয়েছে -> {OUT_DIR/'index.html'}")


if __name__ == "__main__":
    main()
