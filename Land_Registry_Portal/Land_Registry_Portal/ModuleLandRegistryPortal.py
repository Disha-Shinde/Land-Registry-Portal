from Land_Registry_Portal import db_info
import traceback


def update_database(owner_name, adhar_number, email, property_name, property_id):
    try:
        db_obj = db_info.Land_Registry_Portal()
        
        # Check whether owner already exists in database or not.
        query = 'SELECT owner_id FROM land_registry_portal.tbl_owner_details WHERE owner_name = %s AND adhar_number = %s;'
        args = (owner_name, adhar_number)
        owner_id = db_obj.select_db(query, args)
        
        if owner_id == ():
            # The owner details don't exist in the system. New owner_id needs to be created!
            query = 'INSERT INTO land_registry_portal.tbl_owner_details(owner_name, adhar_number, email) VALUES (%s, %s, %s);'
            args = (owner_name, adhar_number, email)
            db_obj.insert_db(query, args)
            
            # The entry for new user is made. Now owner_id need to be extracted.
            query = 'SELECT * FROM land_registry_portal.tbl_owner_details WHERE owner_name = %s AND adhar_number = %s;'
            args = (owner_name, adhar_number)
            owner_id = db_obj.select_db(query, args)
            owner_id = owner_id[0]['owner_id']
            
        else:
            # Owner already exixts in database. Directly extract the owner name.
            owner_id = owner_id[0]['owner_id']
        
        # Check for a transaction related to property_name already exists or not.
        query = 'SELECT property_name FROM land_registry_portal.tbl_land_registry_portal_details WHERE property_name = %s;'
        args = (property_name)
        prop_name = db_obj.select_db(query, args)
        
        if prop_name == ():
            # The transaction with property_name doesn't exist. Need to create new transaction for the same.
            query = 'INSERT INTO land_registry_portal.tbl_land_registry_portal_details VALUES (%s, %s, %s, %s);'
            args = (property_name, owner_id, property_id, '')
            db_obj.insert_db(query, args)    
            
        else:
            # The transaction with property_name already exists. So append previous old owner_id and property_id and update current owner_id.
            query = 'SELECT current_owner_id, list_of_property_id, list_of_owner_id FROM land_registry_portal.tbl_land_registry_portal_details WHERE property_name = %s;'
            args = (property_name)
            details = db_obj.select_db(query, args)
            
            old_owner_id = details[0]['current_owner_id']
            list_of_property_id = details[0]['list_of_property_id'] + ',' + str(property_id)
            list_of_owner_id = details[0]['list_of_owner_id']
            if list_of_owner_id == '':
                list_of_owner_id = list_of_owner_id + str(old_owner_id)
            else:
                list_of_owner_id = list_of_owner_id + ',' + str(old_owner_id)
                   
            query = 'UPDATE land_registry_portal.tbl_land_registry_portal_details SET current_owner_id = %s, list_of_property_id = %s, list_of_owner_id = %s WHERE property_name = %s;'
            args = (owner_id, list_of_property_id, list_of_owner_id, property_name)
            db_obj.update_db(query, args)
            
    except:
        traceback.print_exc()
        
        
#update_database('abc', '123412341234', 'abc@gmail.com', 'prop1', 23)