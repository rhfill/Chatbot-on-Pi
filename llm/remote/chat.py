from llama_index.core.llms import ChatMessage,MessageRole
from fastapi import FastAPI, HTTPException, APIRouter
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.llamafile import LlamafileEmbedding
from llama_index.llms.llamafile import Llamafile
from pydantic import BaseModel
from llama_index.core import VectorStoreIndex
import chromadb

router = APIRouter(prefix="/api/v1")
class ChatRequest(BaseModel):
    query: str
class QueryRequest(BaseModel):
    query: str

llm = Llamafile(temperature=0.5, seed=0)
embed_model = LlamafileEmbedding(base_url="http://localhost:8080")
query_engine = None
dialog = []

def initialize_chromadb(db_path, collection_name):
    db = chromadb.PersistentClient(path=db_path)
    try:
        col = db.get_collection(collection_name)
        return col
    except Exception as e:
        print(f"Error occured :{e}")
        raise

def set_system_prompt(role_prompt):
    messages = [
        ChatMessage(
            role=MessageRole.SYSTEM,
            content=role_prompt + "\n\n\n Limit each reply to no more than 50 words."
        )
    ]
    return messages

def initialize_query_settings():
    global query_engine
    db_path = './chromaDB'
    collection_name = input("Enter the ChromaDB collection name: ")
    # Initialize ChromaDB and Vector Store
    chroma_collection = initialize_chromadb(db_path, collection_name)
    vector_store = ChromaVectorStore(chroma_collection)
    # Initialize Vector Store Index
    index = VectorStoreIndex.from_vector_store(vector_store, embed_model=embed_model)
    # Initialize Query Engine
    query_engine = index.as_query_engine(llm=llm,verbose=True)

@router.post("/chat")
async def chat(request: ChatRequest):
    global dialog
    query = request.query
    if not query:
        raise HTTPException(status_code=400, detail="Query should not be empty.")

    dialog.append(ChatMessage(
        role=MessageRole.USER,
        content=query
    ))

    resp = llm.chat(dialog)
    msg = str(resp.message.content).replace("<|eot_id|>", "").strip()

    # Append the assistant's response to the dialog
    dialog.append(ChatMessage(
        role=MessageRole.ASSISTANT,
        content=msg
    ))
    return {"response": msg}

@router.post("/query")
async def query_system(request: QueryRequest):
    global query_engine

    if query_engine is None:
        raise HTTPException(status_code=500, detail="Query engine is not initialized.")

    resp = str(query_engine.query(request.query)).replace("<|eot_id|>", "").strip()
    return {"response": resp}

app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    role_prompt = input("Enter the roleplay prompt:")
    dialog = set_system_prompt(role_prompt)
    initialize_query_settings()
    uvicorn.run(app, host="0.0.0.0", port=8000)