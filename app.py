import streamlit as st

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent / "src"))

from content.topics import TOPICS
from pipeline.baseline import run_tier1

st.set_page_config(page_title="Tier-1 Baseline", layout="centered")

st.title("Adaptive Explanation System – Tier 1 Baseline")

topic = st.selectbox("Select a topic", list(TOPICS.keys()))
question = TOPICS[topic]["question"]
correct_answer = TOPICS[topic]["answer"]

st.write("### Question")
st.write(question)

user_answer = st.text_area("Your Answer")

if st.button("Submit"):
    explanation = run_tier1(user_answer, correct_answer, topic)

    st.write("### Generated Explanation")
    st.write(explanation)
