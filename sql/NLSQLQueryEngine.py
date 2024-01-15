
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy import insert
from llama_index.llms import OpenAI
from nlsql import SQLDatabase, NLSQLTableQueryEngine, PromptTemplate, ServiceContext, PromptType
from llama_index.indices.struct_store.sql_query import NLSQLTableQueryEngine,NLStructStoreQueryEngine,PGVectorSQLQueryEngine
from llama_index.indices.struct_store.sql import SQLStructStoreIndex
from llama_index import (VectorStoreIndex,SimpleDirectoryReader,ServiceContext,StorageContext,SQLDatabase,)
import openai

class NLSQLQueryEngine:
    def __init__(self, engine, table_name):
        self.engine = engine
        self.table_name = table_name
        self.llm = OpenAI(temperature=0, model="gpt-4")
        self.service_context = ServiceContext.from_defaults(llm=self.llm)
        self.sql_database = SQLDatabase(self.engine, include_tables=[self.table_name])
        self.template = (
            "Given an input question, first create a syntactically correct {dialect} "
            "query to run, then look at the results of the query and return the answer. "
            "You can order the results by a relevant column to return the most "
            "interesting examples in the database.\n\n"
"Never query for all the columns from a specific table, only ask for a "
"few relevant columns given the question.\n\n"
"Pay attention to use only the column names that you can see in the schema "
"description. Each column's description and usage are provided below. "
"Be careful to not query for columns that do not exist. "
"Pay attention to which column is in which table. "
"Also, qualify column names with the table name when needed. "
"When performing a search, use the LIKE clause with '%' wildcard for partial matching. "
"You are required to use the following format, each taking one line:\n\n"
"Question: Question here\n"
"SQLQuery: SQL Query to run\n"
"SQLResult: Result of the SQLQuery\n"
"Answer: Final answer here\n\n"
"Only use tables listed below with their respective columns and descriptions.\n"
"{schema}\n\n"
"Column Descriptions:\n"
"id: レコードの識別子。降順で並べられます。\n"
"campusName: 授業が開催されるキャンパス名 (例: 日吉、三田キャンパス)。\n"
"subjectName: 授業名。通常の授業に関する質問に使用します。必修科目など特定の状況を除き、こちらのカラムを優先的に使用してください。\n"
"academicFieldName: 総合教育科目や人文科学科目などの必修科目に関する質問に対して使用します\n"
"season: 授業が開催される学期 (春学期、秋学期、通年)。\n"
"dayOfWeekPeriod: 授業が開催される曜日と時間割。\n"
"locationName: 授業を担当する教授の名前。\n"
"lessonModeName: 授業の形式（対面授業かオンライン授業か）。\n"
"timetableYear: 授業が開催される年（西暦）。\n"
"faculties: 履修可能な学部（例: 商 - 商学部、経 - 経済学部、文 - 文学部、理 - 理工学部、法/政治 - 法学部政治学科、法/法律 - 法学部法律学科）。\n"
"entryNumber: 授業のID。\n"
"syllabusDetailUrl: 授業のシラバスのURL。\n\n"
"Question: {query_str}\n"
"SQLQuery: "
"Never query for all the columns from a specific table, only ask for a "
"few relevant columns given the question.\n\n"
"Pay attention to use only the column names that you can see in the schema "
"description. Each column's description and usage are provided below. "
"Be careful to not query for columns that do not exist. "
"Pay attention to which column is in which table. "
"Also, qualify column names with the table name when needed. "
"When performing a search, use the LIKE clause with '%' wildcard for partial matching. "
"If the search term in the LIKE clause includes numerical values within '% %', use the {roman_str} function to convert them to Roman numerals. This is important for ensuring the search query matches the database formatting. "
"You are required to use the following format, each taking one line:\n\n"
"Question: Question here\n"
"SQLQuery: SQL Query to run\n"
"SQLResult: Result of the SQLQuery\n"
"Answer: Final answer here\n\n"
"Only use tables listed below with their respective columns and descriptions.\n"
"{schema}\n\n"
"Column Descriptions:\n"
"id: レコードの識別子。降順で並べられます。\n"
"campusName: 授業が開催されるキャンパス名 (例: 日吉、三田キャンパス)。\n"
"subjectName: 授業名。通常の授業に関する質問に使用します。必修科目など特定の状況を除き、こちらのカラムを優先的に使用してください。\n"
"academicFieldName: 総合教育科目や人文科学科目などの必修科目に関する質問に対して使用します\n"
"season: 授業が開催される学期 (春学期、秋学期、通年)。\n"
"dayOfWeekPeriod: 授業が開催される曜日と時間割。\n"
"locationName: 授業を担当する教授の名前。\n"
"lessonModeName: 授業の形式（対面授業かオンライン授業か）。\n"
"timetableYear: 授業が開催される年（西暦）。\n"
"faculties: 履修可能な学部（例: 商 - 商学部、経 - 経済学部、文 - 文学部、理 - 理工学部、法/政治 - 法学部政治学科、法/法律 - 法学部法律学科）。\n"
"entryNumber: 授業のID。\n"
"syllabusDetailUrl: 授業のシラバスのURL。\n\n"
"Question: {query_str}\n"
"SQLQuery: "
        )
        self.text_to_sql_prompt = PromptTemplate(
            template=self.template,
            prompt_type=PromptType.TEXT_TO_SQL,
            #function_mappings={"roman_str": format_query_with_roman_numerals},
        )
        self.table_query_engine = NLSQLTableQueryEngine(
            sql_database=self.sql_database,
            text_to_sql_prompt=self.text_to_sql_prompt,
            tables=[self.table_name],
            service_context=self.service_context,
        )

    def get_query_engine(self):
        return self.table_query_engine

# 使用例
#query_engine = NLSQLQueryEngine(engine, "your_table_name")
#nlsql_table_query_engine = query_engine.get_query_engine()

