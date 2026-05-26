import os
import re

from openai import OpenAI

from .prompts import chatbot_prompt


def build_chat_prompt(question: str) -> str:
    return chatbot_prompt(question)


def _normalize_question(question: str) -> str:
    return re.sub(r"[^a-z0-9\s]", "", question.lower())


def build_contextual_fallback(question: str) -> str:
    text = _normalize_question(question)

    if any(keyword in text for keyword in ["honeymoon", "romantic", "couple"]):
        return (
            "For a romantic trip, our strongest picks are Kerala, Udaipur, Santorini-style luxury stays, and Maldives. "
            "If you want a calm and scenic experience, Kerala is a great first choice, while Maldives suits a premium honeymoon."
        )

    if any(keyword in text for keyword in ["budget", "cheap", "affordable"]):
        return (
            "Budget-friendly options include Budget Himachal Trail, Pune Weekend Retreat, Nainital Lakeside Escape, and Bengaluru Food Trail. "
            "These packages are good for students and first-time travelers who want a memorable trip without overspending."
        )

    if any(keyword in text for keyword in ["summer"]):
        return (
            "For summer travel, consider Goa, Kerala, Andaman, and Bali. These destinations are popular for beaches, relaxed stays, and easy booking options."
        )

    if any(keyword in text for keyword in ["winter"]):
        return (
            "For winter travel, Gulmarg, Manali, Dharamshala, and Iceland Northern Lights are excellent picks. These packages are ideal when you want snow, cozy stays, and scenic mountain views."
        )

    if any(keyword in text for keyword in ["adventure", "trek", "hiking", "ski", "thrill"]):
        return (
            "Adventure-focused options include Goa Adventure Escape, Leh Ladakh Explorer, Banff Mountain Retreat, and Iceland Northern Lights. "
            "These trips work well if you want a mix of outdoor activity and memorable sightseeing."
        )

    if any(keyword in text for keyword in ["family"]):
        return (
            "Family-friendly suggestions include Family Rajasthan Heritage, Cape Town Wildlife Loop, Ooty Hill Retreat, and Mysore Palace Weekend. "
            "These tours are comfortable, easy to plan, and good for all age groups."
        )

    if any(keyword in text for keyword in ["luxury", "premium", "resort", "5 star"]):
        return (
            "Premium choices include Luxury Maldives Getaway, Dubai Desert & Skyline, Swiss Alps Luxury Rail, and Santorini Sunset Escape. "
            "These packages focus on comfort, scenic stays, and high-touch guided experiences."
        )

    if any(keyword in text for keyword in ["student", "college", "young", "budget"]):
        return (
            "Student-friendly packages include Goa Adventure Escape, Budget Himachal Trail, and Bengaluru Food Trail. "
            "They are easy to plan, affordable, and ideal for short university breaks."
        )

    if any(keyword in text for keyword in ["beach"]):
        return (
            "Beach destinations you can explore include Goa, Bali, Andaman, and Maldives. "
            "Choose Goa for affordability, Andaman for crystal-clear water, or Maldives for a premium retreat."
        )

    if any(keyword in text for keyword in ["hill", "mountain", "manali", "ooty", "nainital", "dharamshala", "gulmarg"]):
        return (
            "Hill station ideas include Manali, Ooty, Nainital, Dharamshala, and Gulmarg. These routes are great for cool weather, scenic viewpoints, and easy weekend planning."
        )

    return (
        "I can help with honeymoon ideas, budget trips, summer and winter picks, adventure tours, family travel, luxury stays, student-friendly options, beach destinations, and hill stations. "
        "If you want, I can also recommend the best package based on your travel preferences."
    )


def answer_question(question: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")

    if api_key:
        try:
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[{"role": "user", "content": build_chat_prompt(question)}],
                temperature=0.6,
            )
            return response.choices[0].message.content.strip()
        except Exception as exc:
            print(f"OpenAI chatbot response failed: {exc}")

    return build_contextual_fallback(question)
