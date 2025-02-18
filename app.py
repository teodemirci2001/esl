import streamlit as st
import openai

# Set your OpenAI API key
openai.api_key = "your_openai_api_key_here"

# Define the exam questions
part1_questions = [
    "What is your name?",
    "Where are you from?",
    "Do you live in a house or an apartment?",
    "What do you usually do in the morning?",
    "What is your favorite food?",
    "Do you like to watch TV? What is your favorite show?",
    "What do you do on weekends?",
    "Do you have any brothers or sisters?"
]

part2_prompt = "Look at this picture. Can you describe what you see? (Imagine a picture of a family having a picnic in a park.)"
part2_followup = ["What are the people doing?", "How do you think they are feeling?"]

part3_questions = [
    "What is your favorite season? Why?",
    "Do you like to travel? Where did you go last?",
    "What do you usually do after school or work?",
    "Do you like to read books? What kind of books do you like?",
    "What is your favorite place in your city? Why?",
    "Do you like to cook? What can you cook?"
]

# Initialize session state
if "part" not in st.session_state:
    st.session_state.part = 1
    st.session_state.index = 0
    st.session_state.responses = []

# Title
st.title("A2-Level Speaking Exam Chatbot")

# Display questions and collect responses
if st.session_state.part == 1:
    question = part1_questions[st.session_state.index]
elif st.session_state.part == 2:
    question = part2_prompt if st.session_state.index == 0 else part2_followup[st.session_state.index - 1]
elif st.session_state.part == 3:
    question = part3_questions[st.session_state.index]
else:
    question = "Exam complete! Thank you for your responses."

st.write(f"**Examiner:** {question}")
user_response = st.text_input("Your response:")

if user_response:
    st.session_state.responses.append({"part": st.session_state.part, "question": question, "response": user_response})
    st.session_state.index += 1

    # Move to the next part if all questions are answered
    if st.session_state.part == 1 and st.session_state.index >= len(part1_questions):
        st.session_state.part = 2
        st.session_state.index = 0
    elif st.session_state.part == 2 and st.session_state.index >= len(part2_followup) + 1:
        st.session_state.part = 3
        st.session_state.index = 0
    elif st.session_state.part == 3 and st.session_state.index >= len(part3_questions):
        st.session_state.part = 4

# Display feedback
if st.session_state.responses:
    st.write("### Your Responses:")
    for i, response in enumerate(st.session_state.responses):
        st.write(f"**Question {i + 1}:** {response['question']}")
        st.write(f"**Your Answer:** {response['response']}")
        st.write("---")

# Get feedback using OpenAI
if st.button("Get Feedback"):
    feedback_prompt = "The student gave the following responses:\n"
    for response in st.session_state.responses:
        feedback_prompt += f"Question: {response['question']}\nAnswer: {response['response']}\n\n"
    feedback_prompt += "Provide brief feedback on their grammar, vocabulary, and fluency for an A2-level English learner."

    feedback = openai.Completion.create(
        engine="text-davinci-003",
        prompt=feedback_prompt,
        max_tokens=200
    )
    st.write("### Feedback:")
    st.write(feedback.choices[0].text.strip())
