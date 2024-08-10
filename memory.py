import chromadb
from system import Environment
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


class Memory:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Memory, cls).__new__(cls)
            cls._instance._initialize(*args, **kwargs)
        return cls._instance

    def _initialize(self):

        # Initializing the chromaDB
        self.CHROMA_DB = chromadb.PersistentClient(path="./chroma")
        self.CHROMA_COLLECTION = self.CHROMA_DB.get_or_create_collection(
            name="Data",
            metadata={"hnsw:space": "cosine"}
        )
        Environment.logger.info("Memory initialized successfully")

        # Initializing the embedding model
        self.EMBED_MODEL_NAME = "intfloat/multilingual-e5-large"
        self.EMBED_MODEL = HuggingFaceEmbedding(
            model_name=self.EMBED_MODEL_NAME,
            text_instruction="",
            query_instruction="",
            cache_folder="./models/embedding_models/"+self.EMBED_MODEL_NAME,
        )
        Environment.logger.info("Embedding model initialized successfully")
    

    def queryFromDB(self, embedded_text, top_res, clause=None):
        ans = self.CHROMA_COLLECTION.query(
            query_embeddings=[embedded_text],
            n_results=top_res,
            include=["metadatas", "documents"],
            where=clause
        )
        return ans

    def saveToDB(self, curr_id, curr_metadata, curr_embeddings, curr_docs):
        self.CHROMA_COLLECTION.add(
            documents=[curr_docs],
            embeddings=[curr_embeddings],
            metadatas=[curr_metadata],
            ids=[curr_id]
        )
