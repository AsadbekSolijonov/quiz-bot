import os
import sqlite3
from abc import ABC, abstractmethod

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


class DatabaseConnect(ABC):
    def __init__(self):
        self.conn = sqlite3.connect(f'{CURRENT_DIR}/my_data.db')
        self.curr = self.conn.cursor()
        self.create_table()

    @abstractmethod
    def create_table(self):
        pass


class QuestionCategory(DatabaseConnect):

    def create_table(self):
        sql_query = """
        CREATE TABLE IF NOT EXISTS question_category (
        id INTEGER NOT NULL,
        category_name VARCHAR(50) NOT NULL,
        PRIMARY KEY (id AUTOINCREMENT));
        """
        with self.conn:
            self.curr.execute(sql_query)

    def objects_all(self):
        sql_query = """
        SELECT category_name FROM question_category;
        """
        datas = self.curr.execute(sql_query).fetchall()
        return datas


class Question(DatabaseConnect):
    def create_table(self):
        sql_query = """
        CREATE TABLE IF NOT EXISTS question (
        id INTEGER NOT NULL,
        question VARCHAR(300) NOT NULL,
        explanation VARCHAR(200) NOT NULL,
        category_id INTEGER NOT NULL ,
        FOREIGN KEY (category_id) REFERENCES question_category(id) ON DELETE SET NULL ON UPDATE CASCADE,
        PRIMARY KEY (id AUTOINCREMENT));
        """
        with self.conn:
            self.curr.execute(sql_query)

    def objects_all(self):
        sql_query = """
        SELECT id, question, explanation, category_id FROM question;
        """
        datas = self.curr.execute(sql_query).fetchall()
        return datas


class Answer(DatabaseConnect):
    def create_table(self):
        sql_query = """
        CREATE TABLE IF NOT EXISTS answer (
        id INTEGER NOT NULL,
        question_id INTEGER NOT NULL ,
        a VARCHAR(100) NOT NULL,
        b VARCHAR(100) NOT NULL,
        c VARCHAR(100) NOT NULL,
        correct INTEGER NOT NULL CHECK (correct >= 0 and correct <= 2),
        FOREIGN KEY (question_id) REFERENCES question(id) ON DELETE CASCADE ON UPDATE CASCADE,
        PRIMARY KEY (id AUTOINCREMENT));"""
        with self.conn:
            self.curr.execute(sql_query)

    def get(self, question_id):
        sql_query = f"""
        SELECT id,  question_id, a, b, c, correct FROM answer WHERE question_id={question_id}"""
        datas = self.curr.execute(sql_query).fetchone()
        return datas


if __name__ == "__main__":
    QuestionCategory()
    Question()
    Answer()
