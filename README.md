# Chatbot-on-Pi
NOTE:This is an incomplete project.

## Prerequisites
Python 3.8 or higher. 

## Setup
1. Clone the repository:
```bash
git clone https://github.com/rhfill/Chatbot-on-Pi.git
```

2. Install dependencies:
```bash
 git clone https://github.com/rhfill/Chatbot-on-Pi.git
```

3. Download a llamafile model and run it on port 8080

   Link: [https://github.com/Mozilla-Ocho/llamafile]
   Assume you've downloaded `Meta-Llama-3-8B-Instruct.Q5_K_M.llamafile`, now you need to make
   the llamafile executable:
   ```bash
   chmod +x Meta-Llama-3-8B-Instruct.Q5_K_M.llamafile
   ```
   Then start the llamafile in server mode.  
   ```bash
   ./Meta-Llama-3-8B-Instruct.Q5_K_M.llamafile --server --nobrowser --embedding --port 8080
   ```
4. Create ChromaDB

   Run `create_db.py` to ingest documents into the system.
   ```bash
   python create_db.py
   ```
   Before running the script, you need to place the URLs you want to scrape under `llm/remote/urls.txt`
   The format should be like this:
   ```
   https://en.wikipedia.org/wiki/Elon_Musk
   https://en.wikipedia.org/wiki/SpaceX
   ```
   The script will ask you to input the name of the collection.
5. Run Chat & Query Server

   ```bash
   python server.py
   ```
   The server will now run on port `8000`. See `llm/local/test.py` to know how to interact with the server.
