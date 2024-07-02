from langchain.document_loaders.csv_loader import CSVLoader
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


class Retriever:
    def __init__(self, source: str):
        self.source = source

    def get_context(self):
        return self.__vectorstore().as_retriever()

    def __vectorstore(self):
        loader = CSVLoader(self.source)
        docs = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)

        vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

        return vectorstore
