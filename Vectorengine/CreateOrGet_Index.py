import chromadb
from llama_index import VectorStoreIndex, ServiceContext
from llama_index.vector_stores import ChromaVectorStore
from llama_index.storage.storage_context import StorageContext
from llama_index.embeddings import OpenAIEmbedding
from llama_index.embeddings import AdapterEmbeddingModel

class VectorStoreManager:
    def __init__(self, embed_batch_size=64, path="./chroma_no_metadata", embed_model=None):
        """
        Initializes the VectorStoreManager.

        Args:
            embed_batch_size (int): Batch size for the embedding model.
            path (str): Path where the data is stored.
            embed_model (optional): Custom embedding model to use. Defaults to OpenAIEmbedding if None.
        """
        self.embed_batch_size = embed_batch_size
        self.path = path
        self.db = chromadb.PersistentClient(path=self.path)
        self.base_embed_model = resolve_embed_model("local:BAAI/bge-small-en")
        self.embed_model = AdapterEmbeddingModel(base_embed_model, "embed_model/文学部model")

    def initialize_vector_store_index(self, collection_name, nodes=None):
        """
        Initializes and returns a VectorStoreIndex object for a given collection.
        If the collection does not exist, it creates a new one. If nodes are provided,
        it initializes the index with these nodes.

        Args:
            collection_name (str): The name of the collection.
            nodes (optional): The nodes to be indexed. Default is None.

        Returns:
            VectorStoreIndex: The initialized VectorStoreIndex object.
        """
        try:
            chroma_collection = self.db.get_collection(collection_name)
            vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
            service_context = ServiceContext.from_defaults(embed_model=self.embed_model)
            index = VectorStoreIndex.from_vector_store(
                vector_store,
                service_context=service_context
            )
        except ValueError as e:
            print(f"コレクションが見つかりませんでした。新しいコレクションを作成します: {e}")
            # Initialize vector store and storage context
            vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
            storage_context = StorageContext.from_defaults(vector_store=vector_store)

            # Initialize service context with the specified or default embedding model
            service_context = ServiceContext.from_defaults(embed_model=self.embed_model)
            index = VectorStoreIndex(nodes=nodes if nodes else [], storage_context=storage_context, service_context=service_context)

        return index

    @staticmethod
    def process_entities(nodes):
        # ... [process_entitiesメソッドの内容は変更なし] ...

# Usage example ,collection;　　文学部：bunngakubu1
# manager = VectorStoreManager()
# manager.process_entities(uber_nodes)
# index = manager.initialize_vector_store_index("bunngakubu1", uber_nodes)
