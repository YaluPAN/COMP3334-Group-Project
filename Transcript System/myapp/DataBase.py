import hashlib
import time
import uuid
import pymysql
from Crypto.Cipher import AES
from Crypto import Random
import base64


class Link_Database:
    __variables: dict = {"host": "rm-3nspho22o594ka0w4ko.mysql.rds.aliyuncs.com",
                         "account": "comp3334_g11",
                         "password": "Comp3334",
                         "db_name": "comp3334",
                         "port": 3306,
                         "charset": "utf8"}

    __salt: dict= {"db_name":"salt",
                   "account": "qishihao01",
                   "password": "20011214Db#"
                   }
    __saltconn=None
    __saltcursor=None

    def __init__(self) -> None:
        retryCount, initCount=10, 0
        while initCount<retryCount:
            try:
                self.conn = pymysql.connect(
                    host=self.__variables["host"], user=self.__variables["account"],
                    password=self.__variables["password"], db=self.__variables["db_name"],
                    port=self.__variables["port"], charset=self.__variables["charset"]
                )
                print("Successful link with database.")
                self.cursor = self.conn.cursor()
                break
            except Exception as e:
                print(f"Cannot link with database, error message {e}.")
                initCount+=1

        if initCount>9: exit(0)

        return

    def __salt_conn(self):
        retryCount, initCount = 10, 0
        while initCount < retryCount:
            try:
                self.__saltconn = pymysql.connect(
                    host=self.__variables["host"], user=self.__salt["account"],
                    password=self.__salt["password"], db=self.__salt["db_name"],
                    port=self.__variables["port"], charset=self.__variables["charset"]
                )
                print("Successful link with salt database.")
                self.__saltcursor = self.conn.cursor()
                break
            except Exception as e:
                print(f"Cannot link with salt database, error message {e}.")
                initCount += 1

        if initCount > 9: exit(0)
        return

    def re_define_parameter(self, variable: dict) -> bool:
        if not variable: return False
        for key, val in variable.items():
            if key in self.__variables.keys() and val is not None:
                self.__variables[key] = val
            else:
                print(f"Wrong parameter input, key {key}, val {val}")
        return True

    def return_cursor(self):
        return self.cursor


class Database_operation(Link_Database):

    cursor: pymysql.connect.cursor
    bs=AES.block_size

    def __init__(self):
        super().__init__()
        self.cursor=self.return_cursor()
        self.__salt_conn()

    def get_data(self, user, account):
        sql="SELECT "
        ...

    def salt_generate(self):
        return uuid.uuid4().bytes

    def encrpyion_passowrd(self, pw: str, salt: bytes):
        pwencode=pw.encode("utf-8")
        xored=bytearray()
        for times in range(len(salt)):
            xored.append(salt[times]^pwencode[times%len(salt)])
        return hashlib.sha256(xored).hexdigest()

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    def AES_encryption(self, pw: str, salt):
        pw=self._pad(pw)
        cipher=AES.new(salt, AES.MODE_CBC)
        iv=Random.new().read(AES.block_size)
        cipher=AES.new(salt, AES.MODE_CBC, iv)
        return base64.b64encode(iv+cipher.encrypt(pw.encode()))

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

    def AES_decryption(self, enc, salt):
        dec=base64.b64decode(enc)
        iv=dec[:AES.block_size]
        cipher=AES.new(salt, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(dec[AES.block_size:])).decode('utf-8')


    def insert_database(self, user, password, hash=None)->bool:
        salt=self.salt_generate()

        sql="INSERT INTO `student_ACCOUNT` (`account name`, `password`) values (%s, %s);"
        values=(user, password)
        try:
            self.cursor.execute(sql, values)
            self.conn.commit()
            time.sleep(2)
        except Exception as e:
            print(f"Insert failed, error message {e}")
            return False
        return True

    def retrieve_database(self):
        ...


if __name__=="__main__":
    db=Database_operation()
    db.insert_database()

# SQL statement:
# Create a table to store user accounts and passwords
# c.execute('''CREATE TABLE IF NOT EXISTS users
#              (id integer primary key autoincrement, username text, password text)''')
#
# # Create a table to store the IPFS hashes
# c.execute('''CREATE TABLE IF NOT EXISTS ipfs_hashes
#              (id integer primary key autoincrement, user_id integer, hash text,
#               FOREIGN KEY (user_id) REFERENCES users (id))''')
# conn.commit()





