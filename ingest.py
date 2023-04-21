"""Load html from files, clean up, split, ingest into Weaviate."""
import os
import pickle
import sys
from dotenv import load_dotenv

from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import MarkdownTextSplitter
from langchain.vectorstores.faiss import FAISS

from github import GitHubRepoDownloader

def ingest_docs(user):
    load_dotenv()
    downloader = GitHubRepoDownloader(user, os.environ.get("GITHUB_API_KEY"))
    """Get documents from repositories."""
    files_text = downloader.get_all_starred_repo_markdown_files()
    for text in files_text:
        loader = UnstructuredMarkdownLoader(file_path=None, text=text)
        raw_documents = loader.load()
        
        text_splitter = MarkdownTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )
        documents = text_splitter.split_documents(raw_documents)
        print (documents)

        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.from_documents(documents, embeddings)
        # Save vectorstore
        with open("vectorstore.pkl", "wb") as f:
            pickle.dump(vectorstore, f)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        user = sys.argv[1]
        ingest_docs(user)
    else:
        print("Usage: ingest.py github-username")
