from unicodedata import normalize


def slugify(text: str):
    clean_text = text.strip().replace(' ', '-').lower()
    while '--' in clean_text:
        clean_text = clean_text.replace('--', '-')
    ascii_text = normalize('NFKD', clean_text).encode('ascii', 'ignore')
    strict_text = map(
        (lambda x: chr(x)
         if x in b'abcdefghijklmnopqrstuvwxyz0123456789-' else ''), ascii_text)
    return ''.join(strict_text)
