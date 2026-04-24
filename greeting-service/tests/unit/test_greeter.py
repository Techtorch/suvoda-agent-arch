import unittest

from src.greeter import MAX_NAME_LENGTH, build_response


class GreeterTests(unittest.TestCase):
    def test_defaults_are_applied(self):
        status_code, payload = build_response()
        self.assertEqual(200, status_code)
        self.assertEqual(
            {"greeting": "Hello, world!", "language": "en"},
            payload,
        )

    def test_supported_language_is_used(self):
        status_code, payload = build_response(name="Ramy", lang="es")
        self.assertEqual(200, status_code)
        self.assertEqual(
            {"greeting": "Hola, Ramy!", "language": "es"},
            payload,
        )

    def test_name_is_trimmed(self):
        status_code, payload = build_response(name="  Suvoda  ", lang="en")
        self.assertEqual(200, status_code)
        self.assertEqual("Hello, Suvoda!", payload["greeting"])

    def test_name_length_is_limited(self):
        too_long_name = "a" * (MAX_NAME_LENGTH + 1)
        status_code, payload = build_response(name=too_long_name, lang="en")
        self.assertEqual(400, status_code)
        self.assertEqual(
            {"error": f"Name must be {MAX_NAME_LENGTH} characters or fewer"},
            payload,
        )

    def test_unsupported_language_fails(self):
        status_code, payload = build_response(name="Workshop", lang="de")
        self.assertEqual(400, status_code)
        self.assertEqual("Unsupported language", payload["error"])
        self.assertEqual(["en", "es", "fr"], payload["supported_languages"])


if __name__ == "__main__":
    unittest.main()
