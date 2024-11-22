from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from transformers import pipeline
import torch

class QAService:
    def __init__(self, pdf_text: str):
        """
        Initialize QA service for a specific document
        
        Args:
            pdf_text (str): Full text of the PDF
        """
        # Use a free, open-source embedding model
        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )
        
        # Text splitting for vector storage
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500, 
            chunk_overlap=100
        )
        texts = text_splitter.split_text(pdf_text)
        
        # Create vector store
        self.vectorstore = Chroma.from_texts(
            texts, 
            embedding=self.embeddings
        )
        
        # Question answering pipeline using free HuggingFace model
        self.qa_pipeline = pipeline(
            "question-answering",
            model="deepset/roberta-base-squad2",
            device=0 if torch.cuda.is_available() else -1
        )

    def answer_question(self, question: str) -> str:
        """
        Answer a question based on the document
        
        Args:
            question (str): User's question
        
        Returns:
            str: Generated answer
        """
        # Retrieve relevant context
        docs = self.vectorstore.similarity_search(question, k=3)
        context = " ".join([doc.page_content for doc in docs])
        
        # Generate answer
        result = self.qa_pipeline(question=question, context=context)
        return result['answer']