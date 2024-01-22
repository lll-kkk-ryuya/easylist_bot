from llama_index.node_parser import SimpleNodeParser
from llama_index.finetuning import (
    generate_qa_embedding_pairs,
    EmbeddingQAFinetuneDataset,
    EmbeddingAdapterFinetuneEngine
)
from llama_index.llms import OpenAI
from llama_index.embeddings import resolve_embed_model
import torch
import json

class Finetune_Embed_Model:
    def __init__(self, model_output_path="model_output_test"):
        self.model_output_path = model_output_path

    def finetune(self, documents):
        parser = SimpleNodeParser.from_defaults()
        nodes = parser.get_nodes_from_documents(documents)

        llm = OpenAI(temperature=0, model="gpt-3.5-turbo")
        train_dataset = generate_qa_embedding_pairs(nodes, llm, num_questions_per_chunk=4)

        train_dataset.save_json("train_dataset.json")
        train_dataset = EmbeddingQAFinetuneDataset.from_json("train_dataset.json")

        base_embed_model = resolve_embed_model("local:BAAI/bge-small-en")

        finetune_engine = EmbeddingAdapterFinetuneEngine(
            train_dataset,
            base_embed_model,
            model_output_path=self.model_output_path,
            epochs=4,
            verbose=True
        )

        finetune_engine.finetune()
        return finetune_engine.get_finetuned_model()

# 使用例
#finetuner = EmbedModelFinetuner(model_output_path="my_model_output")
#documents = [...]  # ここにドキュメントのリストを設定
#finetuned_model = finetuner.finetune(documents)
