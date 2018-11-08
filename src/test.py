# -*- coding:utf-8 -*-
import pymysql
from DBUtils.PooledDB import PooledDB


class OPMysql(object):

    __pool = None

    def __init__(self):
        # 构造函数，创建数据库连接、游标
        self.coon = OPMysql.getmysqlconn()
        self.cur = self.coon.cursor(cursor=pymysql.cursors.DictCursor)


    # 数据库连接池连接
    @staticmethod
    def getmysqlconn():
        if OPMysql.__pool is None:
            __pool = PooledDB(creator=pymysql, mincached=1, maxcached=20, host=mysqlInfo['host'], user=mysqlInfo['user'], passwd=mysqlInfo['passwd'], db=mysqlInfo['db'], port=mysqlInfo['port'], charset=mysqlInfo['charset'])
            print(__pool)
        return __pool.connection()

    # 插入\更新\删除sql
    def op_insert(self, sql):
        print('op_insert', sql)
        insert_num = self.cur.execute(sql)
        print('mysql sucess ', insert_num)
        self.coon.commit()
        return insert_num

    # 查询
    def op_select(self, sql):
        print('op_select', sql)
        self.cur.execute(sql)  # 执行sql
        select_res = self.cur.fetchone()  # 返回结果为字典
        print('op_select', select_res)
        return select_res

    #释放资源
    def dispose(self):
        self.coon.close()
        self.cur.close()

mysqlInfo = {
    "host": '127.0.0.1',
    "user": 'root',
    "passwd": 'root',
    "db": 'anxiaoyu',
    "port": 3306,
    "charset": 'utf8'
}

if __name__ == '__main__':
    # 申请资源
    opm = OPMysql()

    sql = "INSERT INTO `housing_resources` (`title`,`bedroom`,`rental_type`,`size`,`turn_towards`,`area`,`price`,`floor`,`decoration`,`img`,`broker_name`,`broker_mobile`,`intermediary`,`remark`) VALUES ('1',1,1,1,1,'1',1,1,'1','1','1','1','1','1'); "
    res = opm.op_insert(sql)

    # 释放资源
    opm.dispose()