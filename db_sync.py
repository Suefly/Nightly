#!/usr/bin/python
import MySQLdb
import time

class DB:
    def __init__(self, host, db_name, port=3306, username='root', password='itsabug'):
        self.host = host
        self.db_name = db_name
        self.port = port
        self.username = username
        self.password = password

    def connect_db(self):
        try:
            db_handle = MySQLdb.connect(
                host=self.host,
                user=self.username,
                passwd=self.password,
                port=self.port,
                db=self.db_name,
            )
            print "Database has successfully connected!"
            return db_handle
        except Exception as e:
            print(e)
            return False

    def disconnect_db(self, db_handle):
        db_handle.close()

    def execute_db(self, db_handle, sqlquery):
        dbcursor = db_handle.cursor()
        try:
            dbcursor.execute(sqlquery)
            result = db_handle.commit()
            dbrecord = dbcursor.fetchall()
            # print(dbrecord)
            return dbrecord[0]
        except:
            db_handle.rollback()
            return False

    def __enter__(self):
        # self.connect_db()
        return self

    def __exit__(self, type, value):
        # self.disconnect_db(self.handle)
        return self


if __name__ == '__main__':
    # iap_list = ["IAP335","IAP325","IAP315","IAP305","IAP225","IAP365","IAP303H","IAP203H","IAP203R"]
    iap_list = {"IAP335":{"5G":"10.64.25.37","2.4G":"10.64.25.37"}, \
                "IAP325":{"5G":"10.64.25.21","2.4G":"10.64.25.34"}, \
                }
    band_dict = {"2.4G": "HT20", "5G": "VHT80"}
    direction_list = ["up","down"]
    build_list = [58846,58867,58882,59068,59123]

    sql_input = "select distinct input.inputId from apTbl ap,apTypeTbl apt,swTopologyTbl tp,swRadioTbl rd,swPerformanceInputTbl \
        input where apt.apType='%s' and apt.apTypeId=ap.apTypeId and ap.topologyId=32 and rd.apId=ap.apId \
        and rd.band = '%s' and rd.frequency = '%s' and rd.apId = input.apId and rd.radioId = input.radioId \
        and input.trafficDirection = '%s'"

    sql_throughput = "select DISTINCT output.inputId from swPerformanceOutputTbl output, swPerformanceInputTbl input \
    where output. = input.inputIinputIdd and output.inputId"

    sql_client = "select clientId from swClientTbl where adminIpv4='%s'"

    sql_cfg = "select cfg.swConfigId,cfg.swVersion from swConfigTbl cfg where cfg.swBuild ='%d'"
    insert_cfg  = "insert into swConfigTbl (swVersion,swBuild) values ('6.5.2.0','%d');"
    
    db_source = DB("10.64.25.246","apPerformance",3306,"root","123456")
    db_dest = DB("10.64.25.246","test",3306,"root","123456")
    dbs_handle = db_source.connect_db()
    dbd_handle = db_dest.connect_db()
    for build in build_list:
        print "check if the build %d exist in US database! if not exist insert to it!" % build
        res = db_dest.execute_db(dbd_handle,sql_cfg % build)
        if not res:
            res1 = db_dest.execute_db(dbd_handle,insert_cfg % build)
            time.sleep(2)
        else:
            print "The build %d has already exist in US database!!!" % build
        configId = db_dest.execute_db(dbd_handle, sql_cfg % build)
        print  "The configId  is", configId

        for iap in iap_list.keys():
            for band in band_dict.keys():
                for dir in direction_list:
                    input_id = db_source.execute_db(dbs_handle,sql_input % (iap,band_dict[band],band,dir))
                    print "input_id =",input_id
                    # print "#"*10,iap_list[iap][band]
                    # print  sql_client % iap_list[iap][band]
                    client_id = db_source.execute_db(dbs_handle,sql_client % iap_list[iap][band])
                    print "client_id =",client_id
                    print "Get the throughput value for inputid = %d configid=%d and clientid=%d!!!" % (input_id[0],configId[0],client_id[0])
                    throughput = db_source.execute_db(dbs_handle,sql_output % (input_id[0],configId[0],client_id[0]))
