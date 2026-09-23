import streamlit as st

from fuzzy_logic import calculate_collection_priority
from llm_processor import (
    extract_bin_information,
    generate_explanation
)


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Garbage Bin Fill Level Detection",
    page_icon="🗑️",
    layout="centered"
)


# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("🗑️ Garbage Bin Fill Level Detection")

st.write(
    """
This application combines **LangChain LLM reasoning**
with **Fuzzy Logic** to determine the collection priority
of a garbage bin.
"""
)


# --------------------------------------------------
# Natural language input
# --------------------------------------------------

st.subheader("Describe the Garbage Bin")

user_text = st.text_area(
    "Enter information about the bin:",
    placeholder=(
        "Example: The bin is about 85% full, "
        "contains around 40 kg of waste and "
        "has not been collected for 4 days."
    ),
    height=120
)


# --------------------------------------------------
# Analyze button
# --------------------------------------------------

if st.button("🔍 Analyze Bin", type="primary"):

    if not user_text.strip():

        st.warning(
            "Please enter a description of the garbage bin."
        )

    else:

        try:

            # ------------------------------------------
            # LangChain
            # ------------------------------------------

            with st.spinner(
                "AI is understanding the description..."
            ):

                extracted = extract_bin_information(
                    user_text
                )

            fill_level = float(
                extracted["fill_level"]
            )

            waste_weight = float(
                extracted["waste_weight"]
            )

            days_since_collection = float(
                extracted["days_since_collection"]
            )


            # ------------------------------------------
            # Display extracted values
            # ------------------------------------------

            st.subheader("🤖 AI Extracted Information")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Fill Level",
                    f"{fill_level:.0f}%"
                )

            with col2:
                st.metric(
                    "Waste Weight",
                    f"{waste_weight:.1f} kg"
                )

            with col3:
                st.metric(
                    "Days Since Collection",
                    f"{days_since_collection:.0f}"
                )


            # ------------------------------------------
            # Fuzzy Logic
            # ------------------------------------------

            # Convert weight to fuzzy-system range.
            # Here 100 kg is treated as maximum.
            fuzzy_weight = min(
                waste_weight,
                100
            )

            priority, status = calculate_collection_priority(
                fill_level,
                fuzzy_weight,
                days_since_collection
            )


            # ------------------------------------------
            # Fuzzy output
            # ------------------------------------------

            st.subheader("🧠 Fuzzy Logic Result")

            st.metric(
                "Collection Priority",
                f"{priority:.2f}/100"
            )

            if status == "HIGH PRIORITY":

                st.error(
                    f"🚨 {status}"
                )

            elif status == "MEDIUM PRIORITY":

                st.warning(
                    f"⚠️ {status}"
                )

            else:

                st.success(
                    f"✅ {status}"
                )


            # ------------------------------------------
            # LLM Explanation
            # ------------------------------------------

            with st.spinner(
                "Generating explanation..."
            ):

                explanation = generate_explanation(
                    user_text,
                    fill_level,
                    waste_weight,
                    days_since_collection,
                    priority,
                    status
                )

            st.subheader("💬 AI Explanation")

            st.write(explanation)


            # ------------------------------------------
            # Show fuzzy rules
            # ------------------------------------------

            with st.expander(
                "📋 View Fuzzy Rules"
            ):

                st.write(
                    """
                    **Rule 1:**  
                    IF fill is LOW AND weight is LOW AND
                    collection is RECENT → priority is LOW

                    **Rule 2:**  
                    IF fill is MEDIUM AND weight is MEDIUM
                    → priority is MEDIUM

                    **Rule 3:**  
                    IF fill is HIGH → priority is HIGH

                    **Rule 4:**  
                    IF fill is HIGH AND weight is HIGH
                    → priority is HIGH

                    **Rule 5:**  
                    IF fill is HIGH AND collection is LONG
                    → priority is HIGH

                    **Rule 6:**  
                    IF weight is HIGH AND collection is LONG
                    → priority is HIGH

                    **Rule 7:**  
                    IF fill is MEDIUM AND collection is LONG
                    → priority is HIGH

                    **Rule 8:**  
                    IF fill is LOW AND weight is MEDIUM
                    AND collection is LONG → priority is MEDIUM
                    """
                )


        except Exception as e:

            st.error(
                "Something went wrong while processing the request."
            )

            st.exception(e)