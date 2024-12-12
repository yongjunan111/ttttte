import joblib
import numpy as np

from dotenv import load_dotenv

from operator import itemgetter
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.retrievers import EnsembleRetriever

from . import template_llm
from .utils import reorder_documents


load_dotenv()

db_chroma = Chroma(
    collection_name="example_collection",
    embedding_function = OpenAIEmbeddings(model='text-embedding-3-small'),
    persist_directory= './save'
)

bm_retriever = joblib.load('./save/bm25_retriever_model.pkl')

retriever_chroma = db_chroma.as_retriever(search_kwargs={'k': 1})

ensemble_retriever = EnsembleRetriever(
        retrievers=[bm_retriever, retriever_chroma],
        weights=[0.5, 0.5]
    )
template = template_llm.template

prompt = PromptTemplate.from_template(template)

model = ChatOpenAI(model_name='gpt-4o-mini')

parser = StrOutputParser()

chain = (
    {
        'reference': itemgetter('question')
        | ensemble_retriever
        | RunnableLambda(reorder_documents),
        'question': itemgetter('question'),
        'language': itemgetter('language'),
    }
    | prompt
    | model
    | parser
)