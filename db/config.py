
import psycopg2
import psycopg2.extras

class DB:
    DB_NAME = "kwork_tg"
    DB_USER = "postgres"
    DB_PASSWORD = "1"
    DB_PORT = "5432"
    DB_HOST = "localhost"
    connect = psycopg2.connect(dbname=DB_NAME ,
                               user=DB_USER ,
                               port=DB_PORT ,
                               host=DB_HOST ,
                               password=DB_PASSWORD)
    cursor = connect.cursor(cursor_factory=psycopg2.extras.DictCursor)

class Manager(DB):
    def save(self) -> object:
        table_name = self.__class__.__name__.lower() + "s"
        cols = [col for col, val in self.__dict__.items() if not val == None]
        values = [val for col, val in self.__dict__.items() if not val == None]
        col_format = " , ".join(cols)
        value_format = " , ".join(["%s"]*len(cols))
        query = f"""
            insert into {table_name} ({col_format}) values ({value_format}) returning *
        """
        self.cursor.execute(query , values)
        self.connect.commit()
        data: list = self.cursor.fetchall()
        dict_data = self.get_dict_resultset(data)[0]
        return self.__class__(**dict_data)

    def get_dict_resultset(self , data):
        dict_result = []
        for row in data:
            dict_result.append(dict(row))
        return dict_result

    def delete(self) -> list[object]:
        table_name = self.__class__.__name__.lower() + "s"
        cols = [col for col, val in self.__dict__.items() if not val == None]
        values = [val for col, val in self.__dict__.items() if not val == None]
        condition_format = "" if not cols else "where " + " = %s and ".join(cols) + " = %s"
        query = f"""
            delete from {table_name} {condition_format} returning *
        """
        self.cursor.execute(query , values)
        self.connect.commit()
        data = self.cursor.fetchall()
        datas: list = self.get_dict_resultset(data)
        return_list = []
        if datas:
            for i in datas:
                return_list.append(self.__class__(**i))
            return return_list
        else:
            return []

    def update(self, **kwargs) -> object:
        table_name = self.__class__.__name__.lower() + "s"
        cols = [col for col, val in self.__dict__.items() if not val == None]
        values = [val for col, val in self.__dict__.items() if not val == None]
        set_cols = kwargs.keys()
        set_values = kwargs.values()
        condition_format = "" if not cols else "where " + " = %s and ".join(cols) + " = %s"
        set_format = " = %s , ".join(set_cols) + " = %s "
        query = f"""
            update {table_name} set {set_format} {condition_format} returning *
        """
        self.cursor.execute(query , list(set_values) + values)
        self.connect.commit()
        data = self.cursor.fetchall()
        datas: list = self.get_dict_resultset(data)
        return_list = []
        if datas:
            for i in datas:
                return_list.append(self.__class__(**i))
            return return_list
        else:
            return []

    def first(self , *args):
        cols_format = "*" if not args else " , ".join(args)
        table_name = self.__class__.__name__.lower() + "s"
        cols = [col for col, val in self.__dict__.items() if  val != None]
        values = [val for col, val in self.__dict__.items() if val != None]
        condition_format = "" if not cols else "where " + " = %s and ".join(cols) + " = %s"
        query = f"""
            select {cols_format} from {table_name} {condition_format}
        """
        self.cursor.execute(query , values)
        data = self.cursor.fetchall()
        dict_data = self.get_dict_resultset(data)
        if dict_data:
            dict_data = dict_data[0]
            return self.__class__(**dict_data)

    def objects(self , *args) -> list:
        cols_format = "*" if not args else " , ".join(args)
        table_name = self.__class__.__name__.lower() + "s"
        cols = [col for col, val in self.__dict__.items() if not val == None]
        values = [val for col, val in self.__dict__.items() if not val == None]
        condition_format = "" if not cols else "where " + " = %s and ".join(cols) + " = %s"
        query = f"""
                    select {cols_format} from {table_name} {condition_format}
                """
        self.cursor.execute(query, values)
        data = self.cursor.fetchall()
        datas : list = self.get_dict_resultset(data)
        return_list = []
        if datas:
            for i in datas:
                return_list.append(self.__class__(**i))
            return return_list

    def get_all(self , *args) -> list[dict]:
        cols_format = "*" if not args else " , ".join(args)
        table_name = self.__class__.__name__.lower() + "s"
        cols = [col for col, val in self.__dict__.items() if not val == None]
        values = [val for col, val in self.__dict__.items() if not val == None]
        condition_format = "" if not cols else "where " + " = %s and ".join(cols) + " = %s"
        query = f"""
                            select {cols_format} from {table_name} {condition_format}
                        """
        self.cursor.execute(query, values)
        data = self.cursor.fetchall()
        datas: list = self.get_dict_resultset(data)
        return datas