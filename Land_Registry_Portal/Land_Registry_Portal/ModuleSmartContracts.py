from web3 import Web3
import json
from Land_Registry_Portal import db_info


def add_details_to_blockchain(property_id, property_name):

    db_obj = db_info.Land_Registry_Portal()
    query = 'SELECT encryption_key FROM land_registry_portal.tbl_advanced_encryption_standard WHERE property_id = %s and property_name = %s;'
    args = (property_id, property_name)
    res = db_obj.select_db(query, args)
    encryption_key = res[0]['encryption_key']
    #encryption_key = encryption_key.decode('utf-8')
    
    query = 'SELECT property_paper_hash FROM land_registry_portal.tbl_inter_planetary_file_system WHERE property_id = %s and property_name = %s;'
    args = (property_id, property_name)
    res = db_obj.select_db(query, args)
    property_paper_hash = res[0]['property_paper_hash']
    
    query = 'SELECT current_owner_id FROM land_registry_portal.tbl_land_registry_portal_details WHERE property_name = %s;'
    args = (property_name)
    res = db_obj.select_db(query, args)
    current_owner_id = res[0]['current_owner_id']
    
    query = 'SELECT owner_name, adhar_number, email FROM land_registry_portal.tbl_owner_details WHERE owner_id = %s;'
    args = (current_owner_id)
    res = db_obj.select_db(query, args)
    owner_name = res[0]['owner_name']
    adhar_number = res[0]['adhar_number']
    email = res[0]['email']
    
    owner_details = str(property_id) + str(property_name) + str(encryption_key) + str(property_paper_hash) + str(owner_name) + str(adhar_number) + str(email)
    hash = Web3.soliditySha3(['string'], [owner_details])
    print(hash)
   

    url = 'http://127.0.0.1:7545'
    web3 = Web3(Web3.HTTPProvider(url))
    if web3.isConnected():

        abi = json.loads('[{"constant":false,"inputs":[{"internalType":"int256","name":"_property_id","type":"int256"},{"internalType":"string","name":"_owner_hash","type":"string"}],"name":"add_details","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"int256","name":"_seller_property_id","type":"int256"},{"internalType":"string","name":"_seller_hash","type":"string"}],"name":"approve_details","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"int256","name":"_property_id","type":"int256"}],"name":"getHash","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"int256","name":"_property_id","type":"int256"}],"name":"getStatus","outputs":[{"internalType":"int256","name":"","type":"int256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"int256","name":"_property_id","type":"int256"}],"name":"revoke_ownership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]')

        address = web3.toChecksumAddress('0x5f50715071EBa9adA24971FC82347a164cF233C1')
        
        contract = web3.eth.contract(address = address, abi = abi)
        
        tx_hash = contract.functions.add_details(property_id, str(hash)).transact({"from": '0xC3777FdDe7B3CaEa4ae874D7cb94d1405b113eFd'})
        web3.eth.waitForTransactionReceipt(tx_hash)

        #hash = contract.functions.getHash(web3.toInt(property_id)).call()
        #print(hash)
        

def verify_seller(seller_property_id):

    url = 'http://127.0.0.1:7545'
    web3 = Web3(Web3.HTTPProvider(url))
    if web3.isConnected():

        abi = json.loads('[{"constant":false,"inputs":[{"internalType":"int256","name":"_property_id","type":"int256"},{"internalType":"string","name":"_owner_hash","type":"string"}],"name":"add_details","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"int256","name":"_seller_property_id","type":"int256"},{"internalType":"string","name":"_seller_hash","type":"string"}],"name":"approve_details","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"int256","name":"_property_id","type":"int256"}],"name":"getHash","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"int256","name":"_property_id","type":"int256"}],"name":"getStatus","outputs":[{"internalType":"int256","name":"","type":"int256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"int256","name":"_property_id","type":"int256"}],"name":"revoke_ownership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]')

        address = web3.toChecksumAddress('0x5f50715071EBa9adA24971FC82347a164cF233C1')
        
        contract = web3.eth.contract(address = address, abi = abi)
        
        status = contract.functions.getStatus(int(seller_property_id)).call()
        print(status)
            
        return status

        
