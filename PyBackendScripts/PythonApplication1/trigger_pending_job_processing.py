import signal
import os
import time
import sys


if len(sys.argv) >= 2:
    set_val = str(sys.argv[1])

    if (set_val =='0' or set_val == '1'):

        sync_file_full_path = os.path.dirname(__file__) + os.sep + "more_pending_jobs.txt"
    
        process_id = None
        with open(sync_file_full_path, "w") as f:
            if f :
                f.write(set_val)


#with open("process_pending_jobs_pid.txt", "r") as f:
#    if f :
#        str_pid = f.readline()
#        process_id = int(str_pid) if str_pid else None
#    
#try:
#    result = os.kill(process_id, signal.SIGILL) if process_id else True
#except Exception, e:
#    print "Exception"
#    pass