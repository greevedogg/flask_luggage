# #Depricated....I will most likely be using sqlite, instead of MySQL and PyMySQL
# #See models.py & config.py for sqlite and sqlalchemy configuration

# CREATE TABLE `users` (
#     `id` int(11) NOT NULL AUTO_INCREMENT,
#     `username` varchar(255) COLLATE utf8_bin NOT NULL,
#     `pin` int(4) COLLATE utf8_bin NOT NULL,
#     PRIMARY KEY (`id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
# AUTO_INCREMENT=1 ;

# CREATE TABLE 'luggagetable' (
#     'id' int(11) NOT NULL AUTO_INCREMENT,
#     'ticket' int(11) NOT NULL,
#     'name' varchar(255) COLLATE utf8_bin NOT NULL,
#     'location' varchar(255) COLLATE utf8_bin NOT NULL,
#     'bagcount' int(11) NOT NULL,
#     'loggedinby' FOREIGN KEY(id='users') #gets entered when luggage is stored. i know this is wrong, need to fix
#     'timein' datetime(now hh:mm) #i know this is wrong, need to fix
#     'loggedoutby' FOREIGN KEY(id='users') #gets entered when luggage is retreived
#     'timeout' datetime(now hh:mm) #timestamp from when luggage is picked up
#     'comment' varchar(255),
#     PRIMARY KEY ('id')
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
# AUTO_INCREMENT=1 ;

# import pymysql.cursors

# # Connect to the database
# connection = pymysql.connect(host='localhost',
#                              user='user',
#                              password='password',
#                              db='db',
#                              charset=utf8mb4',
#                              cursorclass=pymysql.cursors.DictCursor)
                             
# try:
#     with connection.cursor() as cursor:
#         # Create a new record
#         sql = "INSERT INTO 'luggagetable' ('ticket', 'name', 'location', 'bagcount', 'loggedinby', 'timein') VALUES (%i, %s, %s, %i, %s, %d)"
#         cursor.execute(sql, ('12345', 'jones', '34C', '5', 'jhowell', '4:20'))
        
#     # connection is not autocommit by default. So you must commit to save
#     # your changes.
#     connection.commit()
    
#     with connection.cursor() as cursor:
#         # Read a single record
#         sql = "SELECT 'ticket', 'name', 'location' FROM 'luggagetable' WHERE 'ticket'=%i OR 'name'=%s"
#         cursor.execute(sql, ('name@something',))
#         result =cursor.fetchone()
#         print(result)
# finally:
#     connection.close()
