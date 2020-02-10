from Land_Registry_Portal import db_info
from Land_Registry_Portal import ModuleInterPlanetaryFileSystem
from Land_Registry_Portal import ModuleAdvancedEncryptionStandard


def search_property_by_address(district_name, city_name, area_name, plot_number, sector_number):

    db_obj = db_info.Land_Registry_Portal()
    query = 'SELECT property_name FROM land_registry_portal.tbl_property_address_details WHERE district_name = %s AND city_name = %s AND area_name = %s AND plot_number = %s AND sector_number = %s;'
    args = (district_name, city_name, area_name, plot_number, sector_number)
    res = db_obj.select_db(query, args)
    property_name = res[0]['property_name']

    query = 'SELECT current_owner_id, list_of_property_id FROM land_registry_portal.tbl_land_registry_portal_details WHERE property_name = %s;'
    args = (property_name)
    res = db_obj.select_db(query, args)
    current_owner_id = res[0]['current_owner_id']
    list_of_property_id = res[0]['list_of_property_id']

    property_id = list_of_property_id.split(',')[-1]

    query = 'SELECT * FROM land_registry_portal.tbl_owner_details WHERE owner_id = %s;'
    args = (current_owner_id)
    res = db_obj.select_db(query, args)
    owner_name = res[0]['owner_name']
    adhar_number = res[0]['adhar_number']
    email = res[0]['email']
    registration_time = res[0]['registration_time']

    query = 'SELECT property_paper_hash FROM land_registry_portal.tbl_inter_planetary_file_system WHERE property_name = %s AND property_id = %s;'
    args = (property_name, property_id)
    res = db_obj.select_db(query, args)
    property_hash = res[0]['property_paper_hash']

    ModuleInterPlanetaryFileSystem.retrieve_file_from_ipfs(property_id, property_name, property_hash)
    decrypted_file = ModuleAdvancedEncryptionStandard.decrypt_file(property_id)

    return property_id,property_name,owner_name,adhar_number,email,registration_time
    
    
# search_property_by_address('pune', 'pune', 'shivtej nagar', 624, 18)

