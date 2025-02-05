# -*- coding: utf-8 -*-
"""
Created on Sun Jul 16 19:01:37 2023

COVERLETTER
"""

import streamlit as st
from langchain.llms import OpenAI
from langchain import PromptTemplate
from trubrics.integrations.streamlit import FeedbackCollector

if "response" not in st.session_state:
    st.session_state["response"] = None

st.set_page_config(page_title="Cover Letter Generator")
st.title("Create Amazing Cover Letters")

st.sidebar.title("Get that dream job!")
#st.sidebar.markdown("[Sign up now](https://subscribepage.io/yJeBNL) to receive early access to additional AI tools")
st.sidebar.write("Powered by OpenAI, this app serves as your personal assistant to draft compelling cover letters for job applications. Simply copy and paste the job description and your resume into the respective text fields and press submit!") 

URL_STRING = "https://subscribepage.io/yJeBNL"
st.sidebar.markdown(
    f'<a href="{URL_STRING}" style="display: inline-block; padding: 12px 20px; background-color: #706dcb; color: white; text-align: center; text-decoration: none; font-size: 16px; border-radius: 4px;">Sign Up for early access to all our AI tools!</a>',
    unsafe_allow_html=True
)

#openai_api_key=st.secrets["openai"]["openai_api_key"]
openai_api_key=st.secrets.openai.openai_api_key

template = """
You are an expert in writing cover letters for job applicants.

Write a cover letter for the following job description in a professional tone

{job_description}

The cover letter should consist of two paragraphs.  The cover letter should start as follows:  Dear [Recipient's Name] I am writing to apply for the position of

Personalize with relevant experience and skills from the following description of the applicant:

{applicant_description}

"""

prompt = PromptTemplate(
    input_variables=["job_description", "applicant_description"],
    template=template
)


def generate_response(job_details, applicant_details):
  llm = OpenAI(model_name="gpt-3.5-turbo", temperature=0.7, openai_api_key=openai_api_key)
  finalPrompt = prompt.format(job_description=job_details, applicant_description=applicant_details)
  response = llm(finalPrompt)
  return response

collector = FeedbackCollector(
    component_name="evaluate_letter",
    email=st.secrets.trubrics.TRUBRICS_EMAIL, # Store your Trubrics credentials in st.secrets:
    password=st.secrets.trubrics.TRUBRICS_PASSWORD, # https://blog.streamlit.io/secrets-in-sharing-apps/
)

with st.form('my_form'):
  job_details = st.text_area('Paste the job description here, or write a few sentences about the role.','Role CEO X.AI. Lead the team whose goal is to understand the true nature of the universe.  Report directly to Elon.')
  applicant_details = st.text_area('Paste your resume here, or write a few sentences about yourself.','Bodybuilder, Conan, Terminator and former governor of of California.  I killed the Predator.') 
  submitted = st.form_submit_button('Submit')

if submitted and openai_api_key.startswith('sk-'):
    st.session_state["response"] = generate_response(job_details, applicant_details)

if st.session_state["response"]:
    st.info(st.session_state["response"])
    collector.st_feedback(
        feedback_type="thumbs",
        model="gpt3.5turbo",
        open_feedback_label="Any additional feedback?",
        metadata={"LLM response": st.session_state["response"], "job": job_details, "applicant": applicant_details},
        single_submit=False,
    )
