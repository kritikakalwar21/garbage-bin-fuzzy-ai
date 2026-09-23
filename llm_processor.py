import os
import json

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

# ============================================================
# LOAD API KEY
# ============================================================

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY is missing. Add it to your .env file."
    )


# ============================================================
# GEMINI MODEL
# ============================================================

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0
)


# ============================================================
# RESPONSE TEXT HANDLER
# ============================================================

def get_response_text(response):

    content = response.content

    if isinstance(content, str):
        return content

    if isinstance(content, list):

        text_parts = []

        for item in content:

            if isinstance(item, str):
                text_parts.append(item)

            elif isinstance(item, dict):

                if "text" in item:
                    text_parts.append(item["text"])

        return "".join(text_parts)

    return str(content)


# ============================================================
# EXTRACT BIN INFORMATION USING LANGCHAIN + GEMINI
# ============================================================

def extract_bin_information(user_text):

    prompt = ChatPromptTemplate.from_messages([

        (
            "system",
            """
You are a smart garbage-bin monitoring assistant.

Read the user's natural-language description of a garbage bin.

Extract these values:

1. fill_level
2. waste_weight
3. days_since_collection
4. location
5. bin_type

Return ONLY valid JSON.

Use exactly this structure:

{{
    "fill_level": 50,
    "waste_weight": 0,
    "days_since_collection": 0,
    "location": "Unknown",
    "bin_type": "General Waste"
}}

Rules:

FILL LEVEL:
- Must be between 0 and 100.
- "85% full" means 85.
- "half full" means 50.
- "almost full" means 90.
- If not mentioned, use 50.

WASTE WEIGHT:
- Must be in kilograms.
- "18 kg of waste" means 18.
- If not mentioned, use 0.

DAYS SINCE COLLECTION:
- Extract the number of days since the garbage was last collected.
- "collected 3 days ago" means 3.
- "last collection was 5 days ago" means 5.
- "not collected for 7 days" means 7.
- If the user says "today", use 0.
- If not mentioned, use 0.

LOCATION:
- Extract the location if provided.
- If not provided, use "Unknown".

BIN TYPE:
- Extract the bin type if provided.
- Examples: General Waste, Plastic, Organic, Dry Waste, Wet Waste.
- If not provided, use "General Waste".

Do not add explanations.
Do not use Markdown.
Return only JSON.
"""
        ),

        (
            "human",
            "{user_text}"
        )
    ])

    # ========================================================
    # LANGCHAIN FLOW
    # ========================================================

    chain = prompt | llm

    response = chain.invoke({
        "user_text": user_text
    })

    # ========================================================
    # CONVERT RESPONSE TO TEXT
    # ========================================================

    result = get_response_text(response).strip()

    # Remove Markdown code fences if Gemini adds them
    result = result.replace("```json", "")
    result = result.replace("```", "")
    result = result.strip()

    # ========================================================
    # PARSE JSON
    # ========================================================

    try:

        data = json.loads(result)

    except json.JSONDecodeError:

        data = {
            "fill_level": 50,
            "waste_weight": 0,
            "days_since_collection": 0,
            "location": "Unknown",
            "bin_type": "General Waste"
        }

    # ========================================================
    # FILL LEVEL
    # ========================================================

    try:

        fill_level = float(
            data.get("fill_level", 50)
        )

    except (ValueError, TypeError):

        fill_level = 50

    fill_level = max(
        0,
        min(100, fill_level)
    )

    # ========================================================
    # WASTE WEIGHT
    # ========================================================

    try:

        waste_weight = float(
            data.get("waste_weight", 0)
        )

    except (ValueError, TypeError):

        waste_weight = 0

    waste_weight = max(
        0,
        waste_weight
    )

    # ========================================================
    # DAYS SINCE COLLECTION
    # ========================================================

    try:

        days_since_collection = float(
            data.get("days_since_collection", 0)
        )

    except (ValueError, TypeError):

        days_since_collection = 0

    days_since_collection = max(
        0,
        days_since_collection
    )

    # ========================================================
    # LOCATION
    # ========================================================

    location = data.get(
        "location",
        "Unknown"
    )

    if not isinstance(location, str):
        location = "Unknown"

    # ========================================================
    # BIN TYPE
    # ========================================================

    bin_type = data.get(
        "bin_type",
        "General Waste"
    )

    if not isinstance(bin_type, str):
        bin_type = "General Waste"

    # ========================================================
    # RETURN ALL INFORMATION
    # ========================================================

    return {

        "fill_level": fill_level,

        "waste_weight": waste_weight,

        "days_since_collection": days_since_collection,

        "location": location,

        "bin_type": bin_type
    }


# ============================================================
# GENERATE EXPLANATION
# ============================================================

def generate_explanation(
    fill_level,
    waste_weight,
    days_since_collection,
    priority
):

    prompt = ChatPromptTemplate.from_messages([

        (
            "system",
            """
You are a garbage collection assistant.

Explain the garbage-bin collection priority
in simple language.

Mention:
- Fill level
- Waste weight
- Days since last collection
- Collection priority
- Why this priority was assigned

Keep the explanation short and easy to understand.
"""
        ),

        (
            "human",
            """
Fill level: {fill_level}%

Waste weight: {waste_weight} kg

Days since collection: {days_since_collection}

Collection priority: {priority}
"""
        )
    ])

    chain = prompt | llm

    response = chain.invoke({

        "fill_level": fill_level,

        "waste_weight": waste_weight,

        "days_since_collection": days_since_collection,

        "priority": priority
    })

    return get_response_text(response).strip()