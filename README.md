# Chatbot-on-Pi
**NOTE:This is an incomplete project.**

## Prerequisites
Python 3.8 or higher. 

## Setup
1. Clone the repository:
```bash
git clone https://github.com/rhfill/Chatbot-on-Pi.git
```

2. Install necessarry dependencies:
```bash
 python install -r requirements.txt
```

3. Download a llamafile model and run it on port 8080

   You can find the models at [https://github.com/Mozilla-Ocho/llamafile].
   For this example, assume you've downloaded `Meta-Llama-3-8B-Instruct.Q5_K_M.llamafile`. Make
   the llamafile executable with:
   ```bash
   chmod +x Meta-Llama-3-8B-Instruct.Q5_K_M.llamafile
   ```
   Then run the llamafile in server mode:
   ```bash
   ./Meta-Llama-3-8B-Instruct.Q5_K_M.llamafile --server --nobrowser --embedding --port 8080
   ```
4. Create Index & Create ChromaDB

   Run `create_db.py` to ingest documents into the database.
   ```bash
   cd llm/remote
   python create_db.py
   ```
   Before running the script, make sure t add the URLs you want to scrape to `llm/remote/urls.txt` in the following format:
   ```
   https://en.wikipedia.org/wiki/Elon_Musk
   https://en.wikipedia.org/wiki/SpaceX
   ```
   The script will prompt you to input the name of the collection.
5. Run Chat & Query Server

   ```bash
   python server.py
   ```
   The server will now run on port `8000`. Check out `llm/local/test.py` to see how to interact with the server.
