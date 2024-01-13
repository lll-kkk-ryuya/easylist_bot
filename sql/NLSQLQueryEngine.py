
from sqlalchemy import create_engine
from nlsql import SQLDatabase, NLSQLTableQueryEngine, PromptTemplate, ServiceContext, PromptType
import openai

class NLSQLQueryEngine:
    def __init__(self, database_url, table_name, model="gpt-4", temperature=0):
        self.engine = create_engine(database_url)
        self.table_name = table_name
        self.llm = openai.OpenAI(temperature=temperature, model=model)
        self.service_context = ServiceContext.from_defaults(llm=self.llm)
        self.sql_database = SQLDatabase(self.engine, include_tables=[table_name])
        self.text_to_sql_prompt = PromptTemplate(
            template=f"SELECT * FROM {table_name}{{query_str}};",
            function_mappings={"query_str": self.format_query},
            prompt_type=PromptType.TEXT_TO_SQL,
        )
        self.table_query_engine = NLSQLTableQueryEngine(
            sql_database=self.sql_database,
            text_to_sql_prompt=self.text_to_sql_prompt,
            tables=[table_name],
            service_context=self.service_context,
        )

    def format_query(self, **kwargs):
        table_name = kwargs.get("table_name", self.table_name)
        query = f"SELECT * FROM {table_name}"
        conditions = []

        for key, value in kwargs.items():
            if key != "table_name":
                first_part = value.split(' ')[0]
                conditions.append(f"{key} LIKE '%{first_part}%'")

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        return query

# 使用例
#database_url = 'sqlite:///my_database.db'
#table_name = 'my_table'
#nlsql_engine = NLSQLQueryEngine(database_url, table_name)

# クエリの実行例
#query_str = "column_name: value"
#result = nlsql_engine.table_query_engine.execute(query_str)
#print(result)
```

