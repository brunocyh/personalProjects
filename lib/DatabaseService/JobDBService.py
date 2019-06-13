from abc import ABC, abstractmethod
import sqlite3

"""
If we want to expand this service, we might need to consider using command design pattern. Dont really know how i can impl yet.
"""


class IJobDatabase(ABC):
    @staticmethod
    def instantiate_Database(): pass

    @abstractmethod
    def connect(self): pass

    @abstractmethod
    def disconnect(self): pass

    @abstractmethod
    def commit(self): pass

    @abstractmethod
    def reset_table(self): pass

    @abstractmethod
    def create_data(self): pass

    @abstractmethod
    def read_all_data(self, columns): pass

    @abstractmethod
    def update_analysed_data(self): pass

    @abstractmethod
    def delete_data(self): pass


class JobDatabase(IJobDatabase):

    __instance = None
    conn = None
    cursor = None
    db_name = "Database/Job.db"
    table_name = "job_table"

    @staticmethod
    def instantiate_Database() -> IJobDatabase:
        if JobDatabase.__instance == None:
            JobDatabase()
        return JobDatabase.__instance

    def __init__(self):
        # singleton
        if JobDatabase.__instance != None:
            raise Exception('DB is a singleton obejct')

        else:
            JobDatabase.__instance = self

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return True

    def disconnect(self):
        self.conn.commit()
        self.conn.close()
        return True

    def commit(self):
        self.conn.commit()
        return True

    def reset_table(self):
        cmd = []
        cmd.append("DROP TABLE IF EXISTS {};".format(self.table_name))
        cmd.append("CREATE TABLE {} (Page text, Job_title text, Company text, Location text, Search_eng text,\
            Term text, URL text, Words_of_concern text)".format(self.table_name))
        
        [self.cursor.execute(c) for c in cmd]
        return True

    def _sql(self, sql):
        return self.cursor.execute(sql)

    def create_data(self, key_pair: dict):
        try:
            cmd = "INSERT INTO {} VALUES ('{}','{}','{}','{}','{}','{}','{}','{}')".format(self.table_name,
                                                                                           key_pair['Page'],
                                                                                           key_pair['Job_title'],
                                                                                           key_pair['Company'],
                                                                                           key_pair['Location'],
                                                                                           key_pair['Search_eng'],
                                                                                           key_pair['Term'],
                                                                                           key_pair['URL'],
                                                                                           key_pair['Words_of_concern'])
            self.cursor.execute(cmd)
            return True

        except Exception as e:
            raise e

    def read_all_data(self, columns: "list of strings") -> "iterator":
        try:
            columns_str = ""
            for counter, word in enumerate(columns):
                if counter >= 1:
                    columns_str = columns_str + ", " + word
                
                else:
                    columns_str = word
                    

            cmd = "SELECT {} FROM {}".format(columns_str, self.table_name)
            print(cmd)
            return self.cursor.execute(cmd)

        except Exception as e:
            raise e

    def update_analysed_data(self, conditions: tuple, key_pair: tuple):
        try:
            cmd = "UPDATE {} SET {} = '{}' WHERE {} = '{}';".format(self.table_name,
                                                                    conditions[0],
                                                                    conditions[1],
                                                                    key_pair[0],
                                                                    key_pair[1])
            self.cursor.execute(cmd)
            return True

        except Exception as e:
            raise e

    def delete_data(self):
        # TODO: Further development
        raise Exception('Not implemented error')