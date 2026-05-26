import os

from openai import OpenAI

from .prompts import itinerary_prompt


def build_prompt(destination: str, days: int, budget: float, interests: str, travel_type: str) -> str:
    return itinerary_prompt(destination, days, budget, interests, travel_type)


def fallback_itinerary(destination: str, days: int, budget: float, interests: str, travel_type: str) -> str:
    interest_tags = [tag.strip().lower() for tag in interests.replace(",", " ").split() if tag.strip()]
    daily_budget = round(budget / days, 2)

    summary = f"Here is a dynamic {days}-day itinerary for {destination} built for {travel_type} travel with a budget of ₹{budget}."
    day_lines = [f"Day 1: Start with a city walk, local food tasting, and a gentle introduction to {destination}. Budget around ₹{daily_budget}."]

    if any(tag in ["adventure", "trek", "water", "sports"] for tag in interest_tags):
        day_lines.append(f"Day 2: Add adventure activities such as trekking, boating, or ziplining. Budget around ₹{daily_budget}.")
    else:
        day_lines.append(f"Day 2: Explore museums, markets, and local cultural experiences. Budget around ₹{daily_budget}.")

    if any(tag in ["honeymoon", "romantic", "couple"] for tag in interest_tags):
        day_lines.append(f"Day 3: Choose a romantic evening walk, sunset spots, and a cozy café. Budget around ₹{daily_budget}.")
    else:
        day_lines.append(f"Day 3: Visit local attractions and relax at a scenic viewpoint. Budget around ₹{daily_budget}.")

    if days >= 4:
        day_lines.append(f"Day 4: Plan a local day trip, village visit, or group activity based on the interest profile. Budget around ₹{daily_budget}.")

    if days >= 5:
        day_lines.append(f"Day 5: Add a shopping or photography day and conclude with a final meal. Budget around ₹{daily_budget}.")

    return "\n\n".join([
        summary,
        "\n".join(day_lines),
        f"Budget breakdown: Accommodation around ₹{round(budget * 0.4, 2)}, Food around ₹{round(budget * 0.3, 2)}, Activities around ₹{round(budget * 0.2, 2)}, Transport around ₹{round(budget * 0.1, 2)}.",
        f"Hotel suggestions: Choose a budget hotel near the city center, or a homestay if you prefer a lower-cost and local experience.",
        f"Food recommendations: Try local street food, small cafés, and one sit-down restaurant for a special meal.",
        "Safety tips: Keep a copy of the hotel address, travel in daylight for local trips, and carry a basic first-aid kit.",
        f"Must-visit attractions: Use the destination's local highlights and add one hidden gem based on {interests}.",
    ])


def generate_itinerary(destination: str, days: int, budget: float, interests: str, travel_type: str) -> str:
    prompt = build_prompt(destination, days, budget, interests, travel_type)
    api_key = os.getenv("OPENAI_API_KEY")

    if api_key:
        try:
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()
        except Exception as exc:
            print(f"OpenAI itinerary generation failed: {exc}")

    return fallback_itinerary(destination, days, budget, interests, travel_type)
