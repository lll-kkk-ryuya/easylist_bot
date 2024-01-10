from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, insert
from sqlalchemy.exc import NoSuchTableError
import pandas as pd

class DatabaseManager:
    def __init__(self, db_url, echo=False):
        self.engine = create_engine(db_url, echo=echo)
        self.metadata_obj = MetaData(self.engine)

    def create_table(self, table_name):
        # 既存のテーブルを削除
        try:
            old_table = Table(table_name, self.metadata_obj, autoload_with=self.engine)
            old_table.drop(self.engine)
        except NoSuchTableError:
            print(f"テーブル '{table_name}' は存在しません。新規作成します。")
        
        # 新しいテーブルの定義
        new_table = Table(
            table_name,
            self.metadata_obj,
            Column("id", Integer, primary_key=True),
            Column("campusName", String(32)),
            Column("academicFieldName", String(64)),
            Column("season", String(32)),
            Column("subjectName", String(64)),
            Column("dayOfWeekPeriod", String(32)),
            Column("locationName", String(32)),
            Column("lessonModeName", String(32)),
            Column("timetableYear", String(32)),
            Column("faculties", String(64)),
            Column("entryNumber", String(32)),
            Column("syllabusDetailUrl", String(64)),
            extend_existing=True
        )

        # テーブルの作成
        self.metadata_obj.create_all(self.engine)

        # メタデータをデータベースの現在の状態に同期
        self.metadata_obj.reflect()

        return new_table

    def insert_data(self, df, table_name):
        # テーブルオブジェクトの取得
        table = Table(table_name, self.metadata_obj, autoload=True, autoload_with=self.engine)

        # データを行のリストに変換
        rows = df.to_dict(orient='records')

        # データベースにデータを挿入
        with self.engine.begin() as connection:
            for row in rows:
                stmt = insert(table).values(**row)
                connection.execute(stmt)

# 使用例
#db_manager = DatabaseManager('sqlite:///example.db', echo=True)
#table = db_manager.create_table('your_table_name')
#df = pd.DataFrame(...)  # Pandas DataFrame
#db_manager.insert_data(df, 'your_table_name')
