import logging,requests

import chromadb
from llama_index.readers.web import SimpleWebPageReader
from llama_index.embeddings.llamafile import LlamafileEmbedding
from llama_index.core import SimpleDirectoryReader,StorageContext, VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.node_parser import SentenceSplitter

class DataReader:
    def __init__(self, file_path, url_path):
        self.file_path = file_path
        self.url_path = url_path

    def _is_valid_url(self, url):
        try:
            response = requests.head(url, timeout=3)
            return True
        except requests.RequestException:
            return False

    def read_data_from_file(self):
        logging.info("Reading data from directory: %s", self.file_path)
        file_reader = SimpleDirectoryReader(input_files=self.file_path)
        return file_reader.load_data(show_progress=True)

    def read_data_from_web(self, url):
        logging.info(f"Reading data from url: {url}")
        web_reader = SimpleWebPageReader(html_to_text=True)
        return web_reader.load_data(url)

    def read_urls_from_file(self):
        urls = []
        try:
            with open(self.url_path, 'r') as file:
                for line in file:
                    url = line.strip()
                    if url and self._is_valid_url(url):
                        urls.append(url)
                    else:
                        print(f"Invalid URL found in file: {url}")
        except FileNotFoundError:
            print(f"File {self.url_path} not found.")
        return urls
    def parse_data(self, data):
        logging.info("Parsing data")
        node_parser = SentenceSplitter(
            chunk_size=256,
            chunk_overlap=10,
            separator=" ",
            paragraph_separator="\n\n\n",
            secondary_chunking_regex="[^,.;。]+[,.;。]?"
        )
        return node_parser.get_nodes_from_documents(data)

class DatabaseManager:
    def __init__(self, db_path, collection_name):
        self.db_path = db_path
        self.collection_name = collection_name
    def init_db(self):
        logging.info("Initializing the database at path: %s", self.db_path)
        db = chromadb.PersistentClient(path = self.db_path)
        return db.get_or_create_collection(self.collection_name)

class VectorIndexer:
    def __init__(self, nodes, vector_store, embedding_model):
        self.nodes = nodes
        self.vector_store = vector_store
        self.embedding_model = embedding_model

    def create_index(self):
        logging.info("Creating the vector index")
        storage_context = StorageContext.from_defaults(vector_store=self.vector_store)
        return VectorStoreIndex(
            nodes=self.nodes, storage_context=storage_context,embed_model=self.embedding_model, show_progress=True
        )

def main():
    logging.getLogger().setLevel(logging.INFO)
    file_path = './files'
    url_path = './urls.txt'
    db_path = './chromaDB'
    collection_name = input("Enter the database collection name: ")

    # Reading Data
    all_docs = []
    data_reader = DataReader(file_path, url_path)
    # all_docs.extend(data_reader.read_data_from_file())
    urls = data_reader.read_urls_from_file()
    all_docs.extend(data_reader.read_data_from_web(urls))
    doc_nodes = data_reader.parse_data(all_docs)

    # Database Initialization
    db_manager = DatabaseManager(db_path=db_path, collection_name=collection_name)
    db_collection = db_manager.init_db()

    # Initializing Embedding Model
    model = LlamafileEmbedding(base_url="http://localhost:8080",
                               temperature = 0,seed = 0)

    # Creating Vector Index
    vector_store = ChromaVectorStore(chroma_collection=db_collection)
    indexer = VectorIndexer(nodes=doc_nodes, vector_store=vector_store, embedding_model=model)
    index = indexer.create_index()


if __name__ == "__main__":
    main()