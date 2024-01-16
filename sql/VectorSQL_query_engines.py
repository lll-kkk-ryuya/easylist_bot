import os

from sql.VectorSQL_query_engine import VectorSQL_query_engine

class VectorSQL_query_engines:
    def __init__(self, engine):
        self.engine = engine
        self.query_engines = {}

    def process_files(self, file_paths):
        for file_path in file_paths:
            table_name = os.path.splitext(os.path.basename(file_path))[0]
            table_query_engine = VectorSQL_query_engine(self.engine, table_name)
            self.query_engines[table_name] = table_query_engine

        return self.query_engines

# 使用例
# engine = ... # SQLエンジンの初期化
# processor = NLSQLProcessor(engine)
# file_paths = [...]
# query_engines = processor.process_files(file_paths)
