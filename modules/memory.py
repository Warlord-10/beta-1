import chromadb
import os
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext, VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.schema import Document
from llama_index.llms.groq import Groq
from modules.logger import MAIN_LOGGER


class KnowledgeBase:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(KnowledgeBase, cls).__new__(cls)
            cls._instance._initialize(*args, **kwargs)
        return cls._instance

    def _initialize(self):
        self.LLM = Groq(model="gemma2-9b-it", api_key=os.environ.get("GROQ_API"))
        # Initializing the embedding model
        # sentence-transformers/all-mpnet-base-v2
        # facebook/bart-base
        # BAAI/bge-base-en-v1.5
        self.EMBED_MODEL_NAME = "BAAI/bge-small-en-v1.5"
        self.EMBED_MODEL = HuggingFaceEmbedding(
            model_name=self.EMBED_MODEL_NAME,
            cache_folder="./models/embedding_models/"+self.EMBED_MODEL_NAME,
        )
        MAIN_LOGGER.info("Embedding model initialized successfully")


        # Initializing the chromaDB
        chroma_client = chromadb.PersistentClient(path="./chroma_storage")
        chroma_collection = chroma_client.get_or_create_collection(
            name="Data",
            metadata={"hnsw:space": "cosine"}
        )
        self.VECTOR_STORE = ChromaVectorStore(chroma_collection=chroma_collection)
        MAIN_LOGGER.info("Memory initialized successfully")

        # Creating the index
        self.INDEX = VectorStoreIndex.from_vector_store(
            vector_store=self.VECTOR_STORE, 
            embed_model=self.EMBED_MODEL,
            show_progress=True,
            persist_dir="./index_storage"
        )
        MAIN_LOGGER.info("Loaded existing index")
        
        # Creating the query engine
        self.QUERY_ENGINE = self.INDEX.as_query_engine(llm=self.LLM)
        MAIN_LOGGER.info("Knowledge base initialized successfully")
        

    def _getEmbeddings(self, text):
        return self.EMBED_MODEL.embed_query(text)
    
    def _getFileEmbeddings(self, file_path):
        return self.EMBED_MODEL.parse_file(file_path)

    def saveTextToMemory(self, text):
        try:
            doc = Document(text=text)
            self.INDEX.insert(doc)
            self.INDEX.storage_context.persist()
            return "Text saved."
        except:
            return "Error in saving text."

    def saveDocumentToMemory(self, file_path):
        try:
            docs = SimpleDirectoryReader(input_files=[file_path]).load_data(show_progress=True)
            for doc in docs:
                self.INDEX.insert(doc)
            self.INDEX.storage_context.persist()
            return "Document saved."
        except:
            return "Error in saving document."

    def clearMemory(self):
        try:
            self.VECTOR_STORE.clear()
            self.INDEX.storage_context.persist()
            return "Memory cleared."
        except:
            return "Error in clearing memory."
    
    def queryMemory(self, query):
        try:
            response = self.QUERY_ENGINE.query(query)
            return response
        except:
            return "Error in querying memory."
        

if __name__ == "__main__":
    MAIN_MEMORY = KnowledgeBase()
    while True:
        s = int(input("Option: "))
        if s==1:
            t = input("Text: ")
            MAIN_MEMORY.insertTextToKnowledgeBase(t)
        elif s==2:
            t = input("Query: ")
            print(MAIN_MEMORY.queryKnowledgeBase(t))
        elif s==3:
            break