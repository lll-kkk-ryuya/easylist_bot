import chromadb
from llama_index import VectorStoreIndex, ServiceContext
from llama_index.vector_stores import ChromaVectorStore
from llama_index.storage.storage_context import StorageContext
from llama_index.embeddings import OpenAIEmbedding

#既存のコレクションの有無を特定して生成するかどうかを決定したのちにindexを取得する。
class VectorStoreManager:
    def __init__(self, embed_batch_size=64, path="./chroma_no_metadata"):
        """
        Initializes the VectorStoreManager.

        Args:
            embed_batch_size (int): Batch size for the embedding model.
            path (str): Path where the data is stored.
        """
        self.embed_batch_size = embed_batch_size
        self.path = path
        self.db = chromadb.PersistentClient(path=self.path)

    def initialize_vector_store_index(self, nodes, collection_name):
        """
        Initializes and returns a VectorStoreIndex object for a given collection.
        If the collection does not exist, it creates a new one.

        Args:
            nodes: The nodes to be indexed.
            collection_name (str): The name of the collection.

        Returns:
            VectorStoreIndex: The initialized VectorStoreIndex object.
        """
        try:
            chroma_collection = self.db.get_collection(collection_name)
            vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
            index = VectorStoreIndex.from_vector_store(vector_store)
            # Perform operations on the collection here
        except ValueError as e:
            print(f"エラーが発生しました: {e}")
            embed_model = OpenAIEmbedding(embed_batch_size=self.embed_batch_size)
            chroma_collection = self.db.get_or_create_collection(collection_name)

            # Initialize vector store and storage context
            vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
            storage_context = StorageContext.from_defaults(vector_store=vector_store)

            # Initialize service context
            service_context = ServiceContext.from_defaults(embed_model=embed_model)
            index = VectorStoreIndex(nodes=nodes, storage_context=storage_context, service_context=service_context)

        return index

#エラーを回避するためにノードに対して下記の操作を必要とする場合がある
    @staticmethod
    def process_entities(nodes):
        """
        Processes the 'entities' key in node metadata.

        Args:
            nodes: List of nodes to be processed.
        """
        for node in nodes:
            if 'entities' in node.metadata and isinstance(node.metadata['entities'], list):
                entities_str = ', '.join(node.metadata['entities'])
                node.metadata['entities'] = entities_str

# Usage example
#manager = VectorStoreManager()
#index = manager.initialize_vector_store_index(uber_nodes, "bunngakubu1")
#エラーの回避👇
#manager.process_entities(uber_nodes)
