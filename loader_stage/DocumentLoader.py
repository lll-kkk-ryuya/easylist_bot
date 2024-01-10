import os
from llama_index import Document

class DocumentLoader:#metaデータ取得
    def __init__(self, directory):
        self.directory = directory

    def load_documents(self):
        documents = []
        for filename in os.listdir(self.directory):
            if filename.endswith(".txt"):
                file_path = os.path.join(self.directory, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    text = file.read()
                    # 拡張子を除去してカテゴリーを設定
                    category = os.path.splitext(filename)[0]
                    doc = Document(
                        text=text,
                        metadata={"filename": filename, "category": category}
                    )
                    documents.append(doc)
        return documents

# インスタンスの作成とドキュメントの読み込み　　　　使用方法
#document_loader = DocumentLoader('文学部2,3,4')
#documents = document_loader.load_documents()

# テスト出力（オプショナル）
#for doc in documents:
    #print(f"Filename: {doc.metadata['filename']}, Category: {doc.metadata['category']}, Text: {doc.text[:100]}...")
