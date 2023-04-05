import pymysql


# comp3334@rm-3nspho22o594ka0w4.mysql.rds.aliyuncs.com:3306【rm-3nspho22o594ka0w4】


class Link_Database:
    __variables: dict = {"host": "rm-3nspho22o594ka0w4.mysql.rds.aliyuncs.com",
                         "account": "comp3334_g11",
                         "password": "Comp3334",
                         "db_name": "comp3334",
                         "port": 3306,
                         "charset": "utf8"}

    def __init__(self) -> None:
        try:
            self.conn = pymysql.connect(
                host=self.__variables["host"], user=self.__variables["account"],
                password=self.__variables["password"], db=self.__variables["db_name"],
                port=self.__variables["port"], charset=self.__variables["charset"]
            )
            print("Successful link with database.")
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(f"Cannot link with database, error message {e}.")
            exit(0)

        return

    def re_define_parameter(self, variable: dict) -> bool:
        if not variable: return False
        for key, val in variable.items():
            if key in self.__variables.keys() and val is not None:
                self.__variables[key] = val
            else:
                print(f"Wrong parameter input, key {key}, val {val}")
        return True

    def return_cursor(self) -> pymysql.connect:
        return self.cursor


class Database_operation(Link_Database):

    cursor: pymysql.connect.cursor

    def __init__(self):
        super().__init__()
        self.cursor=self.return_cursor()

    def get_data(self):
        ...
    
    def insert_database(self):
        ...

    def retrieve_database(self):
        ...