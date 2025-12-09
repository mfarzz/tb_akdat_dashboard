import re
import datetime

bulan_map = {
    "januari": "01", "februari": "02", "maret": "03", "april": "04", "mei": "05",
    "juni": "06", "juli": "07", "agustus": "08", "september": "09",
    "oktober": "10", "november": "11", "desember": "12"
}

KEYWORDS = [
    "beredar", "unggahan", "diunggah", "diposting", "pada", "arsip",
    "klaim", "disebut", "dibagikan", "membagikan", "membagikan video",
    "melaporkan", "viral", "menyebar"
]

_PUBLICATION_VERBS = [
    "diposting", "diposting pada", "diunggah", "diunggah pada", "unggah", "unggahan",
    "unggah pada", "mengunggah", "mengunggahnya", "mengunggah pada", "diupload", "upload",
    "dipublikasikan", "dipublikasikan pada", "dibagikan", "dibagikan pada", "posting",
    "posted", "share", "shares", "unggah di", "diunggah di"
]

_now_year = datetime.datetime.now().year
MIN_YEAR = 2018
MAX_YEAR = _now_year + 1

def _valid_date(y: int, m: int, d: int) -> bool:
    if not (MIN_YEAR <= y <= MAX_YEAR):
        return False
    try:
        datetime.date(y, m, d)
        return True
    except ValueError:
        return False

def _two_digit_year_to_4(yy: int) -> int:
    return 2000 + yy if yy < 70 else 1900 + yy

_COUNT_CONTEXT = [
    "akun", "pendaftar", "pendaftaran", "anggota", "orang", "member",
    "pengguna", "jumlah", "total", "pendaftar", "registrant", "subscriber"
]
def _is_likely_count(start_idx: int, end_idx: int, text: str, window: int = 30) -> bool:

    L = len(text)
    s = max(0, start_idx - window)
    e = min(L, end_idx + window)
    snippet = text[s:e].lower()
    if re.search(r'\btahun\b', snippet):
        return False
    for kw in _COUNT_CONTEXT:
        if re.search(r'\b' + re.escape(kw) + r'\b', snippet):
            return True
    return False

_NON_PUB_CONTEXT = [
    "direncanakan", "direncanakan tahun", "disimulasikan", "simulasi", "dilaksanakan",
    "direncanakan pada", "perencanaan", "rencana", "diajukan", "diusulkan",
    "sejak", "sejak tahun", "iup", "iupk", "nomor", "no.", "no", "nº", "sk", "surat", "ijin", "izin",
    "registrasi", "nomor izin", "nomor iup", "nomor iupk", "nomor. ",
    "diambil", "diambil pada", "gambar", "foto", "satelit", "denah", "tangkapan layar", "cuplikan layar",
    "tangkapan", "screenshot", "dibangun", "pembangunan", "dalam pembangunan", "sedang dibangun"
]

def _is_in_non_pub_context(start_idx: int, end_idx: int, text: str, window: int = 40) -> bool:

    L = len(text)
    s = max(0, start_idx - window)
    e = min(L, end_idx + window)
    snippet = text[s:e].lower()

    for kw in _NON_PUB_CONTEXT:
        if kw in snippet:
            return True

    if re.search(r'\b(gambar|foto|satelit|denah|tangkapan layar|cuplikan layar|screenshot)\b', snippet):
        return True

    if re.search(r'\bdiambil\b.*\btahun\b', snippet) or re.search(r'\btahun\b.*\bdiambil\b', snippet):
        return True

    if re.search(r'\bpembangunan\b', snippet) or re.search(r'\bdibangun\b', snippet):
        return True

    if re.search(r'(no\.?|nomor|iupk?|sk|surat)\b', snippet):
        if re.search(r'[\d]+\s*[./-]\s*[\d]+', snippet) or re.search(r'/\s*\d{4}\b', snippet):
            return True

    before = text[max(0, start_idx-3):start_idx]
    if re.search(r'[./-]\s*$', before):
        return True

    return False

