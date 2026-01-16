from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

SYSTEM = """You are a Clinical Decision Support (CDS) Explainer.
You MUST follow these rules:
- Only use the provided EVIDENCE snippets for medical claims.
- If evidence is insufficient or missing, say you cannot conclude and ask for missing info.
- Always include citations for any recommendation (cite chunk_id + doc_id + section).
- Do NOT provide medication dosing if missing eGFR or pregnancy status.
- If red flags exist, recommend escalation rather than outpatient antibiotic selection.

Return STRICT JSON with keys:
{
  "recommendation": string,
  "rationale": string,
  "safety_checks": [string],
  "missing_info": [string],
  "citations": [{"chunk_id": string, "doc_id": string, "section": string, "url": string}]
}
"""

def evidence_pack(docs) -> str:
    parts = []
    for d in docs:
        m = d.metadata or {}
        parts.append(
            f"[chunk_id={m.get('chunk_id')} doc_id={m.get('doc_id')} section={m.get('section')} url={m.get('url')}] "
            f"{d.page_content}"
        )
    return "\n\n".join(parts)

def generate_answer(request_dict: Dict[str, Any], evidence_docs) -> Dict[str, Any]:
    model = ChatOpenAI(model="gpt-5-mini", temperature=0)  # :contentReference[oaicite:10]{index=10}

    patient = request_dict["patient"]
    question = request_dict["question"]

    user = f"""
PATIENT_CONTEXT (structured):
{patient}

CLINICIAN_QUESTION:
{question}

EVIDENCE:
{evidence_pack(evidence_docs)}

Now produce the JSON response.
""".strip()

    resp = model.invoke([SystemMessage(content=SYSTEM), HumanMessage(content=user)])
    # The model returns a string; parse JSON safely in caller.
    return {"raw": resp.content}
