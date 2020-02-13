from Land_Registry_Portal import db_info
from Land_Registry_Portal import ModuleInterPlanetaryFileSystem
from Land_Registry_Portal import ModuleAdvancedEncryptionStandard


def view_property(property_name):

    property_details = []
    
    db_obj = db_info.Land_Registry_Portal()
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

    property_details.append(property_id) 
    property_details.append(property_name)
    property_details.append(owner_name)
    property_details.append(adhar_number)
    property_details.append(email)
    property_details.append(registration_time)
    
    return property_details
    
    
    
def search_detailed_property_info(plot_number, sector_number, road_name, area_name, city_name, state_name, country_name, pin_code):

    property_details = []
    args_list = []
    
    db_obj = db_info.Land_Registry_Portal()
    
    query = 'SELECT * FROM land_registry_portal.tbl_property_address_details WHERE '
    
    if plot_number == '' and sector_number == '' and road_name == '' and area_name == '' and city_name == '' and state_name == '' and country_name == '' and pin_code == '':
        query = query[: -7] + ';'
        #print(query)
    else:
        if plot_number != '':
            query += 'plot_number = %s AND '
            args_list.append(plot_number)
        if sector_number != '':
            query += 'sector_number = %s AND '
            args_list.append(sector_number)
        if road_name != '':
            query += 'road_name = %s AND '
            args_list.append(road_name)
        if area_name != '':
            query += 'area_name = %s AND '
            args_list.append(area_name)
        if city_name != '':
            query += 'city_name = %s AND '
            args_list.append(city_name)
        if state_name != '':
            query += 'state_name = %s AND '
            args_list.append(state_name)
        if country_name != '':
            query += 'country_name = %s AND '
            args_list.append(country_name)
        if pin_code != '':
            query += 'pin_code = %s AND '
            args_list.append(pin_code)
                 
        query = query[: -5] + ';'
        #print(query)
        
    args = tuple(args_list)
    res = db_obj.select_db(query, args)
    #print(res)
    
    if res != ():
        for i in range(len(res)):
            property_name = res[i]['property_name']
            address = 'Plot no. : ' + str(res[i]['plot_number']) + ', Sector no. : ' + str(res[i]['sector_number']) + ', ' + res[i]['road_name'] + ', ' + res[i]['area_name'] + ', ' + res[i]['city_name'] + ', ' + res[i]['state_name'] + ', ' + res[i]['country_name'] + ' - ' + str(res[i]['pin_code'])
            
            property_details.append(property_name+';'+address)
    
    return property_details


#print(search_detailed_property_info('pune', 'pune', '', 624, 18, '')    )
    
# search_property_by_address('pune', 'pune', 'shivtej nagar', 624, 18)

