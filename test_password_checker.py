"""Unit tests. Run with:  python3 -m unittest"""

import unittest
from password_checker import check_strength, sha1_hash, count_in_response, load_common_passwords


class TestStrength(unittest.TestCase):

    def setUp(self):
        self.common = load_common_passwords()

    def test_common_password_is_very_weak(self):
        score, rating, tips = check_strength("Password123", self.common)
        self.assertEqual(score, 0)
        self.assertEqual(rating, "Very weak")

    def test_strong_password(self):
        score, rating, tips = check_strength("Blue-Tiger-42-Rain", self.common)
        self.assertEqual(score, 5)
        self.assertEqual(tips, [])

    def test_short_password_gets_length_tip(self):
        score, rating, tips = check_strength("Ab1!", self.common)
        self.assertIn("Use at least 12 characters.", tips)

    def test_repeated_characters_lose_a_point(self):
        score, rating, tips = check_strength("Aaaa-bcdefgh-12", self.common)
        self.assertEqual(score, 4)


class TestBreachHelpers(unittest.TestCase):

    def test_sha1_hash(self):
        # Known SHA-1 of "password"
        self.assertEqual(sha1_hash("password"), "5BAA61E4C9B93F3F0682250B6CF8331B7EE68FD8")

    def test_count_found(self):
        response = "AAAAA:3\n1E4C9B93F3F0682250B6CF8331B7EE68FD8:9659365\nBBBBB:1"
        self.assertEqual(count_in_response("1E4C9B93F3F0682250B6CF8331B7EE68FD8", response), 9659365)

    def test_count_not_found(self):
        self.assertEqual(count_in_response("XYZ", "AAAAA:3\nBBBBB:1"), 0)


if __name__ == "__main__":
    unittest.main()
