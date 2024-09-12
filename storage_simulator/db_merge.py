import sqlite3

db1 = sqlite3.connect("iops.db")
db1Cursor = db1.cursor()
db2 = sqlite3.connect("backup_iops.db")
db2Cursor = db2.cursor()

finaldb =  sqlite3.connect("final.db")
finalCursor = finaldb.cursor()

finalCursor.execute('CREATE TABLE array_iops (id text, time TIMESTAMP, read REAL, write REAL)')
finalCursor.execute('CREATE TABLE pool_iops (id text, time TIMESTAMP, read REAL, write REAL)')
finalCursor.execute('CREATE TABLE volume_iops (id text, time TIMESTAMP, read REAL, write REAL)')
finalCursor.execute('CREATE TABLE vm_iops (id text, time TIMESTAMP, read REAL, write REAL)')

def merge_tables(table):
    for row in db1.execute("SELECT * FROM " + table).fetchall():
        stmt = "INSERT into "+ table + " VALUES('"+ str(row[0]) + "','" + str(row[1]) + "'," + str(row[2]) + "," + str(row[3]) +")"
        finalCursor.execute(stmt)
    finaldb.commit()

    for row in db2.execute("SELECT * FROM " + table).fetchall():
        stmt = "INSERT into "+ table + " VALUES('"+ str(row[0]) + "','" + str(row[1]) + "'," + str(row[2]) + "," + str(row[3]) +")"
        finalCursor.execute(stmt)
    finaldb.commit()

merge_tables("array_iops")
merge_tables("pool_iops")
merge_tables("volume_iops")
merge_tables("vm_iops")

finalCursor.execute("create view total_cust_iops as select 'c1' as id, time, sum(read) as read, sum(write) as write from array_iops GROUP by id, time order by id, time")
finalCursor.execute("create view total_array_iops as select id, time, sum(read) as read, sum(write) as write from array_iops GROUP by id, time order by id, time")
finalCursor.execute("create view total_pool_iops as select id, time, sum(read) as read, sum(write) as write from pool_iops GROUP by id, time order by id, time")
finalCursor.execute("create view total_volume_iops as select id, time, sum(read) as read, sum(write) as write from volume_iops GROUP by id, time order by id, time")
finalCursor.execute("create view total_vm_iops as select id, time, sum(read) as read, sum(write) as write from vm_iops GROUP by id, time order by id, time")
