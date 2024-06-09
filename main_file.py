import streamlit as st
import pickle
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
with open("question_response_pairs.pkl", "rb") as f:
    question_response_pairs = pickle.load(f)

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token.isalnum() and token not in stop_words]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return tokens

def get_best_response(user_input, question_response_pairs):
    user_tokens = preprocess_text(user_input)

    similarities = {}
    for question, response in question_response_pairs.items():
        question_tokens = preprocess_text(question)
        intersection = set(user_tokens) & set(question_tokens)
        union = set(user_tokens) | set(question_tokens)
        jaccard_similarity = len(intersection) / len(union)
        similarities[question] = jaccard_similarity

    best_question = max(similarities, key=similarities.get)

    return question_response_pairs[best_question]

st.title("Info Genie")

execute_program = st.sidebar.checkbox("Execute program")

if execute_program:
    st.write("Bot: Hello! I'm your chatbot. Ask me anything or say 'exit' to end the conversation.")

    user_input = st.text_input("You: ")

    if user_input.lower() == 'exit':
        st.write("Bot: Goodbye! Have a great day.")
    else:
        if user_input:  
            response = get_best_response(user_input, question_response_pairs)
            st.write("Bot:", response)
else:
    st.write("Program execution is currently disabled. Check the box to enable.")
