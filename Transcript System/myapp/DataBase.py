import hashlib
import time
import uuid
import warnings

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

    __salt: dict = {"db_name": "salt",
                    "account": "qishihao01",
                    "password": "20011214Db#"
                    }
    _saltconn = None
    _saltcursor = None

    def __init__(self) -> None:
        retryCount, initCount = 10, 0
        while initCount < retryCount:
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
                initCount += 1

        if initCount > 9: exit(0)

        return

    def _salt_conn(self):
        retryCount, initCount = 10, 0
        while initCount < retryCount:
            try:
                self._saltconn = pymysql.connect(
                    host=self.__variables["host"], user=self.__salt["account"],
                    password=self.__salt["password"], db=self.__salt["db_name"],
                    port=self.__variables["port"], charset=self.__variables["charset"]
                )
                print("Successful link with salt database.")
                self._saltcursor = self._saltconn.cursor()
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
    bs = AES.block_size

    update_standard: dict = {
        "student_account": {"pw": "`password`", "hashes": "`hashes`", "name": "`name`"},
        "admin": {"pw": "`password`"}
    }

    def __init__(self):
        super().__init__()
        self.cursor = self.return_cursor()
        self._salt_conn()

    def get_user_data(self, account, table="student_account"):
        sql = '''SELECT *FROM `user` LEFT JOIN `user_property` ON
        `user`.account = `user_property`.account
        LEFT JOIN `book_on_sell` ON
        `user`.account = `book_on_sell`.account
        WHERE `user`.account = %s;'''

        try:
            self.cursor.execute(sql, (account,))
            results = self.cursor.fetchall()
        except Exception as e:
            print(f"Exception message is {e}")
            return False

        return results

    def get_book_data(self, bookname: str):
        sql = '''SELECT *FROM`books` LEFT JOIN `user_property` ON
        `books`.book_name = `user_property`.owned_book
        LEFT JOIN `book_on_sell` ON
        `books`.book_name = `book_on_sell`.shared_book
        WHERE `books`.book_name = %s;'''
        try:
            self.cursor.execute(sql, (bookname,))
            results = self.cursor.fetchall()
        except Exception as e:
            print(f"Exception message is {e}")
            return False

        return results


    def salt_encode(self, salt: bytes):
        return salt.decode("iso-8859-1")

    def salt_decode(self, enc_salt: str):
        return enc_salt.encode("iso-8859-1")

    def salt_generate(self):
        return uuid.uuid4().bytes

    def encrpyion_passowrd(self, pw: str, salt: bytes):
        pwencode = pw.encode("utf-8")
        xored = bytearray()
        for times in range(len(salt)):
            xored.append(salt[times] ^ pwencode[times % len(salt)])
        return hashlib.sha256(xored).hexdigest()

    # https://stackoverflow.com/questions/12524994/encrypt-and-decrypt-using-pycrypto-aes-256
    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    def AES_encryption(self, pw: str, salt):
        pw = self._pad(pw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(salt, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(pw.encode()))

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]

    def AES_decryption(self, enc, salt):
        dec = base64.b64decode(enc)
        iv = dec[:AES.block_size]
        cipher = AES.new(salt, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(dec[AES.block_size:])).decode('utf-8')

    def pw_encode(self, pw: str):
        salt = self.salt_generate()
        return self.AES_encryption(pw, salt), self.salt_encode(salt)

    def sid_validation(self, sid: str):
        return self.get_user_data(sid)

    def data_validation(self, data: dict) -> bool:
        for key, val in data.items():
            if not val: return False
        return True

    def execute_commit(self, cursors: dict):
        for key, val in cursors.items():
            cursor, conn = None, None
            if key[0:6] == "normal":
                cursor, conn = self.cursor, self.conn
            elif key == "salt":
                cursor, conn = self._saltcursor, self._saltconn
            else:
                return ["invalidate order, reject to execute", False]
            try:
                cursor.execute(val[0], val[1])
                conn.commit()
                time.sleep(2)
            except Exception as e:
                return [f"{e}", False]

        return ["successfully injected", True]

    def sign_up_insert(self, account: str, password: str, name: str, token: int = 50) -> list:
        if self.sid_validation(account):
            warnings.warn(f"SID {account} already exist, cannot register again")
            return ["", False]
        pw_encoded, salt = self.pw_encode(password)

        sql_pw, val_pw = """INSERT INTO `user` (`account`, `pw`, `name`, `token`)
                         values (%s, %s, %s, %d);""", \
                         (account, pw_encoded, name, token)
        sql_salt, val_salt = "INSERT INTO `salt spy` (`account`, `salt`) values (%s, %s);", \
                             (account, salt)

        orders = {"normal": (sql_pw, val_pw), "salt": (sql_salt, val_salt)}
        return self.execute_commit(orders)

    def books_update(self, data: dict):
        """
        when user plan to share and sold a book
        :param data: contains book name, account, bc_hash. book_name is supposed no longer than 50 words
        :return:
        """
        if not self.data_validation(data):
            print("contain invalidate info.")
            return False
        if not self.get_book_data(data["bookname"]):
            print("same Book already been uploaded, you can not upload.")
            return False

        sql_on, value_on = """insert into `books` (`book_name`, `bc_hash`)
                values (%s, %s);
                """, (data["bookname"], data["bc_hash"])
        sql_user_property, val_pro = """insert into `user_property` (`account`, `owned_book`)
        values (%s, %s)""", (data["account"], data["bookname"])

        orders = {"normal": (sql_on, value_on), "normal1": (sql_user_property, val_pro)}
        return self.execute_commit(orders)

    def book_on_sell(self, data):
        """
        plan to implement verification and validation in another class.
        :param data:
        :return:
        """
        sql_booksell, val = """insert into `book_on_sell` (`account`, `shared_book`, `price`)
                        values (%s, %s, %d)""", (data["account"], data["shared_book"], data["price"])

        orders = {"normal": (sql_booksell, val)}
        return self.execute_commit(orders)

    def modify_book_selling(self):
        ...


    def retrieve_database(self):
        ...

if __name__ == "__main__":
    db = Database_operation()
    print(db.get_book_data('aaa'))

    
class Login(object):

    def __init__(self) -> None:
        ...

    # integration of encryption and insert, after insert to decrypt the value
    #     try:
    #         self.cursor.execute(sql_on, value_on)
    #         self.conn.commit()
    #
    #         self.cursor.execute(sql_user_property, val_pro)
    #         self.conn.commit()
    #
    #         time.sleep(2)
    #         print("successfully insert value.")
    #     except Exception as e:
    #         return [f"{e}", False]
    #
    #     return ["", True]
