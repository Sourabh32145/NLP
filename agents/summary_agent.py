import re

# Section headers to look for in clinical notes
SECTION_PATTERNS = {
    "chief_complaint": [
        r"chief complaint[s]?[:]\s*(.*?)(?=\n[A-Z]|\Z)",
        r"chief complaint[s]?[\n](.*?)(?=\n[A-Z]|\Z)",
        r"complaints?[:]\s*(.*?)(?=\n[A-Z]|\Z)",
    ],
    "hpi": [
        r"history of present illness.*?[:]\s*(.*?)(?=\n[A-Z]|\Z)",
        r"HPI[:]\s*(.*?)(?=\n[A-Z]|\Z)",
    ],
    "physical_exam": [
        r"physical examination.*?[:]\s*(.*?)(?=\n[A-Z]|\Z)",
        r"on examination.*?[:]\s*(.*?)(?=\n[A-Z]|\Z)",
        r"on physical examination[,.]?\s*(.*?)(?=\n[A-Z]|\Z)",
    ],
    "ros": [
        r"review of systems.*?[:]\s*(.*?)(?=\n[A-Z]|\Z)",
        r"ROS[:]\s*(.*?)(?=\n[A-Z]|\Z)",
    ],
    "assessment": [
        r"assessment.*?[:]\s*(.*?)(?=\n[A-Z]|\Z)",
        r"impression.*?[:]\s*(.*?)(?=\n[A-Z]|\Z)",
    ],
    "plan": [
        r"plan.*?[:]\s*(.*?)(?=\n[A-Z]|\Z)",
        r"management.*?[:]\s*(.*?)(?=\n[A-Z]|\Z)",
    ],
}


def extract_section(text: str, patterns: list) -> str:
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(1).strip()[:500]  # cap at 500 chars
    return ""


class SummaryAgent:
    def __init__(self):
        pass

    def run(self, state: dict) -> dict:
        entities = state.get("entities", {})
        text = state.get("normalized_text", "")

        diseases   = ", ".join(entities.get("Disease", [])) or "None reported"
        symptoms   = ", ".join(entities.get("Symptom", [])) or "None reported"
        meds       = ", ".join(entities.get("Medication", [])) or "None reported"
        body_parts = ", ".join(entities.get("Body Part", [])) or "None reported"

        # ── Try to extract structured sections from clinical note ──
        chief_complaint  = extract_section(text, SECTION_PATTERNS["chief_complaint"])
        hpi              = extract_section(text, SECTION_PATTERNS["hpi"])
        physical_exam    = extract_section(text, SECTION_PATTERNS["physical_exam"])
        ros              = extract_section(text, SECTION_PATTERNS["ros"])
        assessment       = extract_section(text, SECTION_PATTERNS["assessment"])
        plan_section     = extract_section(text, SECTION_PATTERNS["plan"])

        # ── If no structured sections found, use the full text as clinical course ──
        if not chief_complaint and not hpi and not physical_exam:
            # Unstructured note — split at paragraph breaks
            paragraphs = [p.strip() for p in text.strip().split("\n\n") if p.strip()]
            hpi              = paragraphs[0] if len(paragraphs) > 0 else text[:500]
            physical_exam    = paragraphs[1] if len(paragraphs) > 1 else ""

        # ── Build the discharge summary ──
        lines = [
            "CLINICAL DISCHARGE SUMMARY",
            "==========================",
            f"Primary Diagnoses / Diseases: {diseases}",
            f"Presenting Symptoms: {symptoms}",
            f"Prescribed Medications: {meds}",
            f"Affected Body Parts: {body_parts}",
            "",
            "Clinical Course & Recommendations:",
        ]

        if chief_complaint:
            lines.append(f"- Chief Complaint: {chief_complaint}")
        if hpi:
            lines.append(f"- History of Present Illness: {hpi}")
        if physical_exam:
            lines.append(f"- Physical Examination Findings: {physical_exam}")
        if ros:
            lines.append(f"- Review of Systems: {ros}")
        if assessment:
            lines.append(f"- Assessment: {assessment}")
        if plan_section:
            lines.append(f"- Plan: {plan_section}")

        lines += [
            "- Monitor vitals regularly.",
            "- Follow prescribed medication schedule.",
        ]

        # Add ortho-specific recommendation if knee/joint involved
        body_parts_lower = " ".join(entities.get("Body Part", [])).lower()
        if any(b in body_parts_lower for b in ["knee", "hip", "shoulder", "spine", "ankle"]):
            lines.append("- Consult orthopedic specialist for further evaluation.")

        state["english_summary"] = "\n".join(lines)
        print("[SummaryAgent] Drafted structured summary.")
        return state
