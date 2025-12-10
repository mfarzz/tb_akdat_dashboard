import re
from typing import Optional, List

# Daftar provinsi di Indonesia
PROVINSI = [
    "aceh", "sumatera utara", "sumatera barat", "riau", "kepulauan riau", "jambi",
    "sumatera selatan", "bangka belitung", "bengkulu", "lampung", "dki jakarta",
    "jakarta", "jawa barat", "jawa tengah", "di yogyakarta", "yogyakarta", "jawa timur",
    "banten", "bali", "nusa tenggara barat", "nusa tenggara timur", "kalimantan barat",
    "kalimantan tengah", "kalimantan selatan", "kalimantan timur", "kalimantan utara",
    "sulawesi utara", "sulawesi tengah", "sulawesi selatan", "sulawesi tenggara",
    "gorontalo", "sulawesi barat", "maluku", "maluku utara", "papua barat", "papua"
]

# Daftar kota besar di Indonesia
KOTA_BESAR = [
    "jakarta", "surabaya", "bandung", "medan", "semarang", "makassar", "palembang",
    "depok", "tangerang", "bekasi", "bandar lampung", "padang", "malang", "pekanbaru",
    "denpasar", "batam", "bogor", "yogyakarta", "surakarta", "pontianak", "banjarmasin",
    "samarinda", "manado", "jambi", "cimahi", "balikpapan", "serang", "mataram",
    "kupang", "jayapura", "ambon", "palu", "kendari", "gorontalo", "ternate", "sorong"
]

# Kata kunci yang mengindikasikan lokasi
LOCATION_KEYWORDS = [
    "di", "dari", "ke", "pada", "di daerah", "di wilayah", "di kota", "di provinsi",
    "berlokasi", "terletak", "berada", "mengenai", "tentang", "di indonesia",
    "di jakarta", "di bandung", "di surabaya", "di medan", "di yogyakarta",
    "viral di", "menyebar di", "beredar di", "ditemukan di", "terjadi di",
    "di pulau", "di sumatera", "di jawa", "di kalimantan", "di sulawesi",
    "di papua", "di bali", "di nusa tenggara", "di maluku"
]

# Pattern untuk menemukan lokasi
LOCATION_PATTERNS = [
    # Pattern: "di [Kota/Provinsi]"
    r'\bdi\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
    # Pattern: "dari [Kota/Provinsi]"
    r'\bdari\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
    # Pattern: "ke [Kota/Provinsi]"
    r'\bke\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
    # Pattern: "[Kota/Provinsi], Indonesia"
    r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*indonesia',
    # Pattern: "Kota [Nama]" atau "Kabupaten [Nama]"
    r'\b(kota|kabupaten)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
    # Pattern: "Provinsi [Nama]"
    r'\bprovinsi\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
]

def _normalize_location(location: str) -> str:
    """Normalize location name"""
    if not location:
        return ""
    
    location = location.strip().lower()
    
    # Normalize common variations
    location = location.replace("dki ", "").replace("di ", "")
    location = location.replace("kota ", "").replace("kabupaten ", "").replace("provinsi ", "")
    
    return location.title()

def _is_valid_location(location: str) -> bool:
    """Check if location is a valid Indonesian location"""
    if not location or len(location) < 3:
        return False
    
    location_lower = location.lower()
    
    # Check against known provinces
    for prov in PROVINSI:
        if prov in location_lower or location_lower in prov:
            return True
    
    # Check against known cities
    for kota in KOTA_BESAR:
        if kota in location_lower or location_lower in kota:
            return True
    
    # Check if it's a common Indonesian location pattern
    # (contains common Indonesian location words)
    if any(word in location_lower for word in ["jakarta", "bandung", "surabaya", "medan", 
                                                "yogyakarta", "bali", "sumatera", "jawa", 
                                                "kalimantan", "sulawesi", "papua", "maluku"]):
        return True
    
    return False

