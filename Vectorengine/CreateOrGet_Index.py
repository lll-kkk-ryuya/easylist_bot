import chromadb
from llama_index import VectorStoreIndex, ServiceContext
from llama_index.vector_stores import ChromaVectorStore
from llama_index.storage.storage_context import StorageContext
from llama_index.embeddings import AdapterEmbeddingModel, resolve_embed_model

class VectorStoreMnager:
    def __init__(self, collection_name, embed_batch_size=64, path="chroma_no_metadata", embed_model_path):
        """
        Initializes a VectorStoreIndexInitializer object.

        Args:
            collection_name (str): The name of the collection.
            embed_batch_size (int): Batch size for the embedding model.
            path (str): Path where the data is stored.
            embed_model_path (str): Path to the embedding model.
        """
        self.collection_name = collection_name
        self.embed_batch_size = embed_batch_size
        self.path = path
        self.embed_model_path = embed_model_path
        self.db = chromadb.PersistentClient(path=self.path)
        self.base_embed_model = resolve_embed_model("local:BAAI/bge-small-en")
        self.embed_model = AdapterEmbeddingModel(self.base_embed_model, self.embed_model_path)

    def initialize_index(self, nodes=None):
        """
        Initializes and returns a VectorStoreIndex object for the specified collection.

        Args:
            nodes: The nodes to be indexed.

        Returns:
            VectorStoreIndex: The initialized VectorStoreIndex object.
        """
        try:
            chroma_collection = self.db.get_collection(self.collection_name)
            
            vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
            service_context = ServiceContext.from_defaults(embed_model=self.embed_model)
            
            index = VectorStoreIndex.from_vector_store(
                vector_store,
                service_context=service_context
            )
        except ValueError as e:
            print(f"エラーが発生しました: {e}")
            chroma_collection = self.db.get_or_create_collection(self.collection_name)

            # Initialize vector store and storage context
            vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
            storage_context = StorageContext.from_defaults(vector_store=vector_store)

            # Initialize service context
            service_context = Service_context.from_defaults(embed_model=self.embed_model)
            index = VectorStoreIndex(nodes=nodes, storage_context=storage_context, service_context=service_context)

        return index



    @staticmethod
    def process_nodes(nodes):
        for node in nodes:
            if 'entities' in node.metadata and isinstance(node.metadata['entities'], list):
                entities_str = ', '.join(node.metadata['entities'])
                node.metadata['entities'] = entities_str




# Usage example ,collection;　　文学部：bunngakubu1
# manager = VectorStoreManager()
# manager.process_nodes(uber_nodes)
# index = manager.initialize_vector_store_index("bunngakubu1", uber_nodes)
