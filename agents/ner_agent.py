import re

# ─────────────────────────────────────────────────────────────────────────────
# Words/phrases that signal NEGATION — skip entities that follow these
# ─────────────────────────────────────────────────────────────────────────────
NEGATION_TRIGGERS = {
    "denied", "denies", "deny", "no", "without", "absence of",
    "negative for", "not", "never", "none", "unremarkable for",
    "no evidence of", "ruled out", "absent",
}

# ─────────────────────────────────────────────────────────────────────────────
# Comprehensive clinical keyword dictionary
# Structure: keyword (lower) → category
# ─────────────────────────────────────────────────────────────────────────────
MEDICAL_KEYWORDS: dict[str, str] = {

    # ── DISEASES / DIAGNOSES ─────────────────────────────────────────────────
    "diabetes": "Disease",
    "hypertension": "Disease",
    "asthma": "Disease",
    "pneumonia": "Disease",
    "cancer": "Disease",
    "carcinoma": "Disease",
    "tumor": "Disease",
    "arthritis": "Disease",
    "osteoarthritis": "Disease",
    "rheumatoid arthritis": "Disease",
    "anemia": "Disease",
    "stroke": "Disease",
    "obesity": "Disease",
    "hypothyroidism": "Disease",
    "hyperthyroidism": "Disease",
    "thyroid": "Disease",
    "infection": "Disease",
    "fracture": "Disease",
    "allergy": "Disease",
    "insomnia": "Disease",
    "migraine": "Disease",
    "epilepsy": "Disease",
    "seizure": "Disease",
    "depression": "Disease",
    "anxiety": "Disease",
    "copd": "Disease",
    "bronchitis": "Disease",
    "appendicitis": "Disease",
    "gastritis": "Disease",
    "colitis": "Disease",
    "hepatitis": "Disease",
    "cirrhosis": "Disease",
    "pancreatitis": "Disease",
    "nephritis": "Disease",
    "uti": "Disease",
    "myocardial infarction": "Disease",
    "heart failure": "Disease",
    "atrial fibrillation": "Disease",
    "deep vein thrombosis": "Disease",
    "pulmonary embolism": "Disease",
    "osteoporosis": "Disease",
    "gout": "Disease",
    "lupus": "Disease",
    "scoliosis": "Disease",
    "herniated disc": "Disease",
    "parkinson": "Disease",
    "alzheimer": "Disease",
    "multiple sclerosis": "Disease",
    "meningitis": "Disease",
    "encephalitis": "Disease",
    "glaucoma": "Disease",
    "cataracts": "Disease",
    "sinusitis": "Disease",
    "otitis": "Disease",
    "tonsillitis": "Disease",
    "pharyngitis": "Disease",
    "conjunctivitis": "Disease",
    "eczema": "Disease",
    "psoriasis": "Disease",
    "erythema": "Disease",
    "deformity": "Disease",
    "sprain": "Disease",
    "tendinitis": "Disease",
    "bursitis": "Disease",
    "disc herniation": "Disease",

    # ── SYMPTOMS ─────────────────────────────────────────────────────────────
    "pain": "Symptom",
    "ache": "Symptom",
    "fever": "Symptom",
    "fatigue": "Symptom",
    "headache": "Symptom",
    "headaches": "Symptom",
    "dizziness": "Symptom",
    "cough": "Symptom",
    "nausea": "Symptom",
    "vomiting": "Symptom",
    "diarrhea": "Symptom",
    "dyspnea": "Symptom",
    "shortness of breath": "Symptom",
    "palpitations": "Symptom",
    "swelling": "Symptom",
    "stiffness": "Symptom",
    "tenderness": "Symptom",
    "crepitus": "Symptom",
    "discomfort": "Symptom",
    "weakness": "Symptom",
    "numbness": "Symptom",
    "tingling": "Symptom",
    "bruising": "Symptom",
    "rash": "Symptom",
    "itching": "Symptom",
    "bleeding": "Symptom",
    "discharge": "Symptom",
    "throbbing": "Symptom",
    "sensitivity": "Symptom",
    "photophobia": "Symptom",
    "phonophobia": "Symptom",
    "blurred vision": "Symptom",
    "visual loss": "Symptom",
    "double vision": "Symptom",
    "hearing loss": "Symptom",
    "tinnitus": "Symptom",
    "vertigo": "Symptom",
    "syncope": "Symptom",
    "tremor": "Symptom",
    "paralysis": "Symptom",
    "confusion": "Symptom",
    "memory loss": "Symptom",
    "insomnia": "Symptom",
    "chest pain": "Symptom",
    "back pain": "Symptom",
    "joint pain": "Symptom",
    "muscle pain": "Symptom",
    "neck pain": "Symptom",
    "abdominal pain": "Symptom",
    "morning stiffness": "Symptom",
    "antalgic gait": "Symptom",
    "gait abnormality": "Symptom",
    "edema": "Symptom",
    "hypertonia": "Symptom",
    "hypotonia": "Symptom",
    "papilledema": "Symptom",
    "spasm": "Symptom",
    "rigidity": "Symptom",
    "contracture": "Symptom",
    "atrophy": "Symptom",
    "deficit": "Symptom",
    "loss of function": "Symptom",
    "decreased range of motion": "Symptom",

    # ── MEDICATIONS ───────────────────────────────────────────────────────────
    "aspirin": "Medication",
    "paracetamol": "Medication",
    "acetaminophen": "Medication",
    "ibuprofen": "Medication",
    "naproxen": "Medication",
    "insulin": "Medication",
    "metformin": "Medication",
    "antibiotic": "Medication",
    "antibiotics": "Medication",
    "amoxicillin": "Medication",
    "vaccine": "Medication",
    "inhaler": "Medication",
    "salbutamol": "Medication",
    "atorvastatin": "Medication",
    "lisinopril": "Medication",
    "omeprazole": "Medication",
    "prednisone": "Medication",
    "hydroxychloroquine": "Medication",
    "sumatriptan": "Medication",
    "topiramate": "Medication",
    "valproate": "Medication",
    "gabapentin": "Medication",
    "morphine": "Medication",
    "tramadol": "Medication",
    "codeine": "Medication",
    "diclofenac": "Medication",
    "methotrexate": "Medication",
    "warfarin": "Medication",
    "heparin": "Medication",
    "clopidogrel": "Medication",

    # ── BODY PARTS ────────────────────────────────────────────────────────────
    "head": "Body Part",
    "skull": "Body Part",
    "brain": "Body Part",
    "cranial": "Body Part",
    "cranial nerves": "Body Part",
    "face": "Body Part",
    "eye": "Body Part",
    "eyes": "Body Part",
    "fundoscopic": "Body Part",
    "ear": "Body Part",
    "ears": "Body Part",
    "nose": "Body Part",
    "throat": "Body Part",
    "neck": "Body Part",
    "spine": "Body Part",
    "cervical spine": "Body Part",
    "lumbar spine": "Body Part",
    "thoracic spine": "Body Part",
    "shoulder": "Body Part",
    "elbow": "Body Part",
    "wrist": "Body Part",
    "hand": "Body Part",
    "finger": "Body Part",
    "chest": "Body Part",
    "lung": "Body Part",
    "lungs": "Body Part",
    "heart": "Body Part",
    "abdomen": "Body Part",
    "liver": "Body Part",
    "kidney": "Body Part",
    "bladder": "Body Part",
    "pelvis": "Body Part",
    "hip": "Body Part",
    "thigh": "Body Part",
    "knee": "Body Part",
    "knees": "Body Part",
    "tibia": "Body Part",
    "ankle": "Body Part",
    "foot": "Body Part",
    "lower extremity": "Body Part",
    "upper extremity": "Body Part",
    "extremity": "Body Part",
    "joint": "Body Part",
    "medial joint": "Body Part",
    "ligament": "Body Part",
    "tendon": "Body Part",
    "muscle": "Body Part",
    "nerve": "Body Part",
    "skin": "Body Part",
}


