from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime
from pathlib import Path

app = Flask(__name__)

LEADS_FILE = Path("leads.json")

QUESTIONS = [
    (
        "role_clarity",
        "How clearly can you explain why you are the right person for the role?",
        [
            "I struggle to explain it clearly",
            "I can explain my experience, but not my differentiation",
            "I can connect my experience to the role",
            "I can clearly articulate the business value I bring"
        ]
    ),
    (
        "leadership_story",
        "How strong is your leadership story when an interviewer asks, “Tell me about yourself”?",
        [
            "Mostly a chronological career summary",
            "Reasonably clear, but generic",
            "Clear and relevant to the role",
            "Concise, differentiated and strategically positioned"
        ]
    ),
    (
        "business_impact",
        "How confidently can you demonstrate measurable business impact?",
        [
            "I mainly describe responsibilities",
            "I have examples but struggle to frame the impact",
            "I can explain outcomes with examples",
            "I consistently connect decisions to business outcomes"
        ]
    ),
    (
        "executive_presence",
        "How would you rate your executive presence in a high-stakes interview?",
        [
            "I become noticeably nervous",
            "Generally confident, but inconsistent",
            "Calm and confident in most situations",
            "Calm, concise and authoritative under pressure"
        ]
    ),
    (
        "difficult_questions",
        "How prepared are you for difficult questions about failure, conflict, gaps or weaknesses?",
        [
            "I tend to improvise",
            "I have thought about a few examples",
            "I have prepared strong examples",
            "I can handle difficult questions without becoming defensive"
        ]
    ),
    (
        "strategic_thinking",
        "When asked about the future, how well can you discuss strategy rather than only execution?",
        [
            "I focus mostly on execution",
            "I can discuss strategy with some prompting",
            "I can connect strategy to execution",
            "I naturally think in terms of business, market and enterprise impact"
        ]
    ),
    (
        "role_transition",
        "If this is a bigger role, how clearly can you explain your readiness for the next level?",
        [
            "I mainly rely on past performance",
            "I can explain some evidence",
            "I can show relevant readiness",
            "I can clearly demonstrate the identity and scope of the next-level leader"
        ]
    ),
    (
        "closing",
        "How prepared are you for the final part of the interview — your questions, positioning and closing?",
        [
            "I usually just wait for the interviewer to finish",
            "I ask a few standard questions",
            "I prepare relevant questions",
            "I use the close to reinforce strategic fit and value"
        ]
    )
]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/assessment")
def assessment():
    return render_template(
        "assessment.html",
        questions=QUESTIONS
    )


@app.post("/api/submit")
def submit():

    data = request.get_json(silent=True) or {}

    answers = data.get("answers", {})

    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    phone = (data.get("phone") or "").strip()
    target_role = (data.get("target_role") or "").strip()

    scores = []

    for key, _, _ in QUESTIONS:

        try:
            value = int(answers.get(key, 0))
        except (TypeError, ValueError):
            value = 0

        value = max(1, min(4, value))
        scores.append(value)

    total = sum(scores)

    max_score = len(QUESTIONS) * 4

    percentage = round(
        total / max_score * 100
    )

    if percentage >= 80:

        level = "Strong Interview Readiness"

        message = (
            "Your foundation is strong. "
            "The biggest opportunity is sharpening differentiation, "
            "executive-level storytelling and the way you communicate "
            "strategic value."
        )

    elif percentage >= 60:

        level = "Developing Interview Readiness"

        message = (
            "You have a solid base, but some areas could weaken "
            "your positioning in a competitive interview. "
            "Focused preparation can make your answers more deliberate "
            "and differentiated."
        )

    else:

        level = "Preparation Required"

        message = (
            "Your experience may be stronger than the way it currently "
            "comes across in an interview. The priority is to build "
            "a clearer leadership narrative, stronger evidence and "
            "greater confidence under pressure."
        )

    lead = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "name": name,
        "email": email,
        "phone": phone,
        "target_role": target_role,
        "score": percentage,
        "level": level,
        "answers": answers
    }

    existing = []

    if LEADS_FILE.exists():

        try:
            existing = json.loads(
                LEADS_FILE.read_text(
                    encoding="utf-8"
                )
            )

        except Exception:
            existing = []

    existing.append(lead)

    LEADS_FILE.write_text(
        json.dumps(
            existing,
            indent=2
        ),
        encoding="utf-8"
    )

    return jsonify({
        "score": percentage,
        "level": level,
        "message": message,
        "name": name
    })


@app.route("/health")
def health():

    return {
        "status": "ok"
    }


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5055,
        debug=True
    )
