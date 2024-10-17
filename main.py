from src.data.io_handler import IOHandler
from src.utils.config import Config
from langchain_openai import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import os

class ModelTrainer:
    def __init__(self):
        self.config = Config()
        self.model = ChatOpenAI(api_key=self.config.get_openai_api_key(), temperature=0.7)
        self.embeddings = OpenAIEmbeddings(api_key=self.config.get_openai_api_key())
        self.vector_store = None

    def train(self):
        # Load all CSV files from the dataSource directory
        data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dataSource')
        csv_files = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith('.csv')]
        
        dataset = IOHandler.load_csv(csv_files)
        
        # Prepare the data for embedding
        texts = dataset['Control Description'].tolist()
        metadatas = dataset.to_dict('records')
        
        # Create and save the vector store
        self.vector_store = FAISS.from_texts(texts, self.embeddings, metadatas=metadatas)
        
        # Save the vector store
        vector_store_path = os.path.join(os.path.dirname(__file__), 'vector_store')
        self.vector_store.save_local(vector_store_path)

    def load_trained_model(self):
        vector_store_path = os.path.join(os.path.dirname(__file__), 'vector_store')
        if os.path.exists(vector_store_path):
            self.vector_store = FAISS.load_local(vector_store_path, self.embeddings)
        else:
            raise FileNotFoundError("Trained model not found. Please run the training process first.")

    def get_vector_store(self):
        if self.vector_store is None:
            self.load_trained_model()
        return self.vector_store
