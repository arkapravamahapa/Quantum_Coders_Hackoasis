import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from utils import scheduler, storage
import google.generativeai as genai
import matplotlib.pyplot as plt
from collections import Counter

st.set_page_config(page_title="Revision Scheduler", page_icon="📚", layout="wide")
st.title("📚 Personalized Revision Scheduler")

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-2.0-flash')

try:
    deck = pd.read_csv("data/sample_deck.csv")
except FileNotFoundError:
    st.error("`sample_deck.csv` not found!")
    st.stop()

if 'user_progress' not in st.session_state:
    st.session_state.user_progress = storage.load_progress()

    if not st.session_state.user_progress:
        for _, row in deck.iterrows():
            card_id = row['Question']
            st.session_state.user_progress[card_id] = {
                'question': row['Question'],
                'answer': row['Answer'],
                'repetitions': 0,
                'interval': 0,
                'ease_factor': 2.5,
                'last_reviewed': None,
                'next_review': (datetime.now() - timedelta(days=1)).isoformat()
            }
        storage.save_progress(st.session_state.user_progress)

st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Calendar", "Import/Export"])

st.sidebar.subheader("AI Features")
ai_note = st.sidebar.text_area("Generate a question from a note:", height=100)

if st.sidebar.button("Generate Question", key="ai_generate"):
    if ai_note:
        with st.spinner("Generating..."):
            questions = []
            num_questions = 10
            for i in range(num_questions):
                try:
                    prompt = (
                        f"Generate a single flashcard question from the following note: {ai_note}. "
                        f"Question must be different from previous questions generated."
                    )
                    response = model.generate_content(prompt)
                    questions.append(response.text.strip())
                except Exception as e:
                    st.sidebar.error(f"Error generating question {i+1}: {e}")
                    break

            if questions:
                st.sidebar.success(f"Generated {len(questions)} Questions:")
                for q in questions:
                    st.sidebar.write(f"- {q}")
    else:
        st.sidebar.warning("Please enter a note to generate a question.")

if page == "Dashboard":
    st.header("Today's Review")

    cards_due = scheduler.get_cards_due_today(st.session_state.user_progress)
    st.metric(label="Cards Due Today", value=len(cards_due))

    if not cards_due:
        st.info("You have no cards due for review today. Great job!")

    for i, card_data in enumerate(cards_due):
        st.subheader(card_data['question'])
        with st.expander("Show Answer"):
            st.write(card_data['answer'])

        feedback = st.radio(
            "Grade yourself:",
            ["Again", "Hard", "Good", "Easy"],
            key=f"feedback_{i}",
            horizontal=True
        )

        if feedback:
            card_id = card_data['question']
            st.session_state.user_progress[card_id]['grade'] = feedback
            updated_card = scheduler.calculate_next_review(st.session_state.user_progress[card_id])
            st.session_state.user_progress[card_id] = updated_card
            storage.save_progress(st.session_state.user_progress)
            st.success("Progress saved!")
            st.rerun()

elif page == "Calendar":
    st.header("Study Progress Calendar")

    st.subheader("Study History")
    review_dates = [
        datetime.fromisoformat(card['last_reviewed']).date()
        for card in st.session_state.user_progress.values()
        if card.get('last_reviewed')
    ]

    if review_dates:
        date_counts = Counter(review_dates)
        fig, ax = plt.subplots(figsize=(10, 4))
        sorted_dates = sorted(date_counts.keys())
        ax.bar(
            [d.strftime('%Y-%m-%d') for d in sorted_dates],
            [date_counts[d] for d in sorted_dates]
        )
        ax.set_title("Study History")
        ax.set_ylabel("Cards Reviewed")
        ax.set_xlabel("Date")
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.info("No study history to display yet.")

    st.subheader("Grading Distribution")
    grades = [card['grade'] for card in st.session_state.user_progress.values() if 'grade' in card]

    if grades:
        grade_counts = pd.Series(grades).value_counts()
        fig, ax = plt.subplots()
        ax.pie(grade_counts, labels=grade_counts.index, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        st.pyplot(fig)
    else:
        st.info("No grading data to display yet.")

elif page == "Import/Export":
    st.header("Manage Flashcards")

    uploaded_file = st.file_uploader(
        "Upload a CSV file with 'Question' and 'Answer' columns", type="csv"
    )
    if uploaded_file is not None:
        uploaded_df = pd.read_csv(uploaded_file)
        st.write("Preview of new cards:", uploaded_df)

        if st.button("Add to Deck"):
            for _, row in uploaded_df.iterrows():
                card_id = row['Question']
                st.session_state.user_progress[card_id] = {
                    'question': row['Question'],
                    'answer': row['Answer'],
                    'repetitions': 0,
                    'interval': 0,
                    'ease_factor': 2.5,
                    'last_reviewed': None,
                    'next_review': (datetime.now() - timedelta(minutes=1)).isoformat()
                }
            storage.save_progress(st.session_state.user_progress)
            st.success("New cards added to your deck!")
            st.rerun()

    st.download_button(
        label="Download Progress Data",
        data=storage.export_progress(),
        file_name="user_progress.json",
        mime="application/json"
    )