def _build_negation_windows(text: str) -> list[tuple[int, int]]:
    """
    Returns list of (start, end) char spans that are 'negated' zones.
    A negated zone starts at a negation trigger and spans ~60 chars forward.
    """
    negated_zones = []
    text_lower = text.lower()
    for trigger in NEGATION_TRIGGERS:
        idx = 0
        while True:
            pos = text_lower.find(trigger, idx)
            if pos == -1:
                break
            negated_zones.append((pos, pos + len(trigger) + 70))
            idx = pos + 1
    return negated_zones


def _is_negated(match_start: int, negated_zones: list[tuple[int, int]]) -> bool:
    for start, end in negated_zones:
        if start <= match_start <= end:
            return True
    return False


class NERAgent:
    def __init__(self):
        self.keywords = MEDICAL_KEYWORDS
        # Sort longest phrases first to ensure multi-word matches take priority
        self.sorted_keywords = sorted(
            self.keywords.items(), key=lambda x: len(x[0]), reverse=True
        )

    def run(self, state: dict) -> dict:
        text = state.get("normalized_text", "")
        text_lower = text.lower()
        entities: dict[str, list] = {
            "Disease": [], "Symptom": [], "Medication": [], "Body Part": []
        }

        # Build negation windows once
        negated_zones = _build_negation_windows(text)

        for kw, category in self.sorted_keywords:
            idx = 0
            while True:
                pos = text_lower.find(kw, idx)
                if pos == -1:
                    break
                # Skip if inside a negation zone
                if not _is_negated(pos, negated_zones):
                    display = kw.title()
                    if display not in entities[category]:
                        entities[category].append(display)
                idx = pos + len(kw)

        state["entities"] = entities
        print(f"[NERAgent] Entities: { {k: v for k, v in entities.items() if v} }")
        return state
