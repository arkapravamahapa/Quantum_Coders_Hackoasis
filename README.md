# Quantum_Coders_Hackoasis
📚 Personalized Revision Scheduler
This is a web application built to help students study more effectively using the power of spaced repetition. The app intelligently schedules flashcards for review, personalizes the learning experience with AI, and provides visual insights into study habits.
The project is built entirely in Python using the Streamlit framework, making it a powerful yet simple-to-run web app.
✨ Features
 * Spaced Repetition (SM-2 Algorithm): The core of the app. It dynamically adjusts a card's next review date based on your grading (Again, Hard, Good, Easy) to optimize learning and retention.
 * AI-Powered Flashcard Generation: Using the Gemini API, you can generate multiple flashcard questions from your notes or any text, streamlining the process of creating study materials.
 * Multiple Decks: Organize your flashcards into different subjects or topics. The app supports creating and managing multiple decks for various study needs.
 * Progress Visualization: A dynamic calendar heatmap shows your study streaks and a pie chart visualizes your grading distribution, helping you track your progress at a glance.
 * Data Management: Easily import your flashcards from a CSV file and save your study history locally.
🚀 Setup & Installation
To run this app locally, follow these steps.
Prerequisites
 * Python 3.8+
 * A Gemini API Key (from Google AI Studio)
Step 1: Clone the Repository & Set Up Environment
git clone https://github.com/your-username/revision-scheduler.git
cd revision-scheduler
python -m venv venv
source venv/bin/activate

Step 2: Install Dependencies
Install all the required libraries from the requirements.txt file.
pip install -r requirements.txt

Step 3: Configure Your API Key
Create a folder named .streamlit in your project's root directory and a file named secrets.toml inside it. Add your Gemini API key to this file.
# .streamlit/secrets.toml
GEMINI_API_KEY = "your_gemini_api_key_here"

Step 4: Run the App
Launch the application from your terminal.
streamlit run app.py

The app will automatically open in your web browser.
