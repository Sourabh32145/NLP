import os
import sys

# Set resource path for Indic NLP library if needed
# os.environ['INDIC_RESOURCES_PATH'] = '/path/to/resources'

try:
    from indicnlp.normalize.indic_normalize import IndicNormalizerFactory
    from indicnlp.tokenize import indic_tokenize
    INDIC_NLP_AVAILABLE = True
except ImportError:
    INDIC_NLP_AVAILABLE = False

def normalize_kannada_text(text: str) -> str:
    """
    Normalizes Kannada text to ensure consistent Unicode representation.
    """
    if not INDIC_NLP_AVAILABLE:
        # Fallback to basic cleaning if library not installed
        return text.strip()
    
    # Factory instantiation for Kannada
    factory = IndicNormalizerFactory()
    normalizer = factory.get_normalizer("kn")
    return normalizer.normalize(text)

def tokenize_kannada_text(text: str) -> list:
    """
    Tokenizes Kannada text into individual word/punctuation tokens.
    """
    if not INDIC_NLP_AVAILABLE:
        return text.split()
        
    normalized_text = normalize_kannada_text(text)
    return indic_tokenize.trivial_tokenize(normalized_text, lang='kn')

if __name__ == "__main__":
    # Quick sanity check/test
    sample_text = "ರೋಗಿಗೆ ಮಧುಮೇಹ ಟೈಪ್ 2 ಇರುವುದು ಕಂಡುಬಂದಿದೆ."
    print("Original Text:", sample_text)
    print("Tokens:", tokenize_kannada_text(sample_text))
