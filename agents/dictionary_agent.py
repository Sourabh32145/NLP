import csv
import os
import sys

class DictionaryAgent:
    def __init__(self, dictionary_path=None):
        if dictionary_path is None:
            # Fallback path finding
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.dictionary_path = os.path.join(base_dir, "data", "dictionary", "medical_terms_en_kn.csv")
        else:
            self.dictionary_path = dictionary_path
            
        self.dictionary = {}
        self.load_dictionary()

    def load_dictionary(self):
        """Loads terms from CSV file."""
        if not os.path.exists(self.dictionary_path):
            print(f"[Warning] Dictionary path {self.dictionary_path} not found. Operating in empty mode.")
            return
            
        try:
            with open(self.dictionary_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    eng = row["english_term"].strip().lower()
                    self.dictionary[eng] = {
                        "kannada": row["kannada_term"].strip(),
                        "category": row["category"].strip(),
                        "icd_code": row.get("icd_code", "").strip()
                    }
        except Exception as e:
            print(f"[Error] Failed to load dictionary: {e}")

    def run(self, state: dict) -> dict:
        """
        Scans extracted entities and maps them to Kannada using the dictionary.
        """
        entities = state.get("entities", {})
        mapped = {}
        
        # Search dictionary for matches
        for entity_type, entity_list in entities.items():
            for entity in entity_list:
                cleaned_entity = entity.strip().lower()
                if cleaned_entity in self.dictionary:
                    mapped[entity] = self.dictionary[cleaned_entity]
                else:
                    # Provide empty schema or None for validator/translation to fill
                    mapped[entity] = {
                        "kannada": None, 
                        "category": entity_type,
                        "icd_code": ""
                    }
                    
        state["mapped_terms"] = mapped
        print(f"[DictionaryAgent] Mapped {len([m for m in mapped.values() if m['kannada']])} terms out of {len(mapped)}")
        return state

if __name__ == "__main__":
    agent = DictionaryAgent()
    test_state = {"entities": {"Disease": ["Hypertension", "Type 2 Diabetes", "Unknown Syndrome"]}}
    print(agent.run(test_state))
