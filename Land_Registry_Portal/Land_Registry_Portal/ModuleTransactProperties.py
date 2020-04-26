from Land_Registry_Portal import ModuleAdvancedEncryptionStandard
from Land_Registry_Portal import ModuleInterPlanetaryFileSystem
from Land_Registry_Portal import ModuleSmartContracts
from Land_Registry_Portal import ModuleLandRegistryPortal
from Land_Registry_Portal import db_info


def verify_seller(seller_name, seller_adhar_number, seller_email_id, property_name):
    try:
        db_obj = db_info.Land_Registry_Portal()
        
        query = 'SELECT owner_id FROM land_registry_portal.tbl_owner_details WHERE owner_name = %s AND adhar_number = %s AND email = %s;'
        args = (seller_name, seller_adhar_number, seller_email_id)
        res = db_obj.select_db(query, args)
        
        if res == ():
            return False, -1
            
        owner_id = res[0]['owner_id']   
        
        query = 'SELECT current_owner_id, list_of_property_id FROM land_registry_portal.tbl_land_registry_portal_details WHERE property_name = %s;'
        args = (property_name)
        res = db_obj.select_db(query, args)
        
        if res == ():
            return False, -1
        
        current_owner_id = res[0]['current_owner_id']
        property_id = (res[0]['list_of_property_id']).split(',')[-1]
        
        if owner_id == current_owner_id:
            return True, property_id
        else:
            return False, -1
    except:
        return False, -1


def verify_buyer_and_add_to_database(buyer_name, buyer_adhar_number, buyer_email_id):

    db_obj = db_info.Land_Registry_Portal()
    
    # Check whether buyer already exists in database or not.
    query = 'SELECT owner_id FROM land_registry_portal.tbl_owner_details WHERE owner_name = %s AND adhar_number = %s;'
    args = (buyer_name, buyer_adhar_number)
    owner_id = db_obj.select_db(query, args)
    
    if owner_id == ():
        # The owner details don't exist in the system. New owner_id needs to be created!
        query = 'INSERT INTO land_registry_portal.tbl_owner_details(owner_name, adhar_number, email) VALUES (%s, %s, %s);'
        args = (buyer_name, buyer_adhar_number, buyer_email_id)
        db_obj.insert_db(query, args)
        

def update_owner(seller_name, seller_adhar_number, seller_email_id, property_name, buyer_name, buyer_adhar_number, buyer_email_id, file_name, witness1_name, witness1_aadhar_number, witness1_email_id, witness1_mobno, witness2_name, witness2_aadhar_number, witness2_email_id, witness2_mobno):

    seller_verification, seller_property_id = verify_seller(seller_name, seller_adhar_number, seller_email_id, property_name)
    #print(seller_verification, seller_property_id)
    if seller_verification == True:
        seller_verification_from_blockchain = ModuleSmartContracts.verify_seller(seller_property_id)
        
        if seller_verification_from_blockchain == 1:
            verify_buyer_and_add_to_database(buyer_name, buyer_adhar_number, buyer_email_id)

            buyer_property_id, encrypted_file = ModuleAdvancedEncryptionStandard.encrypt_file(file_name, property_name)
            #print(buyer_property_id, encrypted_file)
            ModuleInterPlanetaryFileSystem.upload_file_in_ipfs(buyer_property_id, property_name, encrypted_file)
            ModuleLandRegistryPortal.update_database(buyer_name, buyer_adhar_number, buyer_email_id, property_name, buyer_property_id)
            ModuleLandRegistryPortal.add_witness_details(buyer_property_id, property_name, witness1_name, witness1_aadhar_number, witness1_email_id, witness1_mobno, witness2_name, witness2_aadhar_number, witness2_email_id, witness2_mobno)
            approved = ModuleSmartContracts.update_details_to_blockchain(seller_name, seller_adhar_number, seller_email_id, buyer_name, buyer_adhar_number, buyer_email_id, property_name, seller_property_id, buyer_property_id)
                
            if approved == True:
                msg = 'Property transfered under the name of buyer successfully!'
            else:
                msg = 'Property can\'t be transfered. Transaction failed!'
        else:
            msg = 'Property doesn\'t belong to the seller according to Blockchain records. Hence property can\'t be transfered. Transaction failed!'
        
    return msg
        
        
#update_owner('abc', '123412341234', 'abc@gmail.com', 'prop7', 'xyz', '432143214321', 'xyz@gmail.com', True, 'sample.txt')
    
#update_details_to_blockchain('abc', '123412341234', 'abc@gmail.com', 'xyz', '432143214321', 'xyz@gmail.com', 'prop7', 10, 18)        
    