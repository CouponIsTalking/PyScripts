from FCPLinks import *

max_comp_id = 167 # hard coded using the max company id in admin menu
i = 40
fcpl = FCPLinks( 0 )
    
while i < max_comp_id:
    fcpl.reinit(i)
    #time.sleep(i/3 * 10)
    fcpl.set_enabled_sites(["deals2buy.com"])
    try:
        fcpl.init_fcplink_retrv()
    except:
        pass
    try:
        fcpl.update_fcplink()
    except:
        pass
    
    print fcpl.fcp_info
    i=i+1

fcpl.deinit()
    