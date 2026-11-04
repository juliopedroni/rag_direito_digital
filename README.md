# 📜 Assistente Virtual de Direito Digital com RAG (LGPD, Marco Civil & Crimes Cibernéticos)

> Aplicação de IA Generativa construída com a arquitetura **RAG (Retrieval-Augmented Generation)** para consulta e interpretação precisa de legislações brasileiras de Direito Digital (LGPD, Marco Civil da Internet e Lei de Crimes Cibernéticos) sem alucinações.

---

## 🎯 Sobre o Projeto

Modelos de Linguagem (LLMs) genéricos costumam alucinar ou responder de forma imprecisa ao lidar com normas regulatórias e termos jurídicos específicos. 

Este projeto resolve esse problema implementando um pipeline de **RAG end-to-end** em Python. O assistente realiza buscas semânticas em uma base de dados vetorial alimentada com os textos oficiais das leis (obtidos no Portal do Planalto) e entrega ao **Google Gemini API** apenas os trechos estritamente relevantes para responder às perguntas do usuário com fundamentação legal direta.

---

## 💡 Principais Diferenciais e Desafios de Engenharia

- **Zero Alucinação (Strict Grounding):** Prompt Engineering projetado para forçar o modelo a responder exclusivamente com base no contexto recuperado das leis. Se o assunto não constar na base, a IA recusa a resposta.
- **Processamento em Lotes (Rate Limiting Handling):** Tratamento de limites de quota (*Free Tier*) da API do Gemini (tokens e requisições por minuto) via *batch processing* inteligente e *delays* assíncronos durante o embedding.
- **Busca Semântica vs. Busca por Palavra-Chave:** Utilização de vetores multidimensionais (`gemini-embedding-001`) no **ChromaDB** para capturar a intenção da pergunta do usuário, e não apenas correspondências exatas de palavras.
- **Persistência Local Eficiente:** Separação entre a etapa de ingestão/vetorização de dados (`app.py`) e a etapa de inferência/chat (`chat.py`), evitando consumo desnecessário de computação e API.

---

## 🛠️ Tecnologias Utilizadas

| Componente | Tecnologia | Função |
| :--- | :--- | :--- |
| **Linguagem** | Python 3.10+ | Linguagem base da aplicação |
| **Orquestração de IA** | LangChain / LCEL | Criação das cadeias de RAG e conectores |
| **Modelo LLM** | Google Gemini (`gemini-2.5-flash`) | Geração de respostas contextuais |
| **Modelo de Embedding** | `gemini-embedding-001` | Conversão de texto em vetores |
| **Vector Database** | ChromaDB | Banco vetorial local persistente |
| **Parsing de Documentos**| PyPDF / PyPDFDirectoryLoader | Leitura e extração de PDFs |
| **Ambiente & Chaves** | `python-dotenv` | Gestão segura de variáveis de ambiente |

---

## 🧠 Arquitetura da Solução

[ PDFs das Leis ] -> [ PyPDF Loader ] -> [ Text Splitter (Chunking) ]
|
v
[ Gemini Embedding API ]
|
v
[ Pergunta do Usuário ] -> [ ChromaDB (Busca Vetorial k=3) ]
|
v
[ Prompt RAG + Contexto das Leis ]
|
v
[ Gemini 2.5 Flash LLM ] -> [ Resposta Fundamentada ]

---

## ⚙️ Como Executar o Projeto

### 1. Pré-requisitos
- Python instalado (v3.10 ou superior)
- Chave de API do **Google AI Studio** ([Obter chave](https://aistudio.google.com/))

### 2. Clonar o repositório e configurar o ambiente
```bash
# Clorar o repositório
git clone [https://github.com/juliopedroni/rag_direito_digital.git](https://github.com/juliopedroni/rag_direito_digital.git)
cd rag_direito_digital

# Criar e ativar o ambiente virtual
python -m venv .venv
.\.venv\Scripts\activate   # No Windows (PowerShell)

# Instalar dependências
pip install langchain langchain-google-genai langchain-community pypdf chromadb python-dotenv

3. Configurar a Chave de API
Crie um arquivo .env na raiz do projeto com o seguinte conteúdo:

GEMINI_API_KEY=sua_chave_aqui

Garanta que os PDFs das leis estão salvos dentro da pasta ./documentos e rode:

python app.py

Executar o Chatbot Interativo

python chat.py


🧪 Exemplo de Uso

Sua Pergunta: O que é considerado dado pessoal sensível segundo a LGPD?

Buscando nas leis e gerando resposta...

Resposta do Gemini:
De acordo com a Lei Geral de Proteção de Dados (LGPD - Lei nº 13.709/2018), dado pessoal sensível é aquele relativo a:
- Origem racial ou étnica;
- Convicção religiosa ou opinião política;
- Filiação a sindicato ou a organização de caráter religioso, filosófico ou político;
- Dado referente à saúde ou à vida sexual;
- Dado genético ou biométrico, quando vinculado a uma pessoa natural.
------------------------------------------------------------

Sua Pergunta: Qual a receita de um bolo de cenoura?

Buscando nas leis e gerando resposta...

Resposta do Gemini:
Não encontrei essa informação nas leis consultadas.