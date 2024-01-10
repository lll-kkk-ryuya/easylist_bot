#チャンクごとに分割した際に失われる情報を補うためのコード　　url;https://docs.llamaindex.ai/en/stable/examples/metadata_extraction/MetadataExtractionSEC.html



from llama_index import Document
from llama_index.node_parser import SimpleNodeParser
from llama_index.extractors import (
    SummaryExtractor,
    QuestionsAnsweredExtractor,
    TitleExtractor,
    KeywordExtractor,
    EntityExtractor,
    BaseExtractor,
)
from llama_index.text_splitter import TokenTextSplitter
from llama_index.llms import OpenAI

class DocumentProcessingPipeline:
    def __init__(self, llm_model="gpt-3.5-turbo", max_tokens=512, temperature=0.16):
        self.llm = OpenAI(temperature=temperature, model=llm_model, max_tokens=max_tokens)
        self.text_splitter = TokenTextSplitter(
            separator=" ", chunk_size=512, chunk_overlap=128
        )
        self.extractors = self._initialize_extractors()

    def _initialize_extractors(self):
        return [
            TitleExtractor(nodes=5, llm=self.llm),
            QuestionsAnsweredExtractor(questions=3, llm=self.llm),
            EntityExtractor(prediction_threshold=0.5),
            SummaryExtractor(summaries=["prev", "self"], "next"], llm=llm),
            KeywordExtractor(keywords=10, llm=self.llm),
            CustomExtractor(),
            MarvinMetadataExtractor(marvin_model=SportsSupplement, llm_model_string=llm_model) 
        ]

    def get_transformations(self):
        return [self.text_splitter] + self.extractors

# カスタム抽出器
class CustomExtractor(BaseExtractor):
    def extract(self, nodes):
        metadata_list = [
            {
                "custom": (
                    node.metadata.get("document_title", "")
                    + "\n"
                    + node.metadata.get("excerpt_keywords", "")
                )
            }
            for node in nodes
        ]
        return metadata_list

# 使用例
#pipeline = DocumentProcessingPipeline()
#transformations = pipeline.get_transformations()
