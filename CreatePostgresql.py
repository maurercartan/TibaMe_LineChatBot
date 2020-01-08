__author__ = 'user'
import os
import psycopg2

class Create_PG_SQL:
    
    def __init__(self):
        # 本地使用資料庫
        # project_name = "news-bot-a"
        # DATABASE_URL = os.popen(f"heroku config:get DATABASE_URL -a {project_name}").read()[:-1]
        
        # 雲端使用資料庫
        self.DATABASE_URL = "postgres://hlanvvnxzkvipq:066670d2118d48d1ce537bbe2eaf6d89f06c2cf99f92e30e3ae6bb55f709addf@ec2-174-129-32-240.compute-1.amazonaws.com:5432/dba4qpfa6mafgt"
        #self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        
    def create_table(self):
        conn = psycopg2.connect(self.DATABASE_URL, sslmode='require')
        sql_cmd = '''CREATE TABLE user_info(
           id serial PRIMARY KEY,
           select_news VARCHAR (50) UNIQUE NOT NULL,
           display_name VARCHAR (100) NOT NULL,
           picture_url VARCHAR (100) UNIQUE NOT NULL,
           status_message VARCHAR (50) UNIQUE NOT NULL,
           user_id VARCHAR (100) UNIQUE NOT NULL,
        );'''
    
        cursor = conn.cursor()
        cursor.execute(sql_cmd)
        conn.commit()
        cursor.close()
        conn.close()
        
    def create_table2(self):
        conn = psycopg2.connect(self.DATABASE_URL, sslmode='require')
        sql_cmd = '''CREATE TABLE news_info(
           id serial PRIMARY KEY,
           news_type VARCHAR (50) UNIQUE NOT NULL,
           news_class VARCHAR (100) NOT NULL,
           news_title VARCHAR (100) UNIQUE NOT NULL,
           news_image VARCHAR (100) UNIQUE NOT NULL,
           news_url VARCHAR (100) UNIQUE NOT NULL,
           news_date VARCHAR (100) UNIQUE NOT NULL
        );'''
    
        cursor = conn.cursor()
        cursor.execute(sql_cmd)
        conn.commit()
        cursor.close()
        conn.close()

    def insert_data(self,myData):
        conn = psycopg2.connect(self.DATABASE_URL, sslmode='require')
        sql_cmd = "INSERT INTO user_info (select_news,display_name,picture_url,status_message,user_id) \
              VALUES ('"+myData[0]+"','"+myData[1]+"','"+myData[2]+"','"+myData[3]+"','"+myData[4]+"')";
        cursor = conn.cursor()
        cursor.execute(sql_cmd)
        conn.commit()
        cursor.close()
        conn.close()

    def update_data(self,user_id,select_news):
        conn = psycopg2.connect(self.DATABASE_URL, sslmode='require')
        sql_cmd = "UPDATE user_info set select_news = '"+select_news+"' where user_id='"+user_id+"'";
        cursor = conn.cursor()
        cursor.execute(sql_cmd)
        conn.commit()
        cursor.close()
        conn.close()

    def select_table(self,sql_cmd):
        conn = psycopg2.connect(self.DATABASE_URL, sslmode='require')
        cursor = conn.cursor()
        cursor.execute(sql_cmd)
        data = []
        while True:
            temp = cursor.fetchone()
            if temp:
                data.append(temp)
            else:
                break
        conn.commit()
        cursor.close()
        conn.close()
        return data

    def update_cmd(self,sql_cmd):
        conn = psycopg2.connect(self.DATABASE_URL, sslmode='require')
        cursor = conn.cursor()
        cursor.execute(sql_cmd)
        conn.commit()
        cursor.close()
        conn.close()
        
    def close(self):
        self.conn.close()

if __name__=="__main__":
    pg = Create_PG_SQL()
    select_news = list(pg.select_table("select * from user_info;"))
    pg.close()
    with open("Select_Database.txt","w",encoding="utf8") as f:
        for i in range(len(select_news)):
            f.write(str(select_news[i])+"\n")
    print(select_news)
    pass
    