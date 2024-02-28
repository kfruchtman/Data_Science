In the folder  2 LLM Based AI apps:
The first app:
Ask_CSV_App.py - an app to ask your csv questions. It is using a lanchgain data frame agent.
The CSV app is working nice but has some issues. The agent is always running 
from the first question making the app work much slower (I couldn't find the solution for that)
Also tokens issues from openAi limitation.
It was not very easy to add memory buffer to remember chat history but I was able to do it finally.
The running frontend is Streamlit.(streamlit run Ask_CSV_App.py)


The second App:
Rag_App.py - a Retrival Augmented Generation technology to bring user data sources to query
an Ai and get Natural Language answers using LLM OpenAI api &Chorma db for embedding. 
This App is working fast and nice but has a bad frontend. I wanted to deploy it on a some kind of web interface.
I plan on doing  that in the near future.

Run it  in the terminal (python Rag_App.py "query_text")





To test the applications here are some optional questions  to use:

Questions for Rag App :
(TXT folder has 4 txt files: 2 for Obama speaches
, 1  text from a book named "breath" ,US vice president speach at  corona time )

"what Markdown editors  can use to try writing in Markdown?"
"What did the president say about Ketanji Brown Jackson"
"What the cynics fail to understand "
"how many females where in the titanic?"
"what is Obama saying about Joe Biden?"
"what is Obama saying about his girls Sasha and Malia?"
"we as a people will get there - what does he mean by that?"
"what is Tummo technique?"




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









