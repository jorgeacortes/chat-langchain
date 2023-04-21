"""Create a ChatVectorDBChain for question/answering."""
from langchain.callbacks.base import AsyncCallbackManager
from langchain.callbacks.tracers import LangChainTracer
from langchain.chains import ChatVectorDBChain, ConversationalRetrievalChain
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.base import CallbackManager
from langchain.chains.chat_vector_db.prompts import (CONDENSE_QUESTION_PROMPT,
                                                     QA_PROMPT)
from langchain.chains.llm import LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.vectorstores.base import VectorStore


def get_chain(
    vectorstore: VectorStore, question_handler, stream_handler, tracing: bool = False
) -> ChatVectorDBChain:
    """Create a ChatVectorDBChain for question/answering."""
    # Construct a ChatVectorDBChain with a streaming llm for combine docs
    # and a separate, non-streaming llm for question generation
    manager = AsyncCallbackManager([StreamingStdOutCallbackHandler()])
    if tracing:
        tracer = LangChainTracer()
        tracer.load_default_session()
        manager.add_handler(tracer)

    llm = OpenAI(temperature=0)
    streaming_llm = OpenAI(
        streaming=True,
        callback_manager=manager,
        verbose=True,
        temperature=0
    )

    question_generator = LLMChain(
        llm=llm,
        prompt=CONDENSE_QUESTION_PROMPT
    )
    doc_chain = load_qa_chain(streaming_llm, chain_type="stuff", prompt=QA_PROMPT, callback_manager=manager)

    qa = ConversationalRetrievalChain(
        retriever=vectorstore.as_retriever(),
        combine_docs_chain=doc_chain,
        question_generator=question_generator
    )
    return qa
