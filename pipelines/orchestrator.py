import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.ingestion_agent import IngestionAgent
from agents.ner_agent import NERAgent
from agents.dictionary_agent import DictionaryAgent
from agents.summary_agent import SummaryAgent
from agents.translation_agent import TranslationAgent
from agents.validator_agent import ValidatorAgent

class PipelineOrchestrator:
    def __init__(self):
        self.ingestion = IngestionAgent()
        self.ner = NERAgent()
        self.dictionary = DictionaryAgent()
        self.summary = SummaryAgent()
        self.translation = TranslationAgent()
        self.validator = ValidatorAgent()

    def run(self, raw_input: str) -> dict:
        """Runs the agents sequentially."""
        state = {
            "raw_input": raw_input,
            "language": "",
            "normalized_text": "",
            "entities": {},
            "mapped_terms": {},
            "english_summary": "",
            "kannada_summary": "",
            "validation_passed": False,
            "validation_errors": []
        }
        
        # Sequentially call agent nodes
        state = self.ingestion.run(state)
        state = self.ner.run(state)
        state = self.dictionary.run(state)
        
        # Iterate or loop back once if validation fails
        max_retries = 2
        for attempt in range(max_retries):
            state = self.summary.run(state)
            state = self.translation.run(state)
            state = self.validator.run(state)
            
            if state["validation_passed"]:
                break
            else:
                print(f"[Orchestrator] Validation failed on attempt {attempt+1}. Retrying...")
                
        return state

if __name__ == "__main__":
    orch = PipelineOrchestrator()
    sample_notes = "The patient has Diabetes and Hypertension. Prescribed Aspirin and Paracetamol."
    result = orch.run(sample_notes)
    print("\n--- Pipeline Execution Output ---")
    print("English:\n", result["english_summary"])
    print("\nKannada:\n", result["kannada_summary"])
