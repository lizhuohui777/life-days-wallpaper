import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('privacy', Path(__file__).resolve().parents[1] / 'scripts/strip_photo_metadata.py')
privacy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(privacy)

def segment(marker, payload):
    return bytes([255, marker]) + (len(payload) + 2).to_bytes(2, 'big') + payload

class JPEGPrivacyTests(unittest.TestCase):
    def test_removes_exif_xmp_iptc_comment_and_trailing_data(self):
        scan = segment(0xDA, b'\x01\x01\x00\x00\x3f\x00') + b'pixels\xff\x00stuffed\xff\xd0restart'
        image = b'\xff\xd8' + segment(0xE1, b'Exif\x00GPS and serial') + segment(0xED, b'IPTC') + segment(0xFE, b'comment') + scan + b'\xff\xd9trailing secret'
        self.assertEqual(privacy.strip_metadata(image), b'\xff\xd8' + scan + b'\xff\xd9')
    def test_preserves_color_profile(self):
        icc = segment(0xE2, b'ICC_PROFILE\x00profile')
        image = b'\xff\xd8' + icc + b'\xff\xd9'
        self.assertEqual(privacy.strip_metadata(image), image)
    def test_invalid_input(self):
        for data in [b'not jpeg', b'\xff\xd8\xff', b'\xff\xd8\xff\xe1\x00\xffshort']:
            with self.assertRaises(ValueError): privacy.strip_metadata(data)

if __name__ == '__main__': unittest.main()
