"""Greeting formats used by the showcase service."""

TEMPLATES = {
    "en": "Hello, {name}!",
    "es": "Hola, {name}!",
    "fr": "Bonjour, {name}!",
}


def supported_languages():
    """Return the supported language codes in a stable order."""
    return tuple(sorted(TEMPLATES))


def render_greeting(language, name):
    """Render the greeting for a validated language and name."""
    return TEMPLATES[language].format(name=name)
