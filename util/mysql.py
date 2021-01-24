import pymysql
from util.log import get_logger
from util.common import *


class MysqlDb(object):

    def __init__(self, option="mysql"):
        self._cfp = read_conf(option=option)
        self.logger = get_logger()
        self._connect()

    def _connect(self):
        try:
            self._conn = pymysql.connect(
                host=self._cfp["host"],
                port=int(self._cfp["port"]),
                user=self._cfp["user"],
                password=self._cfp["password"],
                db=self._cfp["db"])
            self._cursor = self._conn.cursor(pymysql.cursors.DictCursor)

        except pymysql.Error as e:
            self.logger.error(e)
            print('mysql连接失败', e)

    def __del__(self):
        self._cursor.close()
        self._conn.close()

    # def execute(self, sql):
    #     try:
    #         self._cursor.execute(sql)
    #         rowcount = self._cursor.rowcount
    #         return rowcount
    #     except pymysql.Error as e:
    #         self.logger.debug(e)

    def __query_sql_format(self, table, columns=["*"], where=None, order=None, limit=None):
        columns = ",".join(columns)
        if where is not None:
            where = sql_deal(where, str=" AND ")
        if order is not None:
            order = ",".join(order)
        if limit is None:
            if where and order is not None:
                sql = f"SELECT {columns} FROM `{table}` WHERE {where} ORDER BY {order};"
            elif where is not None and order is None:
                sql = f"SELECT {columns} FROM `{table}` WHERE {where};"
            elif where is None and order is not None:
                sql = f"SELECT {columns} FROM `{table}` ORDER BY {order};"
            else:
                sql = f"SELECT {columns} FROM `{table}`;"
        else:
            if where and order is not None:
                sql = f"SELECT {columns} FROM `{table}` WHERE {where} ORDER BY {order} limit {limit};"
            elif where is not None and order is None:
                sql = f"SELECT {columns} FROM `{table}` WHERE {where} limit {limit};"
            elif where is None and order is not None:
                sql = f"SELECT {columns} FROM `{table}` ORDER BY {order} limit {limit};"
            else:
                sql = f"SELECT {columns} FROM `{table}` limit {limit};"

        return sql

    def __insert_sql_format(self, table, columns, values):
        columns = ",".join(columns)
        values_li = []
        for i in values:
            values_li.append(str(i))
        values = ",".join(values_li)
        sql = f"INSERT INTO `{table}`({columns}) VALUES {values};"
        return sql

    def __update_sql_format(self, table, sets, where):
        if where is not None:
            where = sql_deal(where, str=" AND ")
        sets = sql_deal(sets, str=",")
        sql = f"UPDATE `{table}` SET {sets} WHERE {where};"
        return sql

    def __delete_sql_format(self, table, where):
        if where is not None:
            where = sql_deal(where, str=" AND ")
        sql = f"DELETE FROM `{table}` WHERE {where};"
        return sql

    def query(self, table, columns=["*"], where=None, order=None, limit=None, one=True):
        '''

        :param table: 表名
        :param columns: 列名，列表形式["name", "age"]，默认全部
        :param where: 筛选条件，列表形式["height=180", "age=18"]
        :param order: 按字段排序，列表形式["name", "age"]
        :param limit:
        :param one:
        :return:
        '''
        sql = self.__query_sql_format(table=table, columns=columns, where=where, order=order, limit=limit)
        self.logger.info(sql)
        if one:
            try:
                self._cursor.execute(sql)
                data = self._cursor.fetchone()
                self.logger.debug(data)
                return data

            except pymysql.Error as e:
                self.logger.error(e)
                print(e)
        else:
            try:
                self._cursor.execute(sql)
                data = self._cursor.fetchall()
                self.logger.debug(data)
                return data

            except pymysql.Error as e:
                self.logger.error(e)
                print(e)

    def insert(self, table, columns, values):
        '''

        :param table: 表名
        :param columns: 列名，列表形式["name", "age"]
        :param values: 插入数据列表形式[("saki", "20"), ("mimi", "90")]
        :return:
        '''
        sql = self.__insert_sql_format(table=table, columns=columns, values=values)
        self.logger.info(sql)
        try:
            self._cursor.execute(sql)
            self._conn.commit()
            res = self._cursor.lastrowid
            self.logger.debug(res)
            return res

        except pymysql.Error as e:
            self.logger.error(e)
            print(e)
            self._conn.rollback()

    def update(self, table, sets, where):
        '''

        :param table: 表明
        :param sets: 修改内容
        :param where: 筛选条件，列表形式["height=180", "age=18"]
        :return:
        '''
        sql = self.__update_sql_format(table=table, sets=sets, where=where)
        self.logger.info(sql)
        try:
            self._cursor.execute(sql)
            self._conn.commit()
            rowcount = self._cursor.rowcount
            self.logger.debug(rowcount)
            return rowcount

        except pymysql.Error as e:
            self.logger.error(e)
            print(e)
            self._conn.rollback()

    def delete(self, table, where):
        '''

        :param table: 表名
        :param where: 筛选条件，列表形式["height=180", "age=18"]
        :return:
        '''
        sql = self.__delete_sql_format(table=table, where=where)
        self.logger.info(sql)
        try:
            self._cursor.execute(sql)
            self._conn.commit()
            rowcount = self._cursor.rowcount
            self.logger.debug(rowcount)
            return rowcount

        except pymysql.Error as e:
            self.logger.error(e)
            print(e)
            self._conn.rollback()


if __name__ == '__main__':
    my = MysqlDb("mysql")
    a = my.query(table="user", columns=["name", "age"],where=["age=20"],limit=3, one=False)
    print(a)

    b = my.insert(table="user", columns=["name", "age"], values=[("lisi", 28), ("wangwu", 78)])
    print(b)

    # c = my.update(table="user", sets=["name=1234"], where=["age=188"])
    # print(c)
    #
    # d = my.delete(table="user", where=["age=188"])
    # print(d)