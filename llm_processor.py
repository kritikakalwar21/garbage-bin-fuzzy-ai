import os
import json

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


load_dotenv()


def extract_bin_information(user_text):

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
You are a garbage-bin monitoring assistant.

Extract these three values from the user's description:

1. fill_level: percentage from 0 to 100
2. waste_weight: estimated waste weight in kilograms
3. days_since_collection: number of days since last collection

Return ONLY valid JSON in this format:

{
    "fill_level": number,
    "waste_weight": number,
    "days_since_collection": number
}

If a value is not mentioned, make a reasonable estimate based
on the user's description.
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

    content = response.content

    # Remove markdown formatting if model adds it
    content = content.replace("```json", "")
    content = content.replace("```", "")
    content = content.strip()

    data = json.loads(content)

    return data


def generate_explanation(
    user_text,
    fill_level,
    waste_weight,
    days_since_collection,
    priority,
    status
):

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.3
    )

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
You are a smart waste-management assistant.

Explain the garbage-bin fuzzy-logic result in simple language.

Mention:
- fill level
- waste weight
- days since collection
- fuzzy collection priority
- collection status
- recommended action

Do not claim that this is a physical sensor measurement.
"""
        ),
        (
            "human",
            """
Original user description:
{user_text}

Detected values:
Fill Level: {fill_level}%
Waste Weight: {waste_weight} kg
Days Since Collection: {days_since_collection}

Fuzzy Collection Priority: {priority:.2f}/100
Status: {status}
"""
        )
    ])

    chain = prompt | llm

    response = chain.invoke({
        "user_text": user_text,
        "fill_level": fill_level,
        "waste_weight": waste_weight,
        "days_since_collection": days_since_collection,
        "priority": priority,
        "status": status
    })

    return response.content