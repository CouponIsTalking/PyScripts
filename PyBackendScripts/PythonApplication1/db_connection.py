import sqlite3
import _mysql_exceptions
# first of all connect with mysql to check the work done 
#!/usr/bin/python
# e begoli, python connector for mysql
# import MySQL module
import MySQLdb

import misc
from misc import *

#DB_HOST = 'clparser.db.6508209.hostedresource.com'
#DB_USER = 'clparser'
#DB_PASS = 'GrandDb456'
#DB_NAME = 'clparser'

DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASS = ''
DB_NAME = 'trackit_db_test'
#DB_NAME = 'clparser'

DB_CONNECTION_HANDLE = None;

def getDBConn():
	#print "# connect"
	while 1:
		waittime = 30;
		try:
			db = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASS, db=DB_NAME)
			#print "# create a database cursor"
			DB_CONNECTION_HANDLE = db
			return db
		except _mysql_exceptions.OperationalError:
			time.sleep(waittime)
			waittime = waittime + 30


def doesAlreadyExist(db, foreign_job_id):
	check_if_link_already_exist_query = "SELECT * FROM joblinks where http_link = '%s';" % addslashes(foreign_job_id)
	cursor = DBQuery(db, check_if_link_already_exist_query)
	## if the first result is not 'None', then link already exists
	if str(cursor.fetchone()) != 'None':
		#print "link already exists in DB for foreign id "+foreign_job_id
		return 1;
	else:
		return 0;
					
def DBQuery(db, query ):
	
	if db != None :
		cursor = db.cursor()
	elif DB_CONNECTION_HANDLE != None :
		db = DB_CONNECTION_HANDLE
		cursor = db.cursor()
	else :
		db = getDBConn()
		cursor = db.cursor()
	
	while 1:
		try:
			cursor.execute(query)
			break
		except sqlite3.OperationalError:
			time.sleep(60)
			db = getDBConn()
			cursor = db.cursor()
		except _mysql_exceptions.OperationalError:
			time.sleep(60)
			db = getDBConn()
			cursor = db.cursor()
			
	return cursor		

def DBInsertQuery(db, query ):
	
	if db != None :
		cursor = db.cursor()
	elif DB_CONNECTION_HANDLE != None :
		db = DB_CONNECTION_HANDLE
		cursor = db.cursor()
	else :
		db = getDBConn()
		cursor = db.cursor()
	
	while 1:
		try:
			cursor.execute(query)
			break
		except sqlite3.OperationalError:
			time.sleep(60)
			db = getDBConn()
			cursor = db.cursor()
		except _mysql_exceptions.OperationalError:
			time.sleep(60)
			db = getDBConn()
			cursor = db.cursor()
	
	db.commit()	
	return cursor		
	
def update_dupdb_with_this_job (newjob, db):
	
	qinsert = "INSERT INTO joblinks (http_link, link_time, title, email, content) VALUES ('%s', '%s', '%s', '%s', '%s')" % ( addslashes(newjob['unique_ref']), newjob['timefound'], addslashes(newjob['job_name']), newjob['contact_email'], addslashes(newjob['details']))
	
	DBInsertQuery(db, qinsert)

def testme():
	
	i = 3
	while i > 0 :
		
		if i == 3:
			db = None
			print "DB handle = None"
		elif i == 2:
			xdb = getDBConn()
			db = DB_CONNECTION_HANDLE
			print "DB handle from DB_CONNECTION_HANDLE"
		elif i == 1:
			db = getDBConn()
			print "DB handle from getDBConn"
		else :
			break;
			
		shouldExist = doesAlreadyExist(None, "https://marvell.apply2jobs.com/ProfExt/index.cfm?fuseaction=mExternal.showJob&RID=11086&CurrentPage=20")
		if shouldExist:
			print "SUCCESS"
		else :
			print "FAIL"
		
		shouldNotExist = doesAlreadyExist(None, "LOL THIS SHOULDN'T EXIST")
		if shouldNotExist:
			print "FAIL"
		else :
			print "SUCCESS"
	
		i = i - 1 # decrese loop counter
		

	