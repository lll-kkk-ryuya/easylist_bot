from llama_index import get_response_synthesizer, ServiceContext
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.llms import OpenAI
from llama_index.retrievers import VectorIndexRetriever
from llama_index.response_synthesizers import get_response_synthesizer
from Vectorengine.CreateOrGet_Index import VectorStoreManager

class VectorQueryEngineManager:
    def __init__(self, index, model="gpt-4", temperature=0.4, similarity_top_k=5):
        """
        Initializes the VectorQueryEngineManager.

        Args:
            index: The VectorStoreIndex object.
            model (str): The model name for OpenAI LLM. Default is "gpt-4".
            temperature (float): The temperature for OpenAI LLM. Default is 0.4.
            similarity_top_k (int): The number of top similar items to retrieve. Default is 5.
        """
        self.index = index
        self.model = model
        self.temperature = temperature
        self.similarity_top_k = similarity_top_k
        self.llm = OpenAI(model=self.model, temperature=self.temperature)
        self.service_context = ServiceContext.from_defaults(llm=self.llm)
        self.vector_retriever = None
        self.response_synthesizer = None
        self.vector_query_engine = None

    def initialize_vector_query_engine(self):
        """
        Initializes and sets up the VectorQueryEngine with the given parameters.

        Returns:
            RetrieverQueryEngine: The initialized RetrieverQueryEngine object.
        """
        self.vector_retriever = VectorIndexRetriever(index=self.index, similarity_top_k=self.similarity_top_k)
        self.response_synthesizer = get_response_synthesizer(service_context=self.service_context, streaming=True)
        self.vector_query_engine = RetrieverQueryEngine(
            retriever=self.vector_retriever,
            response_synthesizer=self.response_synthesizer,
        )

        return self.vector_query_engine

# Usage example
# manager = VectorQueryEngineManager(index)
# vector_query_engine = manager.initialize_vector_query_engine()
