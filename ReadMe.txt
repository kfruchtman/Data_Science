In the folder  2 LLM Based AI apps:


Ver2.
Ask_CSV_ChatBox.py - 
This is the same as the  app I presented in class  but the agent is not starting from the beginning
 and answering plus I use the built in streamlit chatbox cool feature.Much better performance
plus it is  deployed in streamlit cloud:

Please run:

https://ask-csv-test.streamlit.app/




1.
Ver1.
Old Version that I presented in class.No need to check since Ver2 is updated much better.
Ask_CSV_App.py - an app to ask your csv questions. The main methods are from  lanchgain utilizing a  data-frame agent.
The app is running in a loop of question-answer method.
The agent has a  memory buffer for  chat history but sometimes he is giving funny answers.
The CSV app is working ok but has some issues and needs fine tuning. 
E.g - On each question the agent is starting from the beginning causing app work much slower and also 
there are tokens limitations  from openAi which needs to be addressed.
The  frontend of this app is Streamlit.

Run in the terminal : streamlit run Ask_CSV_App.py






2.
Rag_App.py - using Langchain and OpenAi to create a  "Retrieval Augmented Generation"  application
and  bring user specific data sources into the AI world.
The app is running  in 5 main phases:

1.Load Directory of your choice
2.Split Documents into chunks 
3.Load chunks embedded to VectorDb 
4.Query VectorDb for similarity on embedded data 
5.Ask AI llm model for final answer using prompts via langchain 

in this scenario I inserted to the chroma db the TXT directory  that contains  4 .txt files: 2 .txt of  Obama speaches
,1 txt from a book named "breath",1 txt of US vice president speach at corona time.
They all exist in the TXT folder for your convenience.
The  App is working fast and nice but still not deployed on a nice user-web interface.
I plan on doing  that in the near future.

Run  in the terminal :python Rag_App.py "your question"

Optional Questions for Ask CSV  App :

Keren GARMIN.csv :
what is my avg heart rate when running?
and when doing pilates?
what  was my longest run 
what  was my longest run (the file measures in km not in miles)
what is the avg delta between Max Hear rate and Avg Heart rate  on running activities?
how many running activitives  did I do  in year 2023?
can I have the answer  for all the questions  but for year 2022?
what is my avg cadence running activities only

Titanic.csv
how many females were in the titanic?
what was the avg age of the passengers?
how many survived ?
what is the female male ratio?

Optional Questions for Rag App :

"what Markdown editors  can use to try writing in Markdown?"
"What did the president say about Ketanji Brown Jackson"
"What the cynics fail to understand "
"how many females where in the titanic?"
"what is Obama saying about Joe Biden?"
"what is Obama saying about his girls Sasha and Malia?"
"we as a people will get there - what does he mean by that?"
"what is Tummo technique?"


Enjoy!!! 

*Both apps are using my Personal OpenAi api key.Inside the secret_key.py I insert the key and import to the apps.











