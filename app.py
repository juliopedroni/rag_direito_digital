import os
import time
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

# 1. Carrega as variáveis de ambiente (.env)
load_dotenv()

print("1. A ler os ficheiros PDF das leis...")
caminho_pasta = "./documentos"
loader = PyPDFDirectoryLoader(caminho_pasta)
paginas = loader.load()
print(f"   -> Leitura concluída: {len(paginas)} páginas encontradas.")

print("\n2. A dividir o texto em chunks...")
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100,
    separators=["\n\n", "\n", " ", ""]
)
chunks = text_splitter.split_documents(paginas)
print(f"   -> Chunking concluído: {len(chunks)} chunks gerados.")

print("\n3. A criar Embeddings e a guardar no ChromaDB em lotes pequenos...")

embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
pasta_db = "./chroma_db"


tamanho_lote = 10
vector_store = None

for i in range(0, len(chunks), tamanho_lote):
    lote = chunks[i:i + tamanho_lote]
    num_lote = (i // tamanho_lote) + 1
    total_lotes = (len(chunks) + tamanho_lote - 1) // tamanho_lote
    
    print(f"   -> A processar lote {num_lote}/{total_lotes} ({len(lote)} chunks)...")
    
    if vector_store is None:
        vector_store = Chroma.from_documents(
            documents=lote,
            embedding=embeddings,
            persist_directory=pasta_db
        )
    else:
        vector_store.add_documents(lote)
    
    
    if i + tamanho_lote < len(chunks):
        print("      (Pausa de 20 segundos para respeitar a quota de 30k tokens/min...)")
        time.sleep(20)

print(f"\nSucesso total! Banco vetorial criado e guardado na pasta '{pasta_db}'.")