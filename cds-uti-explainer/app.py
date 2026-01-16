import json
import streamlit as st
from dotenv import load_dotenv

from src.runtime_schema import CDSRequest, PatientContext
from src.runtime_guardrails import check_missing_critical, check_escalation
from src.runtime_retrieve import load_store, retrieve_evidence
from src.runtime_generate import generate_answer

load_dotenv()

st.set_page_config(page_title="CDS Explainer — UTI (NG109)", layout="wide")
st.title("🩺 CDS Explainer — Lower UTI (Cystitis) | RAG w/ NICE NG109")

@st.cache_resource
def init_store():
    return load_store()

store = init_store()

# Sidebar: patient input
st.sidebar.header("Patient Context")
age = st.sidebar.number_input("Age", min_value=0, max_value=120, value=30)
sex = st.sidebar.selectbox("Sex", ["female", "male", "other"])
pregnant = st.sidebar.selectbox("Pregnant?", ["unknown", "no", "yes"])
pen_allergy = st.sidebar.selectbox("Penicillin allergy?", ["unknown", "no", "yes"])
egfr = st.sidebar.text_input("eGFR (leave blank if unknown)", value="")

symptoms = st.sidebar.multiselect(
    "Symptoms",
    ["dysuria", "frequency", "urgency", "suprapubic_pain", "vaginal_discharge"],
    default=["dysuria", "frequency"]
)

red_flags = st.sidebar.multiselect(
    "Red flags",
    ["fever", "flank_pain", "rigors", "sepsis_signs", "pregnancy_complication"],
    default=[]
)

question = st.text_area(
    "Clinician question",
    value="Does this presentation fit uncomplicated lower UTI, and what is the recommended antibiotic choice per NG109? Explain with citations."
)

def tri_state(v: str):
    if v == "yes": return True
    if v == "no": return False
    return None

patient = PatientContext(
    age=age,
    sex=sex,
    pregnant=tri_state(pregnant),
    penicillin_allergy=tri_state(pen_allergy),
    egfr=(float(egfr) if egfr.strip() else None),
    symptoms=symptoms,
    red_flags=red_flags,
)

req = CDSRequest(question=question, patient=patient)

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Input")
    st.json(req.model_dump())

with col2:
    st.subheader("Result")
    run = st.button("Run CDS Explainer")

if run:
    # Deterministic guardrails first
    escalate, esc_msg = check_escalation(patient)
    missing = check_missing_critical(patient)

    # Retrieval query (include patient constraints)
    retrieval_query = (
        f"lower UTI cystitis antimicrobial prescribing NG109 "
        f"age {patient.age} sex {patient.sex} "
        f"pregnant {patient.pregnant} penicillin_allergy {patient.penicillin_allergy} "
        f"symptoms {', '.join(patient.symptoms)} "
        f"red_flags {', '.join(patient.red_flags)}"
    )

    evidence_docs = retrieve_evidence(store, retrieval_query, k=6)

    st.markdown("### Retrieved evidence")
    for d in evidence_docs:
        m = d.metadata or {}
        st.markdown(f"**{m.get('doc_id')} / {m.get('section')} / chunk {m.get('chunk_id')}**")
        st.caption(m.get("url"))
        st.code(d.page_content[:1200])

    if escalate:
        st.error(esc_msg)
        st.info("This tool will not suggest outpatient antibiotic selection when red flags are present.")
        st.stop()

    # If missing critical inputs, still allow an explanation but require model to ask for info
    # (We pass missing fields into the prompt implicitly by patient dict.)
    raw = generate_answer(req.model_dump(), evidence_docs)["raw"]

    try:
        parsed = json.loads(raw)
    except Exception:
        st.warning("Model did not return valid JSON. Showing raw output:")
        st.code(raw)
        st.stop()

    # Show outputs
    st.success("Generated CDS explanation")
    st.json(parsed)

    # Extra safety display
    if missing:
        st.warning(f"Missing critical info: {', '.join(missing)}")
        st.info("No dosing should be provided without these fields.")
