###################################
# This is an LLM application for user specific data 
# accomplished by  RAG (Retrieval Augmented Generation)  technology.
#The app is embedding  txt files to a vectorDB  and retrieves the answers  
# by using LLM with Ai models.
#Best used cases for  large amounts of data
####################################

from chunk import Chunk
from openai import embeddings
from secret_key1 import open_api_key
from langchain_community import document_loaders
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma 
from langchain_core.prompts import ChatPromptTemplate
import os
import shutil
import argparse



CHROMA_PATH='Chroma' #Path to embeddingDB on local PC 
file_path='C:\TXT' #Path to source files 
os.environ['OPENAI_API_KEY']=open_api_key #Key to OpenAI api account 

#Function to to load  and store the data 
def prepare_data():
   docs= load_documents() 
   chunks=split_text(docs)
   save_to_chroma(chunks)
  
#Text splitting into chunks for easy lookup
def split_text(documents: list[Document]):
 text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size=1000,
    chunk_overlap=500,
    length_function=len,
    is_separator_regex=False,
    add_start_index=True
)
 chunks=text_splitter.split_documents(documents)
 print(f'Split {len(documents)} into {len(chunks)} chunks') # Split info
 return chunks

      
#Document load
def load_documents():
  loader = DirectoryLoader(file_path, glob="*.txt")
  docs = loader.load()
  return docs 

#Vector store 
def save_to_chroma(chunks: list[Document]):
 if os.path.exists(CHROMA_PATH):
   shutil.rmtree(CHROMA_PATH) #Delete all data inside this path 
 try:
   db= Chroma.from_documents(chunks,OpenAIEmbeddings(),persist_directory=CHROMA_PATH) #Insert the embedded values to Vector DB
   db.persist() #Save 
   print(f'saved {len(chunks)} to {CHROMA_PATH})')
 except Exception as error:
    print("An exception occurred:", error) 

#Retrieve the data
def query_chroma(query_text):
   try:
    embedding_function=OpenAIEmbeddings()
    db=Chroma(persist_directory=CHROMA_PATH,embedding_function=embedding_function) #Initialize  the Vector-db 
    results=db.similarity_search_with_relevance_scores(query_text,k=3) #Check  for available 3  results optional chunks to answer the query
    if len(results)==0 or results[0][1]<0.7:
      print('Unable to find matching results')
    else:
      context_text= "\n\n--\n\n".join([doc.page_content for doc,score in results])
     
      #print(context_text)
      return context_text
   except Exception as error:
    print("An exception occurred:", error)

   
#Create AI prompts and and use ChatOpenAI model to get an answer
def answer_question(context_text,query_text):
    PROMPT_TEMPLATE="""  Answer the question based on the {context}
 -------
 Answer the question based on the above context : {query}
 
 """ 
    prompt_template=ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt=prompt_template.format(context=context_text,query=query_text)
    model= ChatOpenAI()
    #print(f'{prompt}\n')
    response_text=model.invoke(prompt)
    return response_text

def main():
   
 prepare_data() 
 parser=argparse.ArgumentParser()
 parser.add_argument("query_text",type=str,help="The Query")
 args=parser.parse_args()
 query_text=args.query_text
 context_text=query_chroma(query_text)
 response=answer_question(context_text,query_text)
 print (f' Question   {query_text}:  Answer  {response.content}')


 
if __name__ == '__main__':
    main()