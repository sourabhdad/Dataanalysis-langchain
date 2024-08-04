import streamlit as st
from langchain_experimental.agents import create_csv_agent
from langchain.llms import OpenAI
from dotenv import load_dotenv
import os

def main():
    load_dotenv()
    
    # Check for OpenAI API key
    if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
        st.error("OPENAI_API_KEY is not set. Please set it in your .env file.")
        st.stop()
    
    # Page configuration
    st.set_page_config(page_title="CSV Insight Wizard", page_icon="📊", layout="wide")
    
    # Sidebar
    st.sidebar.title("About")
    st.sidebar.info(
        "This app uses AI to analyze your CSV files. "
        "Upload a CSV and ask questions in natural language!"
    )
    
    # Main content
    st.title("CSV Insight Wizard 🧙‍♂️📊")
    st.markdown(
        "Unlock the power of your data with natural language queries!"
    )
    
    # File upload
    csv_file = st.file_uploader("Upload your CSV file", type="csv")
    
    if csv_file is not None:
        st.success("File successfully uploaded!")
        
        # Create agent
        agent = create_csv_agent(
            OpenAI(temperature=0), csv_file, verbose=True, allow_dangerous_code=True
        )
        
        # Query input
        user_question = st.text_input(
            "What would you like to know about your data?",
            placeholder="E.g., What's the average value in column X?"
        )
        
        if user_question:
            with st.spinner("🧙‍♂️ The wizard is analyzing your data..."):
                try:
                    answer = agent.run(user_question)
                    st.info("Here's what I found:")
                    st.write(answer)
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        
        # Display sample questions
        st.subheader("Not sure what to ask? Try these:")
        sample_questions = [
            "What are the column names in this CSV?",
            "How many rows are in this dataset?",
            "What's the highest value in column X?",
            "Show me a summary of the data."
        ]
        for question in sample_questions:
            if st.button(question):
                with st.spinner("🧙‍♂️ The wizard is analyzing your data..."):
                    try:
                        answer = agent.run(question)
                        st.info(f"Question: {question}")
                        st.write(answer)
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
