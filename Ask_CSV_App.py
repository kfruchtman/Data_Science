###################################
# This is an llm application.It allows a user to ask 
# a CSV file questions and to  retrieve answers through 
# a langchain  agent and OpenAI api.The application
# is running via streamlit  package in the  frontend.
####################################

import csv
from distutils.log import set_verbosity
import langchain
import streamlit as st
import os
import sys
from secret_key import open_api_key
os.environ['OPENAI_API_KEY']=open_api_key
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.agents import AgentExecutor, Tool, ZeroShotAgent,initialize_agent,load_tools
from langchain.memory import ConversationBufferMemory
from langchain.schema.language_model import BaseLanguageModel
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits.csv.base import create_csv_agent 
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
import pandas as pd
from langchain_openai import OpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.globals import set_verbose
from langchain.memory import ConversationBufferMemory,CombinedMemory,ConversationSummaryMemory,ConversationKGMemory
from langchain_openai import ChatOpenAI
import pandas as pd



st.set_page_config(
  page_title="Keren's Python Project Data Science 📉 ",
  page_icon="📊")

#Initialize  DataFrame Agent parameters 
def agent_init():
  llm=OpenAI(temperature=0.0)
  PREFIX = """
  You are working with a pandas dataframe in Python. The name of the dataframe is `df`.
  You should use the tools below to answer the question posed of you:

  Summary of the whole conversation:
  {chat_history_summary}

  Last few messages between you and user:
  {chat_history_buffer}

  Entities that the conversation is about:
  {chat_history_KG}
  """


  chat_history_buffer = ConversationBufferWindowMemory(
      k=5,
      memory_key="chat_history_buffer",
      input_key="input"
      )

  chat_history_summary = ConversationSummaryMemory(
      llm=llm, 
      memory_key="chat_history_summary",
      input_key="input"
      )

  chat_history_KG = ConversationKGMemory(
      llm=llm, 
      memory_key="chat_history_KG",
      input_key="input",
      )

  memory = CombinedMemory(memories=[chat_history_buffer, chat_history_summary, chat_history_KG])

  return llm,PREFIX,memory 





#Invoke the langhchain agent to run the query on the csv file
def answer_question(user_question,i,agent):

     if user_question is not None and user_question!='':
        response= agent.run(user_question)
        st.write(f'The answer to your question is {response}')
        alive_flag = st.radio("Keep querying your CSV file?", ('','Yes', 'No'),index=0,key=f'answer_question_{i}')
        return alive_flag # Flag -'Yes' to keep on questioning the CSV , 'No' to quit the app


def main():
    
  st.title('Ask Your CSV File Questions!')
  user_csv= st.file_uploader('Upload your CSV file please 📉',type="csv")#Upload  a csv file
   
  if  user_csv is not None:
   user_question=st.text_input("Ask a  question on the uploaded CSV file: ❓",key=f'question_0') 
   if user_question:
    i=1
    df = pd.read_csv(user_csv.name) #Convert the csv file into a datafram in pandas
    llm,PREFIX,memory=agent_init()
    agent = create_pandas_dataframe_agent(
    llm, 
    df,
    prefix=PREFIX, 
    verbose=True, 
    agent_executor_kwargs={"memory": memory},
    input_variables=['df_head', 'input', 'agent_scratchpad', 'chat_history_buffer', 'chat_history_summary', 'chat_history_KG']
)
    alive_flag=answer_question(user_question,i,agent) # keep_asking - a flag to know if to keep on asking or quit
    while alive_flag=="Yes":
                  try:
                    i+=1
                    user_question=st.text_input("Next question to CSV file: ❓",key=f'question_{i}') 
                    alive_flag=answer_question(user_question,i,agent)
                    if alive_flag=="No":
                        del agent 
                        break
                  except Exception as error:
                      st.write("An exception occurred:", error)
                  
    if alive_flag=="No":
       st.write('I hope you had fun! 😊  Bye 👋')                  

        
    

     
if __name__ == '__main__':
    main()

