from cryptography.fernet import Fernet
from Land_Registry_Portal import db_info
import glob
import traceback
import os


def generate_key_for_advanced_encryption_standard(property_name, extension):
    try:
        #generate key
        key = Fernet.generate_key()
        
        db_obj = db_info.Land_Registry_Portal()
        query = 'INSERT INTO land_registry_portal.tbl_advanced_encryption_standard(property_name, encryption_key, extension) VALUES (%s, %s, %s);'
        args = (property_name, key.decode('utf-8'), extension)
        db_obj.insert_db(query, args)
        
        query = 'SELECT property_id FROM land_registry_portal.tbl_advanced_encryption_standard WHERE encryption_key = %s;'
        args = (key.decode('utf-8'))
        res = db_obj.select_db(query, args)
        #print(res)
        property_id = res[0]['property_id']

        return property_id, key
    except:
        traceback.print_exc()
        

def encrypt_file(file_name, property_name):
    try:
        extension = file_name.split('.')[1]
        
        #encryption
        with open ('C:/Users/DISHA/Documents/GitHub/BE Project/Land_Registry_Portal/Land_Registry_Portal/Encrypted_Property_Papers/'+file_name, 'rb') as f:
            data = f.read()

        property_id, key = generate_key_for_advanced_encryption_standard(property_name, extension)
        
        fernet = Fernet(key)
        encrypted = fernet.encrypt(data)

        file_name1 = 'C:/Users/DISHA/Documents/GitHub/BE Project/Land_Registry_Portal/Land_Registry_Portal/Encrypted_Property_Papers/'+str(property_id)+'_'+property_name+'.'+str(extension)+'.encrypted'
        with open(file_name1, 'wb')as f:
            f.write(encrypted)
        
        os.remove('C:/Users/DISHA/Documents/GitHub/BE Project/Land_Registry_Portal/Land_Registry_Portal/Encrypted_Property_Papers/'+file_name)
            
        return property_id, file_name1
    except:
        traceback.print_exc()
        
                
def extract_key_for_decryption(property_id):
    try:
        db_obj = db_info.Land_Registry_Portal()
        query = 'SELECT encryption_key FROM land_registry_portal.tbl_advanced_encryption_standard WHERE property_id = %s;'
        args = (property_id)
        res = db_obj.select_db(query, args)
        key = res[0]['encryption_key']
        
        return key
        
    except:
        traceback.print_exc()


def decrypt_file(property_id):
    try:        
        #decryption
        file_name = glob.glob('C:/Users/DISHA/Documents/GitHub/BE Project/Land_Registry_Portal/Land_Registry_Portal/Decrypted_Property_Papers/'+str(property_id)+'_*')
        file_name = file_name[0].split('\\')[1]

        with open ('Land_Registry_Portal/Decrypted_Property_Papers/'+file_name, 'rb') as f:
            data=f.read()

        key = extract_key_for_decryption(property_id)

        fernet = Fernet(key)
        decrypted = fernet.decrypt(data)

        file_name = 'Land_Registry_Portal/Decrypted_Property_Papers/'+str(file_name[:-10])
        with open(file_name, 'wb') as f:
            f.write(decrypted)
            
        return file_name
    except:
        traceback.print_exc()
