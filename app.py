import os
import json

import streamlit as st
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Garbage Bin Fill Level Detection",
    page_icon="🗑️",
    layout="centered"
)


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


# ============================================================
# TITLE
# ============================================================

st.title("🗑️ Garbage Bin Fill Level Detection")

st.write(
    """
    This system uses **LangChain + Gemini AI** to understand
    a natural-language description of a garbage bin and
    **Fuzzy Logic** to calculate its collection priority.
    """
)


# ============================================================
# CHECK API KEY
# ============================================================

if not GOOGLE_API_KEY:

    st.error(
        "GOOGLE_API_KEY is missing. "
        "Create a .env file and add your Google Gemini API key."
    )

    st.stop()


# ============================================================
# INITIALIZE GEMINI
# ============================================================

try:

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        google_api_key=GOOGLE_API_KEY,
        temperature=0
    )

except Exception as e:

    st.error(f"Could not initialize Gemini: {e}")

    st.stop()


# ============================================================
# FUNCTION: GET TEXT FROM GEMINI RESPONSE
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

                    text_parts.append(
                        item["text"]
                    )

        return "".join(text_parts)

    return str(content)


# ============================================================
# LANGCHAIN FUNCTION
# EXTRACT INFORMATION FROM NATURAL LANGUAGE
# ============================================================

