import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

print("Iniciando o Assistente de Direito Digital...")

embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

pasta_db = "./chroma_db"
vector_store = Chroma(
    persist_directory=pasta_db,
    embedding_function=embeddings
)

retriever = vector_store.as_retriever(search_kwargs={"k": 3})

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0  
)

template_prompt = """Você é um especialista em Direito Digital brasileiro (LGPD, Marco Civil da Internet e Crimes Cibernéticos).

Sua ÚNICA fonte de conhecimento são os textos abaixo. É ESTRITAMENTE PROIBIDO utilizar conhecimento externo ou da internet.
Se a resposta não estiver descrita no contexto fornecido, diga EXCLUSIVAMENTE: "Não encontrei essa informação nas leis consultadas."

Contexto recuperado das leis:
{context}

Pergunta do usuário: 
{question}

Resposta fundamentada:"""

prompt = ChatPromptTemplate.from_template(template_prompt)


def formatar_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | formatar_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

print(" -> Assistente pronto para responder perguntas!\n")
print("=" * 60)
print("Digite sua pergunta sobre LGPD, Marco Civil ou Crimes Cibernéticos.")
print("Digite 'sair' para encerrar o programa.")
print("=" * 60 + "\n")

while True:
    pergunta = input("\nSua Pergunta: ")
    if pergunta.lower().strip() in ["sair", "exit", "quit"]:
        print("\nEncerrando o assistente. Até logo!")
        break
        
    if not pergunta.strip():
        continue

    print("\nBuscando nas leis e gerando resposta...")
    try:
        resposta = rag_chain.invoke(pergunta)
        print("\nResposta do Gemini:")
        print(resposta)
        print("-" * 60)
    except Exception as e:
        print(f"\nErro ao processar resposta: {e}")