def update_details_to_blockchain(seller_name, seller_adhar_number, seller_email_id, buyer_name, buyer_adhar_number, buyer_email_id, property_name, seller_property_id, buyer_property_id):

    db_obj = db_info.Land_Registry_Portal()
    query = 'SELECT encryption_key FROM land_registry_portal.tbl_advanced_encryption_standard WHERE property_id = %s and property_name = %s;'
    args = (seller_property_id, property_name)
    res = db_obj.select_db(query, args)
    seller_encryption_key = res[0]['encryption_key']
    #encryption_key = encryption_key.decode('utf-8')
    
    query = 'SELECT property_paper_hash FROM land_registry_portal.tbl_inter_planetary_file_system WHERE property_id = %s and property_name = %s;'
    args = (seller_property_id, property_name)
    res = db_obj.select_db(query, args)
    seller_property_paper_hash = res[0]['property_paper_hash']
    
    seller_details = str(seller_property_id) + str(property_name) + str(seller_encryption_key) + str(seller_property_paper_hash) + str(seller_name) + str(seller_adhar_number) + str(seller_email_id)
    seller_hash = Web3.soliditySha3(['string'], [seller_details])
    print(seller_hash)
    
    db_obj = db_info.Land_Registry_Portal()
    query = 'SELECT encryption_key FROM land_registry_portal.tbl_advanced_encryption_standard WHERE property_id = %s and property_name = %s;'
    args = (seller_property_id, property_name)
    res = db_obj.select_db(query, args)
    buyer_encryption_key = res[0]['encryption_key']  

    query = 'SELECT property_paper_hash FROM land_registry_portal.tbl_inter_planetary_file_system WHERE property_id = %s and property_name = %s;'
    args = (buyer_property_id, property_name)
    res = db_obj.select_db(query, args)
    buyer_property_paper_hash = res[0]['property_paper_hash']    
    
    buyer_details = str(buyer_property_id) + str(property_name) + str(buyer_encryption_key) + str(buyer_property_paper_hash) + str(buyer_name) + str(buyer_adhar_number) + str(buyer_email_id)
    buyer_hash = Web3.soliditySha3(['string'], [buyer_details])
    print(buyer_hash)
   

    url = 'http://127.0.0.1:7545'
    web3 = Web3(Web3.HTTPProvider(url))
    if web3.isConnected():

        abi = json.loads('[{"constant":false,"inputs":[{"internalType":"int256","name":"_property_id","type":"int256"},{"internalType":"string","name":"_owner_hash","type":"string"}],"name":"add_details","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"int256","name":"_seller_property_id","type":"int256"},{"internalType":"string","name":"_seller_hash","type":"string"}],"name":"approve_details","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"int256","name":"_property_id","type":"int256"}],"name":"getHash","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"int256","name":"_property_id","type":"int256"}],"name":"getStatus","outputs":[{"internalType":"int256","name":"","type":"int256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"int256","name":"_property_id","type":"int256"}],"name":"revoke_ownership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]')

        address = web3.toChecksumAddress('0x5f50715071EBa9adA24971FC82347a164cF233C1')
        
        contract = web3.eth.contract(address = address, abi = abi)
        
        print(1)
        approved = contract.functions.approve_details(int(seller_property_id), str(seller_hash)).call()
        print(approved)
        
        if approved == True:
            tx_hash = contract.functions.add_details(buyer_property_id, str(buyer_hash)).transact({"from": '0xC3777FdDe7B3CaEa4ae874D7cb94d1405b113eFd'})
            web3.eth.waitForTransactionReceipt(tx_hash)
            tx_hash = contract.functions.revoke_ownership(int(seller_property_id)).transact({"from": '0xC3777FdDe7B3CaEa4ae874D7cb94d1405b113eFd'})
            web3.eth.waitForTransactionReceipt(tx_hash)
            
        return approved
                

#update_details_to_blockchain('DISHA SHINDE', 432143214321, 'dishashinde17@gmail.com', 'xyz', 432143214321, 'xyz@gmail.com', 'prop21', 49, 53)

'''
pragma solidity >=0.4.22 <0.6.0;

contract Land_Registry_Portal {

    struct Owner {
        string owner_hash;
        int status;
    }
   
    mapping(int => Owner) owner_details;
    
    function add_details(int _property_id, string memory _owner_hash) public {
        
        owner_details[_property_id].owner_hash = _owner_hash;
        owner_details[_property_id].status = 1;
    }
    
    function revoke_ownership(int _property_id) public {
        
        owner_details[_property_id].status = 0;
    }
    
    function getHash(int _property_id) public view returns(string memory) {
        
        return owner_details[_property_id].owner_hash;
    }
    
    function getStatus(int _property_id) public view returns(int) {
        
        return owner_details[_property_id].status;
    }
    
    function approve_details(bool _auth_1, bool _auth_2, int _seller_property_id, string memory _seller_hash) public view returns(bool) {
        
        if (_auth_1 == true && _auth_2 == true) {
        
            if (keccak256(abi.encodePacked(_seller_hash)) == keccak256(abi.encodePacked(owner_details[_seller_property_id].owner_hash))) {
                return true;   
            }
            return false;
            
        }
    }    
    
}
'''