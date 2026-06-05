# Domain Adaptation for Healthcare Text using NLP (Bilingual English ↔ Kannada)

MedScribe AI is a multi-agent domain-adapted NLP system built to parse unstructured English or Kannada Clinical/EHR notes, extract key medical entities (using ClinicalBERT architectures), cross-reference with a Kannada Medical Dictionary, and construct side-by-side bilingual discharge summaries.

## 🚀 Quick Start & Running Streamlit UI

1. Clone or navigate to the directory:
   ```bash
   cd nlp-healthcare
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit application:
   ```bash
   streamlit run ui/app.py
   ```

## 🏗️ Multi-Agent Architecture
The pipeline coordinates 6 specialized agents sequentially using a shared DAG State graph:
- **IngestionAgent**: Normalizes raw input unicode & identifies the text script (English vs Kannada).
- **NERAgent**: Identifies Clinical entities (Diseases, Symptoms, Medications) using BERT/Heuristics.
- **DictionaryAgent**: Matches clinical terms using a custom seed SQLite/CSV medical dictionary.
- **SummaryAgent**: Drafts a structured discharge summary.
- **TranslationAgent**: Translates English segments to Kannada using IndicTrans2 models.
- **ValidatorAgent**: Verifies translation alignment & constraints.
