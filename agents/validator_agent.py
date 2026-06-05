import sys
import os

class ValidatorAgent:
    def __init__(self):
        pass

    def run(self, state: dict) -> dict:
        """
        Validates English ↔ Kannada terminology alignment and ensures no empty output.
        """
        english_summary = state.get("english_summary", "")
        kannada_summary = state.get("kannada_summary", "")
        mapped_terms = state.get("mapped_terms", {})
        
        passed = True
        validation_errors = []
        
        # Check 1: Empty checks
        if not english_summary or not kannada_summary:
            passed = False
            validation_errors.append("Empty summary content generated.")
            
        # Check 2: Verify terms mapped in dictionary are present in the Kannada summary
        for eng, info in mapped_terms.items():
            kn = info.get("kannada")
            if kn and kn not in kannada_summary:
                passed = False
                validation_errors.append(f"Mapped term '{kn}' (from '{eng}') is missing from Kannada summary.")
                
        state["validation_passed"] = passed
        state["validation_errors"] = validation_errors
        
        print(f"[ValidatorAgent] Passed: {passed}, Errors: {validation_errors}")
        return state

if __name__ == "__main__":
    agent = ValidatorAgent()
    test_state = {
        "english_summary": "Diagnoses: Diabetes",
        "kannada_summary": "ರೋಗನಿರ್ಣಯ: ರೋಗಿ",
        "mapped_terms": {"Diabetes": {"kannada": "ಮಧುಮೇಹ"}}
    }
    print(agent.run(test_state))
