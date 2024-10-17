import os
from src.data.io_handler import IOHandler
from src.utils.config import Config
from langchain_openai import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

class ModelTrainer:
    def __init__(self):
        self.config = Config()
        self.model = ChatOpenAI(api_key=self.config.get_openai_api_key(), temperature=0.7)
        self.embeddings = OpenAIEmbeddings(api_key=self.config.get_openai_api_key())
        self.vector_store = None

    def train(self):
        # Get the path to the project root directory
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        # Construct the path to the dataSource directory
        data_dir = os.path.join(project_root, 'dataSource')
        
        # Check if the directory exists
        if not os.path.exists(data_dir):
            raise FileNotFoundError(f"The dataSource directory does not exist: {data_dir}")
        
        # Load all CSV files from the dataSource directory
        csv_files = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith('.csv')]
        
        if not csv_files:
            raise FileNotFoundError(f"No CSV files found in the dataSource directory: {data_dir}")
        
        dataset = IOHandler.load_csv(csv_files)
        
        # Prepare the data for embedding
        texts = dataset['Control Description'].tolist()
        metadatas = dataset.to_dict('records')
        
        # Create and save the vector store
        self.vector_store = FAISS.from_texts(texts, self.embeddings, metadatas=metadatas)
        
        # Save the vector store
        vector_store_path = os.path.join(os.path.dirname(__file__), 'vector_store')
        self.vector_store.save_local(vector_store_path)

    # ... rest of the class remains the same
