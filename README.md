# CS336

### Stub

This is the program to put on your iLab.
Change the username

The psycopg2 package was not working with the default Python environment,
so I had to make a new one.

#### Creating environment
python3 -m venv ~/myenv

source ~/myenv/bin/activate

pip install --upgrade pip setuptools wheel

pip install psycopg pandas tabulate

### Tunnel

Change the username, location of environment, and location of the stub program

### database_llm.py

Change the file path to where you have phi-3.5-mini installed

Change the REMOTE_SCRIPT_PATH to where you have the stub program stored

Make sure to have the preliminary sql file stored in the same directory as database_llm.py

#README
===============================================================================================================
## Team Members
- Jake Kim (jgk98)
- Keith Andre Denila (ksd102) 
- Sean La Peruta (stl71)
- Hunter Nadolski (htn52)

## Contributions
**ilab_script.py**  
- jgk98 & stl71  

**database_llm.py**  
- jgk98 & stl71 & ksd102  

**SSH Tunnel Implementation**  
- jgk98 & stl71  

**Query Parsing**  
- ksd102  

**schema.sql**  
- ksd102  

**stub.py/tunnel.py extra credit**
- htn52

## Challenges & Interests
One challenge was the actual prompting of the llm to create an sql query using the user's question. 
It was difficult to find a consistant 'schema' to the llm response. Especially when it either cuts 
out randomly or just forgets semi-colons for no reason. Changing up the sql script for the schema sent
to the llm fixed most of the problems mostly. It is still very wishy washy with the responses at times.

Another challenge was the ssh tunnel. Especially when trying to make sure all the user interactions can come through
the tunnel and getting the output. As well as making sure that the actual script in the ilab was being used.

Something interesting was how closely tied the sql schema that was fed into the llm is to the actual response it gives.
We had to reduce the schema a bit from the actual sql script that created tables to form the actual db. Adding some comments
to portions that it was not correctly referencing also made it "understand" the schema of the db more.

### Extra Credit
Single point extra credit for stub.py/tunnel.py stdin implementation

### Transcripts
https://chatgpt.com/share/68193824-165c-800c-8ac8-874d5274dadf
https://chatgpt.com/share/6819683e-c828-8007-b020-250c1a0244a7

### Video
https://drive.google.com/file/d/1SR5ZQ7-vsBCHRx88KhehL5gR0-2IsDA_/view?usp=sharing