
import Server as server

connection = server.create_db_connection("sql10.freesqldatabase.com", "sql10518926", "trpxsFcTJZ", "sql10518926")

reademail = ("""
SELECT usermail FROM users
""")
read = server.read_query(connection, reademail)
c = 0
c = int(0)
for emails in read:
    email = str(emails[c])
    temp2 = ("""ALTER TABLE `{}` ADD `med` VARCHAR(45) NOT NULL AFTER `hora_evento`;""").format(email)
    
    exc = server.execute_query(connection, temp2)