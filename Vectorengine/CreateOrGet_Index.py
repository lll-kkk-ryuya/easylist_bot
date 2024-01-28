import chromadb
from llama_index import VectorStoreIndex, ServiceContext
from llama_index.vector_stores import ChromaVectorStore
from llama_index.storage.storage_context import StorageContext
from llama_index.embeddings import AdapterEmbeddingModel, resolve_embed_model

class VectorStoreManager:
    def __init__(self, collection_name, embed_batch_size=64, path="chroma_no_metadata", nodes=None):
        self.collection_name = collection_name
        self.embed_batch_size = embed_batch_size
        self.path = path
        self.nodes = nodes
        self.index = self.initialize_vector_store_index()

    def initialize_vector_store_index(self):
        db = chromadb.PersistentClient(path=self.path)
        base_embed_model = resolve_embed_model("local:BAAI/bge-small-en")
        embed_model = AdapterEmbeddingModel(base_embed_model, "embed_model/文学部model")

        try:
            chroma_collection = db.get_collection(self.collection_name)
            vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
            service_context = ServiceContext.from_defaults(embed_model=embed_model)

            return VectorStoreIndex.from_vector_store(vector_store, service_context=service_context)

        except ValueError as e:
            print(f"エラーが発生しました: {e}")
            chroma_collection = db.get_or_create_collection(self.collection_name)

            vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
            storage_context = StorageContext.from_defaults(vector_store=vector_store)
            service_context = ServiceContext.from_defaults(embed_model=embed_model)

            return VectorStoreIndex(nodes=self.nodes, storage_context=storage_context, service_context=service_context)

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