def extract_all_dates(text: str):

    if not text:
        return None

    candidates = [] 

    def try_add(y, m, d, score, pos):
        try:
            y_i, m_i, d_i = int(y), int(m), int(d)
            if _valid_date(y_i, m_i, d_i):
                candidates.append((score, pos, f"{y_i:04d}-{m_i:02d}-{d_i:02d}"))
        except Exception:
            pass

    for m in re.finditer(r'(\d{4})[\/\-](\d{1,2})[\/\-](\d{1,2})', text):
        y, mo, d = m.group(1), m.group(2), m.group(3)
        try_add(y, mo, d, 3, m.start())

    for m in re.finditer(r'(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{2})(?!\d)', text):
        d, mo, yy = m.group(1), m.group(2), m.group(3)
        try:
            y4 = _two_digit_year_to_4(int(yy))
            try_add(y4, mo, d, 3, m.start())
        except Exception:
            pass

    for m in re.finditer(r'(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{4})', text):
        d, mo, y = m.group(1), m.group(2), m.group(3)
        try_add(y, mo, d, 3, m.start())

    pattern_text = re.compile(r'(\d{1,2})\s+(Januari|Februari|Maret|April|Mei|Juni|Juli|Agustus|September|Oktober|November|Desember)\s+(\d{4})', flags=re.IGNORECASE)
    for m in pattern_text.finditer(text):
        d, month_name, y = m.group(1), m.group(2), m.group(3)
        mo = bulan_map.get(month_name.lower())
        if mo:
            try_add(y, mo, d, 3, m.start())

    pattern_month_year = re.compile(r'(Januari|Februari|Maret|April|Mei|Juni|Juli|Agustus|September|Oktober|November|Desember)\s+(\d{4})', flags=re.IGNORECASE)
    for m in pattern_month_year.finditer(text):
        month_name, y = m.group(1), m.group(2)
        mo = bulan_map.get(month_name.lower())
        if mo:
            try_add(y, mo, 1, 2, m.start())

    year_range_spans = _find_year_range_spans(text)

    decade_spans = []
    for m in re.finditer(r'\b(19|20)\d{2}\s*(?:-?an|s)\b', text, flags=re.IGNORECASE):
        decade_spans.append((m.start(), m.end()))

    for m in re.finditer(r'\b(19|20)\d{2}\b', text):
        if any(s <= m.start() < e for (s, e) in year_range_spans):
            continue
        if any(s <= m.start() < e for (s, e) in decade_spans):
            continue
        if _is_in_non_pub_context(m.start(), m.end(), text):
            continue
        y = int(m.group(0))
        if MIN_YEAR <= y <= MAX_YEAR:
            if _is_likely_count(m.start(), m.end(), text):
                continue
            try_add(y, 1, 1, 1, m.start())

    if not candidates:
        return None

    candidates.sort(key=lambda t: (-t[0], t[1]))
    seen = set()
    ordered = []
    for _, _, ds in candidates:
        if ds not in seen:
            seen.add(ds)
            ordered.append(ds)
    return ordered if ordered else None

def _find_date_near_publication(text: str, window: int = 80):

    if not text:
        return None
    lower = text.lower()
    pub_re = re.compile(r'\b(?:' + '|'.join(re.escape(v) for v in _PUBLICATION_VERBS) + r')\b', flags=re.IGNORECASE)
    for pv in pub_re.finditer(lower):
        start = max(0, pv.start() - 5)
        end = min(len(text), pv.end() + window)
        snippet = text[start:end]
        after_snippet = text[pv.end():end]
        dates_after = extract_all_dates(after_snippet)
        if dates_after:
            return dates_after[0]
        dates_any = extract_all_dates(snippet)
        if dates_any:
            return dates_any[0]
    return None

def _find_year_range_spans(text: str):

    spans = []
    for m in re.finditer(r'\b(19|20)\d{2}\b\s*(?:-|–|—)\s*\b(19|20)\d{2}\b', text):
        spans.append((m.start(), m.end()))
    for m in re.finditer(r'\b(19|20)\d{2}\b\s*(?:sampai|hingga|sampai dengan|sd|s\.d\.|to)\s*\b(19|20)\d{2}\b', text, flags=re.IGNORECASE):
        spans.append((m.start(), m.end()))
    return spans

def extract_relevant_date(text: str):

    if not text:
        return None

    pub_date = _find_date_near_publication(text)
    if pub_date:
        return pub_date

    for m in re.finditer(r'\(([^\)]+)\)', text):
        inside = m.group(1)
        dates = extract_all_dates(inside)
        if dates:
            return dates[0]

    sentences = re.split(r'(?<=[.!?])\s+', text)
    for sentence in sentences:
        lower = sentence.lower()
        if any(kw in lower for kw in KEYWORDS):
            pub_in_sentence = _find_date_near_publication(sentence)
            if pub_in_sentence:
                return pub_in_sentence
            dates = extract_all_dates(sentence)
            if dates:
                return dates[0]

    all_dates = extract_all_dates(text)
    return all_dates[0] if all_dates else None