def extract_all_locations(text: str) -> Optional[List[str]]:
    """
    Extract all location mentions from text
    
    Args:
        text: Text content to extract locations from
        
    Returns:
        List of unique locations found, or None if no locations found
    """
    if not text:
        return None
    
    locations = []
    text_lower = text.lower()
    
    # Check for known provinces and cities first (most reliable)
    for prov in PROVINSI:
        pattern = r'\b' + re.escape(prov) + r'\b'
        if re.search(pattern, text_lower, re.IGNORECASE):
            locations.append(prov.title())
    
    for kota in KOTA_BESAR:
        pattern = r'\b' + re.escape(kota) + r'\b'
        if re.search(pattern, text_lower, re.IGNORECASE):
            locations.append(kota.title())
    
    # Check for explicit location mentions with keywords
    keyword_patterns = [
        (r'\bdi\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', "di"),
        (r'\bdari\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', "dari"),
        (r'\bke\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', "ke"),
        (r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*indonesia', "indonesia"),
    ]
    
    for pattern, _ in keyword_patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            if match.lastindex:
                location = match.group(match.lastindex)
            else:
                location = match.group(0)
            
            normalized = _normalize_location(location)
            if normalized and _is_valid_location(normalized):
                locations.append(normalized)
    
    # Use regex patterns
    for pattern in LOCATION_PATTERNS:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            if match.lastindex:
                location = match.group(match.lastindex)
            else:
                location = match.group(0)
            
            normalized = _normalize_location(location)
            if normalized and _is_valid_location(normalized):
                locations.append(normalized)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_locations = []
    for loc in locations:
        loc_lower = loc.lower()
        if loc_lower not in seen:
            seen.add(loc_lower)
            unique_locations.append(loc)
    
    return unique_locations if unique_locations else None

def extract_relevant_location(text: str) -> Optional[str]:
    """
    Extract the most relevant location from text
    Similar to extract_relevant_date, finds location near keywords
    
    Args:
        text: Text content to extract location from
        
    Returns:
        Most relevant location found, or None if no location found
    """
    if not text:
        return None
    
    # First, try to find location near location keywords
    for keyword in LOCATION_KEYWORDS:
        pattern = r'\b' + keyword.replace("di ", r'di\s+').replace("dari ", r'dari\s+') + r'\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)'
        for match in re.finditer(pattern, text, re.IGNORECASE):
            location = match.group(1) if match.lastindex else match.group(0)
            normalized = _normalize_location(location)
            if normalized and _is_valid_location(normalized):
                return normalized
    
    # Check in sentences with location keywords
    sentences = re.split(r'(?<=[.!?])\s+', text)
    for sentence in sentences:
        sentence_lower = sentence.lower()
        if any(kw in sentence_lower for kw in LOCATION_KEYWORDS):
            for keyword in LOCATION_KEYWORDS:
                pattern = r'\b' + keyword.replace("di ", r'di\s+') + r'\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)'
                match = re.search(pattern, sentence, re.IGNORECASE)
                if match:
                    location = match.group(1) if match.lastindex else match.group(0)
                    normalized = _normalize_location(location)
                    if normalized and _is_valid_location(normalized):
                        return normalized
    
    # Check for known locations in text
    text_lower = text.lower()
    
    # Priority: major cities first
    for kota in KOTA_BESAR:
        if re.search(r'\b' + re.escape(kota) + r'\b', text_lower):
            return kota.title()
    
    # Then provinces
    for prov in PROVINSI:
        if re.search(r'\b' + re.escape(prov) + r'\b', text_lower):
            return prov.title()
    
    # Get all locations and return the first one
    all_locations = extract_all_locations(text)
    return all_locations[0] if all_locations else None

# Mapping kota ke provinsi
KOTA_TO_PROVINSI = {
    "jakarta": "DKI Jakarta",
    "surabaya": "Jawa Timur",
    "bandung": "Jawa Barat",
    "medan": "Sumatera Utara",
    "semarang": "Jawa Tengah",
    "makassar": "Sulawesi Selatan",
    "palembang": "Sumatera Selatan",
    "depok": "Jawa Barat",
    "tangerang": "Banten",
    "bekasi": "Jawa Barat",
    "bandar lampung": "Lampung",
    "padang": "Sumatera Barat",
    "malang": "Jawa Timur",
    "pekanbaru": "Riau",
    "denpasar": "Bali",
    "batam": "Kepulauan Riau",
    "bogor": "Jawa Barat",
    "yogyakarta": "DI Yogyakarta",
    "surakarta": "Jawa Tengah",
    "pontianak": "Kalimantan Barat",
    "banjarmasin": "Kalimantan Selatan",
    "samarinda": "Kalimantan Timur",
    "manado": "Sulawesi Utara",
    "jambi": "Jambi",
    "cimahi": "Jawa Barat",
    "balikpapan": "Kalimantan Timur",
    "serang": "Banten",
    "mataram": "Nusa Tenggara Barat",
    "kupang": "Nusa Tenggara Timur",
    "jayapura": "Papua",
    "ambon": "Maluku",
    "palu": "Sulawesi Tengah",
    "kendari": "Sulawesi Tenggara",
    "gorontalo": "Gorontalo",
    "ternate": "Maluku Utara",
    "sorong": "Papua Barat"
}

# Normalisasi nama provinsi untuk konsistensi
PROVINSI_NORMALIZED = {
    "aceh": "Aceh",
    "sumatera utara": "Sumatera Utara",
    "sumatera barat": "Sumatera Barat",
    "riau": "Riau",
    "kepulauan riau": "Kepulauan Riau",
    "jambi": "Jambi",
    "sumatera selatan": "Sumatera Selatan",
    "bangka belitung": "Bangka Belitung",
    "bengkulu": "Bengkulu",
    "lampung": "Lampung",
    "dki jakarta": "DKI Jakarta",
    "jakarta": "DKI Jakarta",
    "jawa barat": "Jawa Barat",
    "jawa tengah": "Jawa Tengah",
    "di yogyakarta": "DI Yogyakarta",
    "yogyakarta": "DI Yogyakarta",
    "jawa timur": "Jawa Timur",
    "banten": "Banten",
    "bali": "Bali",
    "nusa tenggara barat": "Nusa Tenggara Barat",
    "nusa tenggara timur": "Nusa Tenggara Timur",
    "kalimantan barat": "Kalimantan Barat",
    "kalimantan tengah": "Kalimantan Tengah",
    "kalimantan selatan": "Kalimantan Selatan",
    "kalimantan timur": "Kalimantan Timur",
    "kalimantan utara": "Kalimantan Utara",
    "sulawesi utara": "Sulawesi Utara",
    "sulawesi tengah": "Sulawesi Tengah",
    "sulawesi selatan": "Sulawesi Selatan",
    "sulawesi tenggara": "Sulawesi Tenggara",
    "gorontalo": "Gorontalo",
    "sulawesi barat": "Sulawesi Barat",
    "maluku": "Maluku",
    "maluku utara": "Maluku Utara",
    "papua barat": "Papua Barat",
    "papua": "Papua"
}

def _normalize_to_province(location: str) -> Optional[str]:
    """
    Normalize location name to province name
    
    Args:
        location: Location name (can be city or province)
        
    Returns:
        Normalized province name or None
    """
    if not location:
        return None
    
    location_lower = location.strip().lower()
    
    # Remove common prefixes
    location_lower = location_lower.replace("dki ", "").replace("di ", "")
    location_lower = location_lower.replace("kota ", "").replace("kabupaten ", "").replace("provinsi ", "")
    location_lower = location_lower.strip()
    
    # Check if it's already a province
    if location_lower in PROVINSI_NORMALIZED:
        return PROVINSI_NORMALIZED[location_lower]
    
    # Check if it's a city and map to province
    if location_lower in KOTA_TO_PROVINSI:
        return KOTA_TO_PROVINSI[location_lower]
    
    # Try to match with province list (partial match)
    for prov_key, prov_name in PROVINSI_NORMALIZED.items():
        if prov_key in location_lower or location_lower in prov_key:
            return prov_name
    
    # Try to match with city list and get province
    for kota_key, prov_name in KOTA_TO_PROVINSI.items():
        if kota_key in location_lower or location_lower in kota_key:
            return prov_name
    
    return None

def extract_relevant_province(text: str) -> Optional[str]:
    """
    Extract the most relevant province from text
    Maps cities to their provinces
    
    Args:
        text: Text content to extract province from
        
    Returns:
        Most relevant province found, or None if no province found
    """
    if not text:
        return None
    
    # First extract location
    location = extract_relevant_location(text)
    if not location:
        return None
    
    # Normalize to province
    province = _normalize_to_province(location)
    return province

