from azureml_user.parallel_run import EntryScript

import json,os,time

#
def init():
    
    global logger
    logger = EntryScript().logger
    logger.info("train init()")
    
#
def run(mini_batch):
    
    results = []
    logger.info(f"train run({mini_batch})")
    for tenant_file_path in mini_batch:
        tenant_basename = os.path.basename(tenant_file_path)
        with open(tenant_file_path,'r') as tenant_file:
            tenant_dict = json.load(tenant_file)
        logger.info(f"train processing({tenant_basename} => {tenant_dict})")
        time.sleep(0.5) # simulate some small processing
        results.append(f"{tenant_basename},processed")

    return results