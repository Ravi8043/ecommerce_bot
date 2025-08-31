import os
from operator import itemgetter
from dotenv import load_dotenv
import traceback

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

# --- 0. Environment Setup ---
# Create a .env file in your project root and add your Google API key:
# GOOGLE_API_KEY="your_google_api_key_here"
load_dotenv()

# Check if the API key is set
if "GOOGLE_API_KEY" not in os.environ:
    raise ValueError("Google API key not found. Please set it in your .env file.")

# --- 1. Initialize Models ---
# Initialize the Google LLM and the embedding model.
# FIX: Updated the model name from "gemini-pro" to the correct, stable version "gemini-1.0-pro".
llm = ChatGoogleGenerativeAI(model="gemini-1.0-pro")
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# --- 2. RAG Setup: Vector Store and Retriever ---
# In this version, the documents are hardcoded.
faq_and_product_docs = [
    Document(page_content="Our return policy allows for returns within 30 days of purchase, provided the item is in its original condition.", metadata={"source": "faq"}),
    Document(page_content="To track your order, please use the tracking link sent to your email address after shipment.", metadata={"source": "faq"}),
    Document(page_content="We currently do not offer international shipping.", metadata={"source": "faq"}),
    Document(page_content="The 'QuantumLeap X1' smartwatch features a 72-hour battery life under normal usage.", metadata={"source": "product_docs"}),
    Document(page_content="The 'QuantumLeap X1' is water-resistant up to 5 atmospheres (50 meters).", metadata={"source": "product_docs"}),
    Document(page_content="Our customer support team is available 24/7 via the chat widget on our website.", metadata={"source": "faq"})
]

# Create the vector store from the documents
vectorstore = FAISS.from_documents(faq_and_product_docs, embeddings)
# The retriever will be used to fetch relevant documents
retriever = vectorstore.as_retriever(search_kwargs={"k": 2}) # Retrieve top 2 most relevant docs

# --- 3. Define Chains ---

# RAG Chain: This is the primary chain for answering questions.
rag_prompt_template = """
You are a helpful customer support assistant. Answer the user's question based only on the following context.
If the context does not contain the answer, say that you don't have enough information to answer. Do not make up information.

Context:
{context}

Question: {question}
"""
rag_prompt = ChatPromptTemplate.from_template(rag_prompt_template)

def format_docs(docs):
    """Helper function to format retrieved documents into a single string."""
    return "\n\n".join(doc.page_content for doc in docs)

# The main RAG pipeline
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | rag_prompt
    | llm
    | StrOutputParser()
)

# Fallback Chain: This chain is triggered if the RAG chain fails.
fallback_chain = RunnableLambda(
    lambda x: "I'm sorry, I'm having trouble finding an answer right now. Would you like to speak to a human agent?"
)

# Add the fallback mechanism to the main RAG chain.
rag_chain_with_fallback = rag_chain.with_fallbacks(fallbacks=[fallback_chain])

# Human Escalation Chain: A simple chain for when the user explicitly asks for a human.
human_escalation_chain = RunnableLambda(
    lambda x: "It sounds like you need to speak with a human. I am transferring you to an agent now."
)


# --- 4. Define the Router ---
# The router decides which chain to use based on the user's input.
def route(info):
    """
    Inspects the user's question for keywords to decide the routing path.
    """
    question = info.get("question", "").lower()
    # Keyword triggers for escalation
    if any(keyword in question for keyword in ["human", "agent", "person", "support"]):
        return human_escalation_chain
    else:
        return rag_chain_with_fallback

# The final chain combines the routing logic with the different response chains.
full_chain = RunnableLambda(route)


# --- 5. Run Examples (ADVANCED DEBUG MODE) ---
if __name__ == "__main__":
    print("Chatbot is ready. Running in ADVANCED DEBUG mode.")
    
    test_question = "What is the battery life of the QuantumLeap X1?"
    print(f"\n--- Testing with question: '{test_question}' ---")

    try:
        # Step 1: Test the retriever
        print("\n[DEBUG] Step 1: Retrieving documents...")
        retrieved_docs = retriever.invoke(test_question)
        if not retrieved_docs:
            print("[DEBUG] FAILED: Retriever returned no documents.")
        else:
            print(f"[DEBUG] SUCCESS: Retrieved {len(retrieved_docs)} documents.")
            for i, doc in enumerate(retrieved_docs):
                print(f"  - Doc {i+1}: {doc.page_content[:80]}...")
        
        # Step 2: Test the document formatter
        print("\n[DEBUG] Step 2: Formatting documents...")
        formatted_context = format_docs(retrieved_docs)
        print("[DEBUG] SUCCESS: Formatted context created.")
        # print(f"  - Context: {formatted_context}") # Uncomment for full context view

        # Step 3: Test the prompt
        print("\n[DEBUG] Step 3: Formatting the prompt...")
        prompt_input = {"context": formatted_context, "question": test_question}
        formatted_prompt = rag_prompt.invoke(prompt_input)
        print("[DEBUG] SUCCESS: Prompt formatted.")
        # print(f"  - Formatted Prompt: {formatted_prompt}") # Uncomment for full prompt view

        # Step 4: Test the LLM call directly
        print("\n[DEBUG] Step 4: Invoking the LLM...")
        llm_response = llm.invoke(formatted_prompt)
        print("[DEBUG] SUCCESS: LLM responded.")
        print(f"  - LLM Response: {llm_response.content}")

        # Step 5: Test the full RAG chain
        print("\n[DEBUG] Step 5: Testing the full RAG chain...")
        full_rag_response = rag_chain.invoke(test_question)
        print("[DEBUG] SUCCESS: Full RAG chain executed.")
        print(f"\n--- FINAL RESPONSE ---")
        print(f"User: {test_question}")
        print(f"Chatbot: {full_rag_response}")
        print(f"----------------------")

    except Exception as e:
        print(f"\n--- ERROR ---")
        print(f"An error occurred during the debug process: {e}")
        print("Full traceback:")
        traceback.print_exc()
        print(f"--- END ERROR ---\n")
