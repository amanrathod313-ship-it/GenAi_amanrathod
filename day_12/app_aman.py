import streamlit as st
import os
from mistralai.client import Mistral
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("MISTRAL_API_KEY")

st.title("AI RESUME BUILDER")
st.write("Create a professional resume using AI!")

client = Mistral(api_key=api_key) if api_key else None

name = st.text_input("Enter your full name")
education = st.text_input("Enter your education")
skills = st.text_area("Enter your skills")
experience = st.text_area("Enter your work experience or projects")

job_role = st.selectbox(
    "Choose your target job role",
    [
        "Python Developer",
        "Web Developer",
        "Data Analyst",
        "AI/ML Engineer",
        "Software Engineer"
    ]
)

if st.button("Generate Resume"):

    if not name.strip():
        st.warning("Please enter your name.")

    elif not skills.strip():
        st.warning("Please enter your skills.")

    elif not api_key:
        st.error("MISTRAL_API_KEY is missing from your .env file.")

    else:
        st.subheader("Your AI-Generated Resume")

        try:
            with st.spinner("Creating your resume..."):

                response = client.chat.stream(
                    model="mistral-small-latest",
                    temperature=0.4,
                    messages=[
                        {
                            "role": "system",
                            "content": """
                            You are a professional resume writer.
                            Create a clear, ATS-friendly resume.
                            Use headings and bullet points.
                            Never invent qualifications, skills,
                            work experience, or achievements.
                            """
                        },
                        {
                            "role": "user",
                            "content": f"""
                            Create a professional resume using these details:

                            Name: {name}
                            Education: {education}
                            Skills: {skills}
                            Experience and Projects: {experience}
                            Target Job Role: {job_role}

                            Include:
                            1. Professional Summary
                            2. Technical Skills
                            3. Education
                            4. Work Experience or Projects
                            5. Relevant Career Highlights

                            Use only the information provided.
                            For missing details, do not make anything up.
                            """
                        }
                    ]
                )

                def token_stream():
                    for chunk in response:
                        content = chunk.data.choices[0].delta.content
                        if content:
                            yield content

                resume = st.write_stream(token_stream())

                st.download_button(
                    label="Download Resume",
                    data=resume,
                    file_name="my_resume.txt",
                    mime="text/plain"
                )

        except Exception as e:
            st.error(f"An error occurred: {e}")
