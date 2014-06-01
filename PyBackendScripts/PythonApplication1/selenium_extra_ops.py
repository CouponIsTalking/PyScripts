from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
import time

import hashlib

def WaitForPageRefresh ( driver, orig_page_source, timeout_in_sec):

	orig_page_source = orig_page_source.encode("ascii", "ignore")
	first_hash = hashlib.md5(orig_page_source)
	#second_hash = first_hash
	time_spent = 0
	sleep_time = 5	# in secs
	
	while 1:
		time.sleep(sleep_time)
		new_page_source = driver.page_source.encode("ascii", "ignore")
		second_hash = hashlib.md5(new_page_source)
		time_spent = time_spent + sleep_time
		if (time_spent >= timeout_in_sec or first_hash != second_hash):
			break;
			
	return 

def WaitForPageRefreshWithGivenInBWSleepTime ( driver, orig_page_source, timeout_in_sec, sleep_time):

	orig_page_source = orig_page_source.encode("ascii", "ignore")
	first_hash = hashlib.md5(orig_page_source)
	#second_hash = first_hash
	time_spent = 0
	#sleep_time = 5	# in secs
	
	while 1:
		time.sleep(sleep_time)
		new_page_source = driver.page_source.encode("ascii", "ignore")
		second_hash = hashlib.md5(new_page_source)
		time_spent = time_spent + sleep_time
		if (time_spent >= timeout_in_sec or first_hash != second_hash):
			break;
			
	return 
