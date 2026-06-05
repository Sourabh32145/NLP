import re
import logging

logger = logging.getLogger(__name__)

import sys
import os

# Ensure we can import from agents
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.ner_agent import MEDICAL_KEYWORDS

# ─────────────────────────────────────────────────────────────────
# Medical terms that get "(English)" added after Kannada translation
# We use the master list from NER, but exclude simple words we don't want bracketed
# ─────────────────────────────────────────────────────────────────
EXCLUDED_FROM_BRACKETS = {"pain", "ache", "aches", "head"}
MEDICAL_TERMS_LIST = [
    term for term in MEDICAL_KEYWORDS.keys()
    if term not in EXCLUDED_FROM_BRACKETS
]
# Sort by length descending so multi-word phrases like "lumbar spine" match before "spine"
MEDICAL_TERMS_LIST.sort(key=len, reverse=True)

# Build a single regex pattern that matches any of these terms
# using \b to ensure word boundaries
_escaped_terms = [re.escape(term) for term in MEDICAL_TERMS_LIST]
_MEDICAL_TERMS_PATTERN = re.compile(r'\b(' + '|'.join(_escaped_terms) + r')\b', re.IGNORECASE)

# ─────────────────────────────────────────────────────────────────
# Structural header translations (applied before Google Translate)
# ─────────────────────────────────────────────────────────────────
HEADER_DICT = {
    "clinical discharge summary": "ಚಿಕಿತ್ಸಕ ಬಿಡುಗಡೆ ಸಾರಾಂಶ",
    "primary diagnoses / diseases": "ಪ್ರಾಥಮಿಕ ರೋಗನಿರ್ಣಯಗಳು / ಕಾಯಿಲೆಗಳು",
    "presenting symptoms": "ಪ್ರಸ್ತುತಪಡಿಸುವ ಲಕ್ಷಣಗಳು",
    "presenting complaints": "ಪ್ರಸ್ತುತ ದೂರುಗಳು",
    "prescribed medications": "ಶಿಫಾರಸು ಮಾಡಿದ ಔಷಧಿಗಳು",
    "affected body parts": "ಬಾಧಿತ ದೇಹದ ಭಾಗಗಳು",
    "clinical course & recommendations": "ಚಿಕಿತ್ಸಕ ಕ್ರಮ ಮತ್ತು ಶಿಫಾರಸುಗಳು",
    "physical examination findings": "ದೈಹಿಕ ಪರೀಕ್ಷೆಯ ಫಲಿತಾಂಶಗಳು",
    "chief complaint": "ಮುಖ್ಯ ದೂರು",
    "history of present illness": "ಪ್ರಸ್ತುತ ಅನಾರೋಗ್ಯದ ಇತಿಹಾಸ",
    "history of present illness (hpi)": "ಪ್ರಸ್ತುತ ಅನಾರೋಗ್ಯದ ಇತಿಹಾಸ (HPI)",
    "review of systems (ros)": "ವ್ಯವಸ್ಥೆಗಳ ವಿಮರ್ಶೆ (ROS)",
    "constitutional": "ಸಾಮಾನ್ಯ ಆರೋಗ್ಯ",
    "cardiovascular": "ಹೃದಯ ರಕ್ತನಾಳ ವ್ಯವಸ್ಥೆ",
    "respiratory": "ಉಸಿರಾಟದ ವ್ಯವಸ್ಥೆ",
    "neurological": "ನರಮಂಡಲ ವ್ಯವಸ್ಥೆ",
    "gastrointestinal": "ಜೀರ್ಣಾಂಗ ವ್ಯವಸ್ಥೆ",
    "musculoskeletal": "ಸ್ನಾಯು-ಅಸ್ಥಿ ವ್ಯವಸ್ಥೆ",
    "internal medicine": "ಆಂತರಿಕ ಔಷಧ",
    "orthopedic": "ಮೂಳೆ ಚಿಕಿತ್ಸೆ",
    "department": "ವಿಭಾಗ",
    "provider": "ವೈದ್ಯರು",
    "date": "ದಿನಾಂಕ",
    "none reported": "ಯಾವುದೂ ವರದಿಯಾಗಿಲ್ಲ",
    "- monitor vitals regularly.": "- ನಿಯಮಿತವಾಗಿ ಪ್ರಮುಖ ಆರೋಗ್ಯ ಸೂಚಕಗಳನ್ನು ಮೇಲ್ವಿಚಾರಣೆ ಮಾಡಿ.",
    "- follow prescribed medication schedule.": "- ಶಿಫಾರಸು ಮಾಡಿದ ಔಷಧಿ ವೇಳಾಪಟ್ಟಿಯನ್ನು ಅನುಸರಿಸಿ.",
    "- patient reported": "- ರೋಗಿ ನೀಡಿದ ವಿವರಣೆ",
    "- consult orthopedic specialist for further evaluation.": "- ಹೆಚ್ಚಿನ ಮೌಲ್ಯಮಾಪನಕ್ಕಾಗಿ ಮೂಳೆ ತಜ್ಞರನ್ನು ಸಂಪರ್ಕಿಸಿ.",
    "discharge summary": "ಬಿಡುಗಡೆ ಸಾರಾಂಶ",
}

