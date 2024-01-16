#ベータ版
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy import insert
from llama_index.llms import OpenAI
from nlsql import SQLDatabase, NLSQLTableQueryEngine, PromptTemplate, ServiceContext, PromptType
from llama_index.indices.struct_store.sql_query import NLSQLTableQueryEngine,NLStructStoreQueryEngine,PGVectorSQLQueryEngine
from llama_index.indices.struct_store.sql import SQLStructStoreIndex
from llama_index import (VectorStoreIndex,SimpleDirectoryReader,ServiceContext,StorageContext,SQLDatabase,)
import openai

class VectorSQL_query_engine:
    def __init__(self, engine, table_name):
        self.engine = engine
        self.table_name = table_name
        self.llm = OpenAI(temperature=0, model="gpt-4")
        self.service_context = ServiceContext.from_defaults(llm=self.llm)
        self.sql_database = SQLDatabase(self.engine, include_tables=[self.table_name])
        self.template = (
            """\
Given an input question, first create a syntactically correct {dialect} \
query to run, then look at the results of the query and return the answer. \
You can order the results by a relevant column to return the most \
interesting examples in the database.

Pay attention to use only the column names that you can see in the schema \
description. Be careful to not query for columns that do not exist. \
Pay attention to which column is in which table. Also, qualify column names \
with the table name when needed.

IMPORTANT NOTE: you can use specialized pgvector syntax (`<->`) to do nearest \
neighbors/semantic search to a given vector from an embeddings column in the table. \
The embeddings value for a given row typically represents the semantic meaning of that row. \
The vector represents an embedding representation \
of the question, given below. Do NOT fill in the vector values directly, but rather specify a \
`[query_vector]` placeholder. For instance, some select statement examples below \
(the name of the embeddings column is `embedding`):
SELECT * FROM items ORDER BY embedding <-> '[query_vector]' LIMIT 5;
SELECT * FROM items WHERE id != 1 ORDER BY embedding <-> (SELECT embedding FROM items WHERE id = 1) LIMIT 5;
SELECT * FROM items WHERE embedding <-> '[query_vector]' < 5;

You are required to use the following format, \
each taking one line:

Question: Question here
SQLQuery: SQL Query to run
SQLResult: Result of the SQLQuery
Answer: Final answer here

Only use tables listed below.
{schema}


Question: {query_str}
SQLQuery: \
"""

        )
        self.text_to_sql_prompt = PromptTemplate(
            template=self.template,
            prompt_type=PromptType.TEXT_TO_SQL,
            #function_mappings={"roman_str": format_query_with_roman_numerals},
        )
        self.table_query_engine = VectorSQL_query_engine(
            sql_database=self.sql_database,
            text_to_sql_prompt=self.text_to_sql_prompt,
            tables=[self.table_name],
            service_context=self.service_context,
        )

    def get_query_engine(self):
        return self.table_query_engine
