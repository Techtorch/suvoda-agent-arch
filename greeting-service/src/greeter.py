"""Business logic for the greeting service."""

from src.formats import TEMPLATES, render_greeting, supported_languages

DEFAULT_LANGUAGE = "en"
DEFAULT_NAME = "world"
MAX_NAME_LENGTH = 50


def _normalize_name(name):
    if name is None:
        return DEFAULT_NAME

    normalized = name.strip()
    return normalized or DEFAULT_NAME


def _normalize_language(language):
    if language is None:
        return DEFAULT_LANGUAGE

    normalized = language.strip()
    return normalized or DEFAULT_LANGUAGE


def build_response(name=None, lang=None):
    """Return an HTTP-style status code and JSON-serializable payload."""
    language = _normalize_language(lang)
    if language not in TEMPLATES:
        return 400, {
            "error": "Unsupported language",
            "supported_languages": list(supported_languages()),
        }

    normalized_name = _normalize_name(name)
    if len(normalized_name) > MAX_NAME_LENGTH:
        return 400, {
            "error": f"Name must be {MAX_NAME_LENGTH} characters or fewer"
        }

    return 200, {
        "greeting": render_greeting(language, normalized_name),
        "language": language,
    }