# Proper-noun / skip patterns — kept in English
SKIP_PATTERNS = [
    r'^\d{1,2}-[A-Za-z]{3}-\d{4}$',  # 03-Jun-2026
    r'^\d+$',                           # plain numbers
    r'^\d+-\d+$',                       # ranges 5-6
    r'^[A-Z][a-z]+\s[A-Z][a-z]+$',      # full names
    r'^Dr\.',                           # Dr. titles
    r'^MD$|^PhD$|^RN$',                 # qualifications
    r'^[A-Z]{2,}$',                     # acronyms HPI, ROS
]


def _is_skip_token(token: str) -> bool:
    for pat in SKIP_PATTERNS:
        if re.match(pat, token):
            return True
    return False


class Translator:
    def __init__(self, config=None):
        self.config = config
        self._google_translator = None
        self._gt_available = None  # None = untested

    def _get_google_translator(self):
        """Lazily initialise deep_translator GoogleTranslator."""
        if self._gt_available is False:
            return None
        if self._google_translator is not None:
            return self._google_translator
        try:
            from deep_translator import GoogleTranslator
            self._google_translator = GoogleTranslator(source='en', target='kn')
            self._gt_available = True
            logger.info("deep_translator GoogleTranslator initialized.")
        except Exception as e:
            logger.warning(f"deep_translator not available: {e}")
            self._gt_available = False
            self._google_translator = None
        return self._google_translator

    def translate_english_to_kannada(self, text: str) -> str:
        """
        Translates English clinical text to Kannada.
        Priority:
          1. Header/structural exact match (instant, no API call)
          2. Google Translate via deep_translator (with inline tags)
          3. Return original text unchanged (names, dates, etc.)
        """
        stripped = text.strip()
        if not stripped:
            return text

        # 1. Exact header/structural match (case-insensitive)
        key = stripped.lower().rstrip('.')
        if key in HEADER_DICT:
            return HEADER_DICT[key]
        if stripped.lower() in HEADER_DICT:
            return HEADER_DICT[stripped.lower()]

        # 2. Skip proper nouns / dates — keep English
        if _is_skip_token(stripped):
            return text

        # 3. Inject placeholders for medical terms
        word_map = {}
        placeholder_idx = 0
        def replacer(match):
            nonlocal placeholder_idx
            word = match.group(1) # The matched term
            placeholder = f"__{placeholder_idx}__"
            word_map[placeholder] = f"({word.title()})"
            placeholder_idx += 1
            return f"{word} {placeholder}"

        tagged_text = _MEDICAL_TERMS_PATTERN.sub(replacer, stripped)

        # 4. Google Translate
        gt = self._get_google_translator()
        if gt is not None:
            try:
                from deep_translator import GoogleTranslator
                result = GoogleTranslator(source='en', target='kn').translate(tagged_text)
                if result and result.strip():
                    final_text = result.strip()
                    # Restore placeholders to English brackets
                    for placeholder, english_bracket in word_map.items():
                        final_text = final_text.replace(placeholder, english_bracket)
                    return final_text
            except Exception as e:
                logger.warning(f"Google Translate failed: {e}")

        # 5. Final fallback
        return text

    def translate_block(self, text: str) -> str:
        """
        Translates a multi-sentence block paragraph.
        Splits by sentence, translates each, rejoins.
        """
        if not text.strip():
            return text

        # Split into sentences
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        translated_sentences = []
        for sent in sentences:
            if sent.strip():
                translated_sentences.append(self.translate_english_to_kannada(sent.strip()))

        return " ".join(translated_sentences)
