#
# usage process_pending_jobs.py job_types=get_rp:get_prod_detail
#  options - 
#   job_types
#   mode_set
#   update_status
#   bypass_txt_update
#
#
from FeatureExtractor import *
from web_interface import *
from get_related_prods import *
from GenPriceNotf import *
from misc import *
import time
import signal, os
import sys


global_settings = {'mode_set' : 'accurate', 'update_status': 1}

if len(sys.argv) >=2 :
    params = sys.argv[1].split(',')
    for param in params:
        vals = param.split('=')
        print vals
        if 'job_types' == vals[0]: 
            if 'allowed_job_types' not in global_settings: global_settings['allowed_job_types'] = {}
            all_parts_of_vals1 = vals[1].split(':')
            for x in all_parts_of_vals1:
                global_settings['allowed_job_types'][x] = True
        elif 'mode_set' == vals[0]:
            global_settings['mode_set'] = vals[1]			
        elif 'update_status' == vals[0]:
            global_settings['update_status'] = int(vals[1])
        elif 'bypass_txt_update' == vals[0]:
            global_settings['bypass_txt_update'] = int(vals[1])
        
process_id = os.getpid()
with open("process_pending_jobs_pid.txt", "w") as f:
    f.write(str(process_id))


# globals
rp_urllib2 = GetRelatedProds("", "")
rp_urllib2.set_tool('urllib2')

rp_selenium = GetRelatedProds("", "")
rp_selenium.set_tool('selenium')

fe = FeatureExtractor("")

wi = WebInterface()

processing_jobs = False
    
def run():
    
    global rp_urllib2
    global rp_selenium
    global fe
    global wi
    global processing_jobs
    global global_settings
    
    if True == processing_jobs:
        return 'processing'
    
    processing_jobs = True
    
    print "Processing jobs"
    
    while True:
        
        job_type_str = ""
        for x in global_settings['allowed_job_types']: 
            if global_settings['allowed_job_types'][x] : job_type_str = x if (not job_type_str) else job_type_str + "," + x
        
        jobs = wi.get_pending_jobs(job_type_str)
        if not jobs:
            print "-------------- NO MORE PENDING JOBS FOUND --------------"
            return 'no_more_jobs'
        
        print str(len(jobs)) + " new jobs found"
        for job in jobs:
            type = job['type']
            url = job['url']
            result = False
            
            # if this is not our job type, then continue
            if type not in global_settings['allowed_job_types']:
                print "Job type ("+type+") not the one we're processing in this job"
                continue
            else:
                print "Going to process new job type ("+type+")"
            
            if (type == 'get_rp'):
                rp_selenium.set_tool('selenium')
                rp_selenium.move_to_url(url)
                rp_selenium.set_tool('urllib2')
                full_links = rp_selenium.extract_related_prods();
                print full_links
                result = rp_selenium.update_related_prods_in_db() if full_links else True
            
            elif (type == 'get_prod_detail'):
                if fe.reinit(url):
                    #fe.set_mode('accurate')
                    fe.set_mode(global_settings['mode_set'])
                    fe.run()
                    fe.print_stuff()
                    result = fe.update_prod_info_in_db()
                elif not fe.tracker_info:
                    wi.update_backend_job_status(job['id'], 101)
                # update product with title (if not already present), price, image(if not already present) data
            elif (type=='gen_pr_notf'):
                gpn = GenPriceNotf(job['pid'].encode("ascii","ignore"))
                done = gpn.generate_notifications()
                result = True if done else False
            
            if 1==global_settings['update_status'] and result == True:
                wi.update_backend_job_status(job['id'], 1)
    
    processing_jobs = False
    return 'finished'
        
def new_job_handler1(signum, frame):
    print 'new_job_handler called to get prod info', signum
    new_call = run() if (True==processing_job) else False
    print new_call
    
#signal.signal(signal.SIGILL, new_job_handler1)

#while True:
#    pass

while True:
    
    new_call = False
    bypass_txt_update=False;
    if "bypass_txt_update" in global_settings:
        if 1==global_settings['bypass_txt_update']:
            bypass_txt_update=True;
        
    run_result = ""
    # sleep for another minute if we found no pending jobs in last
    # run's result
    if run_result == 'no_more_jobs':
        print "No more jobs."
        print "...zzz...Going to check after 5 minute now...zzz..."
        time.sleep(300)
    
    if bypass_txt_update:
        new_call = True
        # if we are bypassing text file check, then wait and play nice
        print "...zzz...Going to check after a minute now...zzz..."
        time.sleep(60);
    else:
        try:
            response_page = wi.get_a_webpage(SITE_NAME + "/py/trackit/PythonApplication1/more_pending_jobs.txt")
            val = response_page
            new_call = True if val and (1==int(val)) else False
        except IOError, e:
            print "No such file"
        except ValueError, e:
            print "value error, likely IO op on closed file"
            #time.sleep(2)
        time(10)
    
    if new_call:
        run_result = run()
        wi.get_a_webpage(SITE_NAME + "/products/disable_trigger_for_pending_jobs")
        #with open("more_pending_jobs.txt", "w") as f:
        #    f.write("0")
    
    
# deinit stuff
rp_selenium.deinit()    
rp_urllib2.deinit()
fe.deinit()  