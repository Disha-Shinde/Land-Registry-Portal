import ipfsapi
from Land_Registry_Portal import db_info
import glob


def upload_file_in_ipfs(property_id, property_name, file_name):
    # Connect to local node
    try:
        api = ipfsapi.connect('127.0.0.1', 5001)
        #print(api)        
        new_file = api.add(file_name)
        hash = new_file['Hash']
        
        db_obj = db_info.Land_Registry_Portal()
        query = 'INSERT INTO land_registry_portal.tbl_inter_planetary_file_system(property_id, property_name, property_paper_hash) VALUES (%s, %s, %s);'
        args = (property_id, property_name, hash)
        db_obj.insert_db(query, args)
        
        return hash
    except ipfsapi.exceptions.ConnectionError as ce:
        print(str(ce))
        

def retrieve_file_from_ipfs(property_id, property_name, hash):
    try:
        api = ipfsapi.connect('127.0.0.1', 5001)
        #print(api)
        
        content=api.cat(hash)
 
        file_name = glob.glob('F:/BE Project/Land_Registry_Portal/Land_Registry_Portal/Decrypted_Property_Papers/'+str(property_id)+'_*')[0]
        f=open(file_name, 'wb')
        f.write(content)
        
    except ipfsapi.exceptions.ConnectionError as ce:
        print(str(ce))


#print(upload_file("Encrypted_Property_Papers/sample.txt"))
#retrieve_file('sample.txt','Qmed5e19FCV7Yn9DPWUA4i8r9KiG9v59jdHjktVao1HosX')
#upload_file_in_ipfs(1, '', 'F:\BE Project\Land_Registry_Portal\Land_Registry_Portal\Encrypted_Property_Papers\sample.txt') 