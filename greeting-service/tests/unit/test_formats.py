import unittest

from src.formats import render_greeting, supported_languages


class FormatTests(unittest.TestCase):
    def test_supported_languages_are_stable(self):
        self.assertEqual(("en", "es", "fr"), supported_languages())

    def test_render_greeting_uses_selected_template(self):
        self.assertEqual("Bonjour, Workshop!", render_greeting("fr", "Workshop"))


if __name__ == "__main__":
    unittest.main()
