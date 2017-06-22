# import MySQLdb


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
                    host=self.serverip,
                    user=self.username,
                    passwd=self.password,
                    port=self.portnum,
                    db=self.dbname,
                )
                return db_handle
            except Exception as e:
                print(e)
                return False

        def disconnect_db(self, db_handle):
            db_handle.close()

        def update_db(self, db_handle, sqlquery):
            dbcursor = db_handle.cursor()
            try:
                dbcursor.execute(sqlquery)
                result = db_handle.commit()
                print(result)
                return True
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
    iap_list = {"IAP335":{"5G":"10.64.25.37","2.4G":"10.65.25.37"}, \
                "IAP325":{"5G":"10.64.25.21","2.4G":"10.64.25.34"}, \
                }
    band_dict = {"2.4G": "HT20", "5G": "VHT80"}
    direction_list = ["up","down"]

    sql_query = "select distinct input. from apTbl ap,apTypeTbl apt,swTopologyTbl tp,swRadioTbl rd,swPerformanceInputTbl \
        input where apt.apType='%s' and apt.apTypeId=ap.apTypeId and ap.topologyId=32 and rd.apId=ap.apId \
        and rd.band = '%s' and rd.frequency = '%s' and rd.apId = input.apId and rd.radioId = input.radioId \
        and input.trafficDirection = '%s'"

    sql_throughput = "select DISTINCT output.inputId from swPerformanceOutputTbl output, swPerformanceInputTbl input \
    where output. = input.inputIinputIdd and output.inputId"

    sql_client = "select clientId from swClientTbl where adminIpv4='%s'"

    for iap in iap_list.keys():
        for band in band_dict.keys():
            for dir in direction_list:
                # print("iap=",iap,"band=",band,"dir=",dir)
                sql = sql_query % (iap,band_dict[band],band,dir)
                print(sql)
                print(iap_list[iap][band])
                sql_client % iap_list[iap][band]