def extract_bin_information(user_text):

    prompt = ChatPromptTemplate.from_messages([

        (
            "system",
            """
You are an intelligent garbage-bin monitoring assistant.

Read the user's description of a garbage bin.

Extract the following information:

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
- Use kilograms.
- "18 kg of waste" means 18.
- If not mentioned, use 0.

DAYS SINCE COLLECTION:
- "collected 3 days ago" means 3.
- "not collected for 5 days" means 5.
- "last collected yesterday" means 1.
- "collected today" means 0.
- If not mentioned, use 0.

LOCATION:
- Extract the location.
- If not mentioned, use "Unknown".

BIN TYPE:
- Extract the bin type.
- Examples: General Waste, Plastic, Organic,
  Dry Waste, Wet Waste.
- If not mentioned, use "General Waste".

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

    chain = prompt | llm

    response = chain.invoke({
        "user_text": user_text
    })

    result = get_response_text(response).strip()

    # Remove markdown if Gemini adds it
    result = result.replace("```json", "")
    result = result.replace("```", "")
    result = result.strip()

    try:

        data = json.loads(result)

    except json.JSONDecodeError:

        return {
            "fill_level": 50,
            "waste_weight": 0,
            "days_since_collection": 0,
            "location": "Unknown",
            "bin_type": "General Waste"
        }

    # --------------------------------------------------------
    # Fill level
    # --------------------------------------------------------

    try:

        fill_level = float(
            data.get("fill_level", 50)
        )

    except:

        fill_level = 50

    fill_level = max(
        0,
        min(100, fill_level)
    )

    # --------------------------------------------------------
    # Waste weight
    # --------------------------------------------------------

    try:

        waste_weight = float(
            data.get("waste_weight", 0)
        )

    except:

        waste_weight = 0

    waste_weight = max(
        0,
        waste_weight
    )

    # --------------------------------------------------------
    # Days since collection
    # --------------------------------------------------------

    try:

        days_since_collection = float(
            data.get(
                "days_since_collection",
                0
            )
        )

    except:

        days_since_collection = 0

    days_since_collection = max(
        0,
        days_since_collection
    )

    # --------------------------------------------------------
    # Location
    # --------------------------------------------------------

    location = data.get(
        "location",
        "Unknown"
    )

    if not isinstance(location, str):

        location = "Unknown"

    # --------------------------------------------------------
    # Bin type
    # --------------------------------------------------------

    bin_type = data.get(
        "bin_type",
        "General Waste"
    )

    if not isinstance(bin_type, str):

        bin_type = "General Waste"

    # --------------------------------------------------------
    # Return extracted information
    # --------------------------------------------------------

    return {

        "fill_level": fill_level,

        "waste_weight": waste_weight,

        "days_since_collection":
            days_since_collection,

        "location": location,

        "bin_type": bin_type
    }


# ============================================================
# FUZZY LOGIC SYSTEM
# ============================================================

def calculate_collection_priority(
    fill_level,
    waste_weight,
    days_since_collection
):

    # --------------------------------------------------------
    # INPUT VARIABLES
    # --------------------------------------------------------

    fill = ctrl.Antecedent(
        np.arange(0, 101, 1),
        "fill"
    )

    weight = ctrl.Antecedent(
        np.arange(0, 51, 1),
        "weight"
    )

    days = ctrl.Antecedent(
        np.arange(0, 11, 1),
        "days"
    )

    priority = ctrl.Consequent(
        np.arange(0, 101, 1),
        "priority"
    )


    # ========================================================
    # MEMBERSHIP FUNCTIONS
    # ========================================================

    # --------------------------------------------------------
    # FILL LEVEL
    # --------------------------------------------------------

    fill["low"] = fuzz.trimf(
        fill.universe,
        [0, 0, 40]
    )

    fill["medium"] = fuzz.trimf(
        fill.universe,
        [25, 50, 75]
    )

    fill["high"] = fuzz.trimf(
        fill.universe,
        [60, 100, 100]
    )


    # --------------------------------------------------------
    # WASTE WEIGHT
    # --------------------------------------------------------

    weight["low"] = fuzz.trimf(
        weight.universe,
        [0, 0, 15]
    )

    weight["medium"] = fuzz.trimf(
        weight.universe,
        [10, 25, 40]
    )

    weight["high"] = fuzz.trimf(
        weight.universe,
        [30, 50, 50]
    )


    # --------------------------------------------------------
    # DAYS SINCE COLLECTION
    # --------------------------------------------------------

    days["recent"] = fuzz.trimf(
        days.universe,
        [0, 0, 3]
    )

    days["moderate"] = fuzz.trimf(
        days.universe,
        [2, 5, 7]
    )

    days["long"] = fuzz.trimf(
        days.universe,
        [6, 10, 10]
    )


    # --------------------------------------------------------
    # OUTPUT PRIORITY
    # --------------------------------------------------------

    priority["low"] = fuzz.trimf(
        priority.universe,
        [0, 0, 40]
    )

    priority["medium"] = fuzz.trimf(
        priority.universe,
        [30, 50, 70]
    )

    priority["high"] = fuzz.trimf(
        priority.universe,
        [60, 80, 100]
    )

    priority["urgent"] = fuzz.trimf(
        priority.universe,
        [80, 100, 100]
    )


    # ========================================================
    # FUZZY RULES
    # ========================================================

    rule1 = ctrl.Rule(
        fill["low"] &
        weight["low"] &
        days["recent"],
        priority["low"]
    )

    rule2 = ctrl.Rule(
        fill["medium"] &
        weight["medium"],
        priority["medium"]
    )

    rule3 = ctrl.Rule(
        fill["high"] &
        weight["medium"],
        priority["high"]
    )

    rule4 = ctrl.Rule(
        fill["high"] &
        weight["high"],
        priority["urgent"]
    )

    rule5 = ctrl.Rule(
        days["long"] &
        fill["high"],
        priority["urgent"]
    )

    rule6 = ctrl.Rule(
        days["long"] &
        weight["high"],
        priority["urgent"]
    )

    rule7 = ctrl.Rule(
        fill["medium"] &
        days["moderate"],
        priority["medium"]
    )

    rule8 = ctrl.Rule(
        fill["low"] &
        days["long"],
        priority["medium"]
    )

    rule9 = ctrl.Rule(
        fill["high"] &
        days["moderate"],
        priority["high"]
    )

    rule10 = ctrl.Rule(
        weight["high"] &
        days["moderate"],
        priority["high"]
    )


    # ========================================================
    # CONTROL SYSTEM
    # ========================================================

    priority_control = ctrl.ControlSystem([

        rule1,
        rule2,
        rule3,
        rule4,
        rule5,
        rule6,
        rule7,
        rule8,
        rule9,
        rule10

    ])


    simulation = ctrl.ControlSystemSimulation(
        priority_control
    )


    # ========================================================
    # FUZZIFICATION
    # ========================================================

    simulation.input["fill"] = fill_level

    simulation.input["weight"] = min(
        weight_input := waste_weight,
        50
    )

    simulation.input["days"] = min(
        days_since_collection,
        10
    )


    # ========================================================
    # FUZZY INFERENCE + DEFUZZIFICATION
    # ========================================================

    simulation.compute()

    result = simulation.output["priority"]


    # ========================================================
    # CONVERT NUMBER TO STATUS
    # ========================================================

    if result < 30:

        status = "Low Priority"

    elif result < 60:

        status = "Medium Priority"

    elif result < 80:

        status = "High Priority"

    else:

        status = "Urgent Collection"


    return result, status


# ============================================================
# AI EXPLANATION
# ============================================================

def generate_explanation(
    user_text,
    fill_level,
    waste_weight,
    days_since_collection,
    location,
    status
):

    prompt = ChatPromptTemplate.from_messages([

        (
            "system",
            """
You are a garbage collection assistant.

Explain the garbage-bin collection result
in simple language.

Mention:
- Fill level
- Waste weight
- Days since collection
- Location
- Collection status
- Why the fuzzy system assigned this status

Do not invent information.

Keep the explanation short.
"""
        ),

        (
            "human",
            """
Original user description:
{user_text}

Fill level: {fill_level}%

Waste weight: {waste_weight} kg

Days since collection: {days_since_collection}

Location: {location}

Collection status: {status}
"""
        )
    ])

    chain = prompt | llm

    response = chain.invoke({

        "user_text": user_text,

        "fill_level": fill_level,

        "waste_weight": waste_weight,

        "days_since_collection":
            days_since_collection,

        "location": location,

        "status": status
    })

    return get_response_text(response).strip()


# ============================================================
# STREAMLIT USER INPUT
# ============================================================

st.subheader("📝 Describe the Garbage Bin")

user_text = st.text_area(
    "Enter a description:",
    placeholder=(
        "Example: The garbage bin near the college gate "
        "is 85% full, contains 18 kg of waste, "
        "and has not been collected for 4 days."
    ),
    height=150
)


# ============================================================
# ANALYZE BUTTON
# ============================================================

if st.button(
    "🔍 Analyze Garbage Bin",
    use_container_width=True
):

    if not user_text.strip():

        st.warning(
            "Please enter a description of the garbage bin."
        )

        st.stop()


    # ========================================================
    # STEP 1 - LANGCHAIN EXTRACTION
    # ========================================================

    with st.spinner(
        "🤖 AI is understanding the description..."
    ):

        try:

            extracted = extract_bin_information(
                user_text
            )

        except Exception as e:

            st.error(
                f"AI extraction error: {e}"
            )

            st.stop()


    # ========================================================
    # SHOW EXTRACTED DATA
    # ========================================================

    st.subheader(
        "🤖 AI Extracted Information"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Fill Level",
            f"{extracted['fill_level']:.0f}%"
        )

        st.metric(
            "Waste Weight",
            f"{extracted['waste_weight']:.1f} kg"
        )

    with col2:

        st.metric(
            "Days Since Collection",
            f"{extracted['days_since_collection']:.0f}"
        )

        st.write(
            "**Location:**",
            extracted["location"]
        )

        st.write(
            "**Bin Type:**",
            extracted["bin_type"]
        )


    # ========================================================
    # STEP 2 - FUZZY LOGIC
    # ========================================================

    with st.spinner(
        "🧠 Fuzzy Logic is calculating priority..."
    ):

        try:

            priority_score, status = (
                calculate_collection_priority(

                    extracted["fill_level"],

                    extracted["waste_weight"],

                    extracted[
                        "days_since_collection"
                    ]
                )
            )

        except Exception as e:

            st.error(
                f"Fuzzy Logic error: {e}"
            )

            st.stop()


    # ========================================================
    # SHOW FUZZY RESULT
    # ========================================================

    st.subheader(
        "🧠 Fuzzy Logic Result"
    )

    st.metric(
        "Collection Priority Score",
        f"{priority_score:.2f} / 100"
    )

    st.info(
        f"📌 **{status}**"
    )


    # ========================================================
    # STEP 3 - AI EXPLANATION
    # ========================================================

    with st.spinner(
        "💬 AI is generating an explanation..."
    ):

        try:

            explanation = generate_explanation(

                user_text,

                extracted["fill_level"],

                extracted["waste_weight"],

                extracted[
                    "days_since_collection"
                ],

                extracted["location"],

                status
            )

        except Exception as e:

            st.warning(
                f"Could not generate AI explanation: {e}"
            )

            explanation = (
                f"The bin has a fill level of "
                f"{extracted['fill_level']:.0f}%, "
                f"contains approximately "
                f"{extracted['waste_weight']:.1f} kg "
                f"of waste, and has not been collected "
                f"for {extracted['days_since_collection']:.0f} days."
            )


    # ========================================================
    # SHOW EXPLANATION
    # ========================================================

    st.subheader(
        "💬 AI Explanation"
    )

    st.write(explanation)


    # ========================================================
    # PROJECT FLOW
    # ========================================================

    st.divider()

    st.subheader(
        "🔄 System Flow"
    )

    st.write(
        """
        **Natural Language Input**
        ↓
        
        **LangChain + Gemini**
        ↓
        
        **Information Extraction**
        ↓
        
        **Fuzzification**
        ↓
        
        **Fuzzy Rule Evaluation**
        ↓
        
        **Defuzzification**
        ↓
        
        **Collection Priority**
        ↓
        
        **LangChain + Gemini Explanation**
        """
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("📚 About the Project")

    st.write(
        """
        **Garbage Bin Fill Level Detection**

        This mini project combines two AI techniques:

        ### 1. AI / LLM Component

        LangChain + Gemini understands
        natural-language descriptions.

        Example:

        "The bin is almost full and hasn't
        been collected for 5 days."

        The LLM extracts numerical information.

        ### 2. Fuzzy Logic Component

        Fuzzy Logic uses:

        • Fill Level  
        • Waste Weight  
        • Days Since Collection

        to calculate a collection priority.

        ### Fuzzy Output

        • Low Priority
        • Medium Priority
        • High Priority
        • Urgent Collection
        """
    )