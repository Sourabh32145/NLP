import sys
import os
import re
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.translation_utils import Translator

class TranslationAgent:
    def __init__(self):
        self.translator = Translator()

    def run(self, state: dict) -> dict:
        english_summary = state.get("english_summary", "")
        mapped_terms    = state.get("mapped_terms", {})

        translated_lines = []
        for line in english_summary.split("\n"):
            if not line.strip():
                translated_lines.append("")
                continue

            # Lines with colon: translate heading and value separately
            if ":" in line and not line.strip().startswith("-"):
                parts = line.split(":", 1)
                heading = parts[0].strip()
                value   = parts[1].strip()
                t_heading = self.translator.translate_english_to_kannada(heading)
                # Value may be multi-sentence clinical text
                t_value   = self.translator.translate_block(value) if value else ""
                translated_line = f"{t_heading}: {t_value}" if t_value else f"{t_heading}:"
            else:
                # Bullet points and plain lines
                translated_line = self.translator.translate_english_to_kannada(line)

            translated_lines.append(translated_line)

        state["kannada_summary"] = "\n".join(translated_lines)
        print("[TranslationAgent] Generated Kannada Summary.")
        return state
