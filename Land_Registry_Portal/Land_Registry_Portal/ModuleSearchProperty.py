import ModuleInterPlanetaryFileSystem
import ModuleAdvancedEncryptionStandard
import db_info

def search_property(district_name, city_name, area_name, plot_number, sector_number):
    query = 'SELECT property_name FROM land_registry_portal.property_details WHERE district_name = %s AND city_name = %s AND area_name = %s AND plot_number = %s AND sector_number = %s;'
    args = (area_name,plot_number,sector_number)
    res = db_obj.select_db(query, args)
    property_name = res[0]['property_name']

    query = 'SELECT current_owner_id,list_of_property_id FROM land_registry_portal.tbl_land_registry_portal_details WHERE property_name=%s'
    args = (property_name)
    res = db_obj.select_db(query, args)
    current_owner_id = res[0]['current_owner_id']
    list_of_property_id = res[0]['list_of_property_id']

    property_id = list_of_property_id.split(',')[-1]

    query = 'SELECT * FROM land_registry_portal.tbl_owner_details WHERE current_owner_id = %s'
    args = (current_owner_id)
    res = db_obj.select_db(query, args)
    owner_name = request.POST.get("owner_name")
    adhar_number = request.POST.get("adhar_number")
    email = request.POST.get("email")
    registration_time = request.POST.get("registration_time")

    query = 'SELECT property_paper_hash FROM land_registry_portal.tbl_interplanetary_file_system WHERE property_name = %s AND property_id = %s'
    args = (property_name, property_id)
    res = db_obj.select_db(query, args)
    property_paper_hash = res[0]['property_paper_hash']

    ModuleInterPlanetaryFileSystem.retrieve_file_from_ipfs(property_id, property_name, property_hash)
    decrypted_file = ModuleAdvancedEncryptionStandard.decrypt_file(property_id)

return property_id,property_name,owner_name,adhar_number,email,registration_time

