import argparse,json,os
    
# retrieve output location
parser = argparse.ArgumentParser()
parser.add_argument('--tenant_metadata_folder', type=str, dest='tenant_metadata_folder')
args, unknown_args = parser.parse_known_args()
tenant_metadata_folder = args.tenant_metadata_folder
print("tenant_metadata_folder:", tenant_metadata_folder)

# simulating reading tenants from DB
tenants = []
for i in range(1, 100):
    tenants.append({ "id": str(i) })

# dump tenant metadata/data into one file per tenant for further processing by parallel run step
for tenant in tenants:
    tenant_metadata_file_name = "tenant_" + tenant['id'] + '.json'
    with open(os.path.join(tenant_metadata_folder,tenant_metadata_file_name),'w') as tenant_metadata_file:
        json.dump(tenant,tenant_metadata_file)