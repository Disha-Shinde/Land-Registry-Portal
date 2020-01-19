import pymysql.cursors


class Land_Registry_Portal():
    
    def __init__(self):
        self.connection=''
    
    def getConnection(self):
        try:
            connection = pymysql.connect(host='127.0.0.1',
                                         user='dbadmin',
                                         password='disha_shinde',                             
                                         db='land_registry_portal',
                                         charset='utf8mb4',
                                         cursorclass=pymysql.cursors.DictCursor
                                     )
            return connection
        
        except:
            print("Connection was not established!")
        
    def insert_db(self, query, args=()):
        
        try:
            connection = self.getConnection()
            
            cursor = connection.cursor()
            cursor.execute(query, args)
     
            connection.commit() 
            connection.close()
        except:
            print("Error in Insert operation!")
        
    
    def select_db(self, query, args=()):
        #try :
        connection = self.getConnection()
        cursor = connection.cursor()

        cursor.execute(query, args)
        result = cursor.fetchall()

        connection.close()
        return result
        #except:
        print("Error in Select operation!")
            
            
    def update_db(self, query, args=()):
        try :
            connection = self.getConnection()
            cursor = connection.cursor()
            
            cursor.execute(query, args)
             
            connection.commit() 
            connection.close()
        except:
            print("Error in update query!")
            
            
    def delete_db(self, query, args=()):
        try :
            connection = self.getConnection()
            cursor = connection.cursor()
             
            cursor.execute(query, args)
             
            connection.commit() 
            connection.close()
        except:
            print("Error in delete query!")   

#db_obj = Land_Registry_Portal()
#db_obj.insert_db('insert into land_registry_portal.tbl_advanced_encryption_standard values (%s, %s)',(2,'yMz5a_GRUu6ZF-6YmxL9ki-Wd29K44_avPTVnDNsVTM='))
#db_obj.delete_db('delete from land_registry_portal.tbl_advanced_encryption_standard where property_id=%s;',(3))

