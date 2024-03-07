###################################
# This is an llm application.It allows a user to ask 
# a CSV file questions and to  retrieve answers through 
# a langchain  agent and OpenAI api.The application
# is running via streamlit  package in the  frontend.
####################################

from distutils.log import set_verbosity
import streamlit as st
import os
#from secret_key import open_api_key
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

#os.environ['OPENAI_API_KEY']=open_api_key
os.environ['OPENAI_API_KEY']=st.secrets=["open_api_key"]

st.set_page_config(
   page_title="POC Ai 📉 ",
   page_icon="📊")

#Initialize  DataFrame Agent parameters (llm, memory and PREFIX )
def agent_init(df):

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

  agent=create_pandas_dataframe_agent(
      llm, 
      df,
      prefix=PREFIX, 
      verbose=True, 
      agent_executor_kwargs={"memory": memory},
      input_variables=['df_head', 'input', 'agent_scratchpad', 'chat_history_buffer', 'chat_history_summary', 'chat_history_KG']
  )
      
  return agent
             
#Invoke the langhchain agent to run the query on the csv file
def answer_question(user_question,agent):

     if user_question is not None and user_question!='':
        response= agent.run(user_question)
        return response




def main():
    
 st.title('Ask Your CSV File Questions!')
 user_csv= st.file_uploader('Upload your CSV file please 📉',type="csv")#Upload  a csv file
 message=st.chat_message('assistent',avatar="😊")
 message.write('Ask your CSV file a question')

 if "chat_hist"  not in st.session_state:
     st.session_state.chat_hist=[]


 for message in st.session_state.chat_hist:
     with st.chat_message(message["role"]):
        st.markdown(message["content"])


 question=st.chat_input('Input question')
 if  user_csv is not None:
    df = pd.read_csv(user_csv) #Convert the csv file into a datafram in pandas
    if question:
      with st.chat_message("user"):
          st.session_state.chat_hist.append({"role":"user","content": question})
          st.markdown(question)
      agent=agent_init(df)
      response=answer_question(question,agent)
      with st.chat_message('assistent'):
          st.markdown(response)
      st.session_state.chat_hist.append({"role":"assistent","content": response})
     
 else:
    st.markdown('Please upload a CSV file ')
     
if __name__ == '__main__':
    main()

