import os
import re
from typing import List

try:
    from openai import OpenAI
except Exception:
    OpenAI = None

from .prompts import chatbot_prompt


def build_chat_prompt(question: str) -> str:
    return chatbot_prompt(question)


def _normalize_question(question: str) -> str:
    return re.sub(r"[^a-z0-9\s]", "", question.lower())


def _detect_intent_keywords(text: str) -> List[str]:
    kws = []
    mapping = {
        "honeymoon": ["honeymoon", "romantic", "couple"],
        "budget": ["budget", "cheap", "affordable"],
        "adventure": ["adventure", "trek", "hiking", "ski", "thrill"],
        "family": ["family"],
        "beach": ["beach", "swim", "snorkel"],
        "winter": ["winter", "snow"],
        "summer": ["summer"],
        "luxury": ["luxury", "premium", "resort", "5 star"],
    }
    for key, words in mapping.items():
        if any(w in text for w in words):
            kws.append(key)
    return kws


def build_contextual_fallback(question: str) -> str:
    text = _normalize_question(question)
    intents = _detect_intent_keywords(text)

    # Short direct Q/A style for factual questions
    if text.startswith("how") or text.startswith("what") or text.startswith("why") or text.startswith("when") or text.startswith("where"):
        # Provide a concise, structured answer template
        answer = "Here's a concise answer:\n"
        answer += "- Summary: "
        # Simple heuristics for travel queries
        if "price" in text or "cost" in text or "budget" in intents:
            answer += "Costs vary by package; budget options start around ₹6,000 and luxury packages can exceed ₹30,000.\n"
            answer += "- Tips: compare inclusions (meals, transfers, guides) before booking.\n"
        elif "best" in text or "recommend" in text or intents:
            picks = []
            if "honeymoon" in intents:
                picks = ["Kerala Backwater Retreat", "Santorini Sunset Escape", "Luxury Maldives Getaway"]
            elif "adventure" in intents:
                picks = ["Leh Ladakh Explorer", "Iceland Northern Lights", "Banff Mountain Retreat"]
            elif "beach" in intents:
                picks = ["Goa Adventure Escape", "Andaman Island Escape", "Bali Beach Bliss"]
            elif "family" in intents:
                picks = ["Family Rajasthan Heritage", "Cape Town Wildlife Loop", "Ooty Hill Retreat"]
            else:
                picks = ["Goa Adventure Escape", "Kerala Backwater Retreat", "Bengaluru Food Trail"]
            answer += "Recommended picks: " + ", ".join(picks) + ".\n"
            answer += "- Next step: Tell me travel dates and number of people for a tailored option.\n"
        else:
            answer += "It depends on your preferences—tell me your travel dates, budget, and interests for tailored suggestions.\n"
        return answer + "\nWould you like me to suggest specific packages?"

    # Conversational style for general queries
    opening = "Sure — I can help with that.\n"
    if intents:
        opening += "Based on what you said, here are quick suggestions:\n"
        lines = []
        if "honeymoon" in intents:
            lines.append("• Romantic stays: Kerala backwaters, Santorini-style sunsets, Maldives overwater villas.")
        if "budget" in intents:
            lines.append("• Budget friendly: Himachal Trail, Pune Weekend Retreat, Nainital Lakeside Escape.")
        if "adventure" in intents:
            lines.append("• Adventure: Leh Ladakh, Banff, Iceland Northern Lights.")
        if "family" in intents:
            lines.append("• Family trips: Rajasthan Heritage, Cape Town Wildlife Loop, Mysore Palace Weekend.")
        if "beach" in intents:
            lines.append("• Beach picks: Goa, Andaman, Bali.")
        opening += "\n".join(lines)
        opening += "\n\nIf you want, I can narrow these to packages that match your dates and budget."
        return opening

    # Generic fallback helpful response
    return (
        "I can help plan trips, recommend packages, and answer travel questions.\n"
        "Try asking: 'Recommend a 5-day budget beach trip in June' or 'Best honeymoon spots in India'.\n"
        "If you give me dates, budget, and number of travelers, I can suggest exact packages."
    )


def answer_question(question: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")

    # Prefer OpenAI if available
    if api_key and OpenAI is not None:
        try:
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[{"role": "user", "content": build_chat_prompt(question)}],
                temperature=float(os.getenv("OPENAI_TEMP", 0.6)),
            )
            return response.choices[0].message.content.strip()
        except Exception as exc:
            print(f"OpenAI chatbot response failed: {exc}")

    # Local fallback that attempts to be helpful and human-like
    return build_contextual_fallback(question)
