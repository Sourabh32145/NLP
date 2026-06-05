import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.kannada_utils import normalize_kannada_text

class IngestionAgent:
    def __init__(self):
        pass

    def run(self, state: dict) -> dict:
        """
        Receives raw clinical notes, normalizes text, and identifies the dominant language.
        """
        raw_text = state.get("raw_input", "")
        
        # Determine language (Basic script detection)
        # Kannada unicode block range: 0C80 - 0CFF
        is_kannada = any('\u0c80' <= char <= '\u0cff' for char in raw_text)
        detected_lang = "kn" if is_kannada else "en"
        
        # Preprocess / normalize text
        if detected_lang == "kn":
            normalized_text = normalize_kannada_text(raw_text)
        else:
            normalized_text = raw_text.strip()
            
        state["language"] = detected_lang
        state["normalized_text"] = normalized_text
        
        print(f"[IngestionAgent] Detected Language: {detected_lang}")
        return state

if __name__ == "__main__":
    agent = IngestionAgent()
    test_state = {"raw_input": "ರೋಗಿಗೆ ಮಧುಮೇಹ ಟೈಪ್ 2 ಇರುವುದು ಕಂಡುಬಂದಿದೆ."}
    print(agent.run(test_state))
