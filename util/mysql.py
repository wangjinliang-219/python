import pymysql
from util.log import get_logger
from util.common import *


class MysqlDb(object):
    cfp = read_conf("db.ini")

    def __init__(self):
        self.logger = get_logger()
        try:
            self.conn = pymysql.connect(
                host=self.cfp["mysql"]["host"],
                port=int(self.cfp["mysql"]["port"]),
                user=self.cfp["mysql"]["user"],
                password=self.cfp["mysql"]["password"],
                db=self.cfp["mysql"]["db"])
            self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)

        except pymysql.Error as e:
            self.logger.error(e)
            print('mysql连接失败', e)

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def execute(self, sql):
        try:
            self.cursor.execute(sql)
            rowcount = self.cursor.rowcount
            return rowcount
        except pymysql.Error as e:
            self.logger.debug(e)

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
                self.cursor.execute(sql)
                data = self.cursor.fetchone()
                self.logger.debug(data)
                return data

            except pymysql.Error as e:
                self.logger.error(e)
                self.conn.rollback()
        else:
            try:
                self.cursor.execute(sql)
                data = self.cursor.fetchall()
                self.logger.debug(data)
                return data

            except pymysql.Error as e:
                self.logger.error(e)
                self.conn.rollback()

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
            self.cursor.execute(sql)
            self.conn.commit()
            res = self.cursor.lastrowid
            self.logger.debug(res)
            return res

        except pymysql.Error as e:
            self.logger.error(e)
            self.conn.rollback()

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
            self.cursor.execute(sql)
            self.conn.commit()
            rowcount = self.cursor.rowcount
            self.logger.debug(rowcount)
            return rowcount

        except pymysql.Error as e:
            self.logger.error(e)
            self.conn.rollback()

    def delete(self, table, where):
        '''

        :param table: 表名
        :param where: 筛选条件，列表形式["height=180", "age=18"]
        :return:
        '''
        sql = self.__delete_sql_format(table=table, where=where)
        self.logger.info(sql)
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            rowcount = self.cursor.rowcount
            self.logger.debug(rowcount)
            return rowcount

        except pymysql.Error as e:
            self.logger.error(e)
            self.conn.rollback()


if __name__ == '__main__':
    my = MysqlDb()
    a = my.query(table="tp_goods", columns=["goods_id", "goods_name", "goods_sn", "store_count", "comment_count"], where=["click_count<20"], order=["goods_id"], limit=3, one=False)
    print(a)
