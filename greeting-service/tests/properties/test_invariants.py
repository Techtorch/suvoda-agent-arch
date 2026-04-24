import json
import random
import string
import unittest

from src.greeter import MAX_NAME_LENGTH, build_response


UNICODE_SAMPLES = ["Ana", "Élodie", "Søren", "東京", "مرحبا"]


def random_name():
    letters = string.ascii_letters + " -'"
    size = random.randint(1, MAX_NAME_LENGTH)
    return "".join(random.choice(letters) for _ in range(size))


class InvariantTests(unittest.TestCase):
    def test_responses_encode_as_utf8_json(self):
        sample_names = UNICODE_SAMPLES + [random_name() for _ in range(25)]
        for name in sample_names:
            status_code, payload = build_response(name=name, lang="en")
            encoded = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            decoded = json.loads(encoded.decode("utf-8"))

            self.assertEqual(200, status_code)
            self.assertEqual(payload, decoded)

    def test_blank_name_falls_back_to_default(self):
        status_code, payload = build_response(name="   ", lang="fr")
        self.assertEqual(200, status_code)
        self.assertEqual(
            {"greeting": "Bonjour, world!", "language": "fr"},
            payload,
        )


if __name__ == "__main__":
    unittest.main()
