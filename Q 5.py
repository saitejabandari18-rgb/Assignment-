import json
from openai import OpenAI


client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio"
)

MODEL = "qwen3-0.6b"


def ask_llm(prompt: str, system: str) -> str:

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": system
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


QUIZ = [
    (
        "What does a thermostat do in a smart building?",
        "It measures room temperature and switches heating or "
        "cooling to hold a target temperature."
    ),

    (
        "Why do smart buildings measure CO2 concentration?",
        "High CO2 indicates poor indoor air quality; the ventilation "
        "system uses it to bring in fresh air."
    ),

    (
        "What is the purpose of presence detection in a smart building?",
        "It detects whether people are present so systems such as "
        "lighting and heating can be adjusted according to occupancy."
    ),

    (
        "What is a heat pump used for in a smart building?",
        "A heat pump transfers heat from one place to another and "
        "can provide efficient heating or cooling."
    ),

    (
        "Why are sensors important in smart buildings?",
        "Sensors collect information about things such as temperature, "
        "air quality and occupancy so building systems can respond."
    )
]


def try_parse_json(text):

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def judge_answer(question: str, reference: str, answer: str) -> dict:

    system = (
        "You are a grading judge for a smart building quiz. "
        "Return only a JSON object with exactly two keys: "
        "score and reason. "
        "Score must be an integer from 0 to 10. "
        "Reason must be one sentence. "
        "Different wording from the reference answer is fine. "
        "10 = same meaning as the reference, "
        "7 = mostly correct, "
        "5 = partially correct, "
        "2 = mostly wrong, "
        "0 = wrong or off-topic."
    )

    prompt = f"""
Question:
{question}

Reference answer:
{reference}

Student answer:
{answer}

Give a score from 0 to 10.

Reply with only JSON:
{{"score": 7, "reason": "Mostly correct but missing an important point."}}
"""

    reply = ask_llm(prompt, system)

    return try_parse_json(reply)


def check_verdict(d) -> str:

    if d is None:
        return "The response is not valid JSON."

    if not isinstance(d, dict):
        return "The response must be a JSON object."

    if set(d.keys()) != {"score", "reason"}:
        return "The JSON must contain exactly score and reason."

    score = d["score"]

    if isinstance(score, bool) or not isinstance(score, int):
        return "The score must be an integer."

    if score < 0 or score > 10:
        return "The score must be between 0 and 10."

    reason = d["reason"]

    if not isinstance(reason, str) or not reason.strip():
        return "The reason must be a non-empty string."

    return ""


def judge_with_retry(question, reference, answer, max_attempts=3):

    last_error = ""

    for attempt in range(max_attempts):

        if attempt == 0:
            verdict = judge_answer(
                question,
                reference,
                answer
            )

        else:
            system = (
                "You are a grading judge. "
                "Return only valid JSON with exactly "
                "score and reason."
            )

            prompt = f"""
Question:
{question}

Reference answer:
{reference}

Student answer:
{answer}

Your previous response was invalid.

The validation error was:
{last_error}

Return corrected JSON only.

The score must be an integer from 0 to 10.
The reason must be a non-empty one-sentence string.

Use this scale:
10 = same meaning as reference
7 = mostly correct
5 = partially correct
2 = mostly wrong
0 = wrong or off-topic

Example:
{{"score": 7, "reason": "The main idea is correct but one detail is missing."}}
"""

            reply = ask_llm(prompt, system)
            verdict = try_parse_json(reply)

        last_error = check_verdict(verdict)

        if last_error == "":
            return verdict

    print(
        "ERROR: Could not grade question:",
        question
    )
    print("Reason:", last_error)

    return None


def grade_quiz(answers: list) -> dict:

    scores = []
    total = 0
    max_possible = 0
    ungraded = []

    for i in range(len(QUIZ)):

        question = QUIZ[i][0]
        reference = QUIZ[i][1]
        answer = answers[i]

        verdict = judge_with_retry(
            question,
            reference,
            answer
        )

        if verdict is None:
            ungraded.append(i + 1)
            print(f"Question {i + 1}: UNGRADED")
            continue

        score = verdict["score"]
        reason = verdict["reason"]

        scores.append(score)
        total += score
        max_possible += 10

        print(
            f"Question {i + 1}: "
            f"{score}/10 - {reason}"
        )

    print("Total:", total, "/", max_possible)

    if max_possible > 0:
        percentage = total / max_possible * 100
    else:
        percentage = 0

    print(f"Percentage: {percentage:.1f}%")

    if len(ungraded) > 0:
        print("Ungraded questions:", ungraded)
    else:
        print("Ungraded questions: none")

    return {
        "scores": scores,
        "total": total,
        "max possible": max_possible,
        "ungraded": ungraded
    }


# Demo
if __name__ == "__main__":

    strong_answers = [
        "A thermostat measures the room temperature and controls "
        "heating or cooling to keep it close to the target temperature.",

        "High CO2 usually means the indoor air quality is poor. "
        "The ventilation system can increase the supply of fresh air.",

        "Presence detection identifies whether people are in a room. "
        "The building can then adjust lighting and heating based on occupancy.",

        "A heat pump moves heat from one place to another and can "
        "be used efficiently for heating or cooling.",

        "Sensors collect information such as temperature, air quality "
        "and occupancy so the building systems can react."
    ]

    weak_answers = [
        "It controls the temperature.",

        "It measures the air.",

        "It detects people.",

        "It makes heat.",

        "Sensors collect data."
    ]

    print("========== STRONG STUDENT ==========")

    strong_result = grade_quiz(strong_answers)

    print("Strong result:", strong_result)

    print("\n========== WEAK STUDENT ==========")

    weak_result = grade_quiz(weak_answers)

    print("Weak result:", weak_result)


# ---------------------------------------------------------------
# REAL TRANSCRIPT
#
# After running the program, paste ONE actual prompt and the
# actual raw model response from your LM Studio run here.
#
# Do not use a made-up response.
#
# PROMPT:
# [paste the actual prompt here]
#
# RAW MODEL REPLY:
# [paste the exact raw reply here]
# ---------------------------------------------------------------