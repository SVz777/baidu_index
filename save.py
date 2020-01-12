from sakura import mysql

# init db
mysql_config = {
    'host': '192.168.0.7',
    'user': 'root',
    'password': 'password',
    'db': 'xxlw'
}

sakura = mysql.connect(**mysql_config)

# table
Baidu = sakura.getModel('baidu')