import pymysql

### MAIN DB CONNECTION ###
def connect():
    connection = pymysql.connect(host='sgarrett-4214-practice.c2e1dpbmjmfg.us-east-2.rds.amazonaws.com',
                                 port=3306,
                                 database='sys',
                                 user='admin',
                                cursorclass=pymysql.cursors.DictCursor)
    print("Connected")
    return connection