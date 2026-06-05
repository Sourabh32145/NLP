import streamlit as st
import sys
import os

# Fix Unicode printing issues on Windows cmd/powershell
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Include parent dir in pythonpath
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipelines.orchestrator import PipelineOrchestrator

st.set_page_config(
    page_title="Clinical Translation",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enterprise Custom Styling (Medical Green Theme - Dark Mode Compatible)
st.markdown("""
<style>
    /* Global Typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Top Navigation Bar / Header */
    .header-container {
        padding: 1.5rem 0 2rem 0;
        border-bottom: 1px solid #10b981;
        margin-bottom: 2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .header-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #10b981; /* Emerald 500 */
        letter-spacing: -0.025em;
        margin: 0;
    }
    .header-badge {
        font-size: 0.75rem;
        font-weight: 600;
        background-color: rgba(16, 185, 129, 0.1);
        color: #34d399; /* Emerald 400 */
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        border: 1px solid #10b981;
    }

    /* Section Headers */
    .section-header {
        font-size: 1rem;
        font-weight: 600;
        color: #34d399; /* Emerald 400 */
        margin-bottom: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Text Area Styling */
    .stTextArea textarea {
        border-radius: 8px;
        border: 1px solid #374151; /* Gray 700 */
        padding: 1rem;
        font-size: 0.95rem;
        line-height: 1.5;
        transition: border-color 0.15s ease-in-out;
    }
    .stTextArea textarea:focus {
        border-color: #10b981 !important; /* Emerald 500 */
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.2) !important;
    }

    /* Primary Button */
    .stButton > button {
        background-color: #059669; /* Emerald 600 */
        color: white;
        border-radius: 6px;
        padding: 0.6rem 1.2rem;
        font-weight: 500;
        font-size: 0.95rem;
        border: none;
        box-shadow: 0 4px 6px -1px rgba(16, 185, 129, 0.2), 0 2px 4px -1px rgba(16, 185, 129, 0.1);
        transition: all 0.2s;
        width: 100%;
        margin-top: 1rem;
    }
    .stButton > button:hover {
        background-color: #047857; /* Emerald 700 */
        box-shadow: 0 10px 15px -3px rgba(16, 185, 129, 0.3), 0 4px 6px -2px rgba(16, 185, 129, 0.15);
        color: white;
    }

    /* Output Code Blocks */
    .stCodeBlock {
        border-radius: 8px;
        border: 1px solid #374151;
    }
    .stCodeBlock code {
        font-family: 'Inter', sans-serif !important;
        font-size: 0.95rem !important;
        line-height: 1.6 !important;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        border-bottom: 1px solid #374151;
    }
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 0;
        font-weight: 500;
        font-size: 0.95rem;
    }
    .stTabs [aria-selected="true"] {
        color: #10b981 !important; /* Emerald 500 */
        border-bottom: 2px solid #10b981 !important;
    }

    /* Subtle UI Tweaks */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Layout spacing */
    .block-container {
        padding-top: 2rem;
        max-width: 1200px;
    }
</style>
""", unsafe_allow_html=True)

# Application Header
st.markdown("""
<div class="header-container">
    <div class="header-title">Clinical Translation and Summarization System</div>
    <div class="header-badge">English ↔ Kannada Translation Engine</div>
</div>
""", unsafe_allow_html=True)

col_in, padding, col_out = st.columns([1, 0.05, 1])

with col_in:
    st.markdown('<div class="section-header">Source Clinical Notes</div>', unsafe_allow_html=True)
    
    sample_options = {
        "Custom Input": "",
        "Neurology Assessment (Headaches)": "The patient is a 29-year-old female who presented to the neurology clinic with complaints of recurrent headaches over the past six months. She described the headaches as severe, throbbing pain predominantly affecting the left side of her head, often accompanied by nausea, sensitivity to light, and sensitivity to sound. The patient reported that the headaches are frequently triggered by stress, inadequate sleep, and prolonged screen exposure. She denied any recent head trauma, fever, weakness, visual loss, or other neurological symptoms.\n\nOn examination, the patient was alert, oriented, and in no acute distress. Vital signs were within normal limits. Neurological examination revealed no focal deficits. Cranial nerves were intact, motor and sensory functions were normal."
    }
    sample_key = st.selectbox("Select a Template", list(sample_options.keys()), label_visibility="collapsed")
    
    input_text = st.text_area(
        "Clinical Input",
        value=sample_options[sample_key],
        height=350,
        placeholder="Enter unstructured clinical notes or EHR text...",
        label_visibility="collapsed"
    )
    
    generate_btn = st.button("Generate Structured Bilingual Summary")

if generate_btn:
    if not input_text.strip():
        st.error("Please provide clinical text to process.")
    else:
        with st.spinner("Processing clinical narrative through translation pipeline..."):
            orch = PipelineOrchestrator()
            result = orch.run(input_text)
            
            with col_out:
                st.markdown('<div class="section-header">Processed Output</div>', unsafe_allow_html=True)
                tab1, tab2, tab3 = st.tabs(["Kannada Summary", "English Summary", "Diagnostics"])
                
                with tab1:
                    st.code(result["kannada_summary"], language="text")
                    
                with tab2:
                    st.code(result["english_summary"], language="text")
                    
                with tab3:
                    st.markdown("**Extracted Clinical Entities**")
                    st.json(result["entities"])
                    
                    if result["validation_errors"]:
                        for err in result["validation_errors"]:
                            st.error(f"Validation Error: {err}")
                    else:
                        st.info("System Validation Passed: Terminology aligned.")
