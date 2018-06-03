#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3
class SQLight:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()
    
    ########################################    User_cat    #####################################################################
    
    def check_id_cat(self,id,cat):
        with self.connection:
            return self.cursor.execute('SELECT count(*) FROM user WHERE message_id = ? and category = ?', (id,cat)).fetchone()[0]

    def check_user(self,id):
        with self.connection:
            return len(self.cursor.execute('SELECT * FROM user WHERE message_id = ?', (id,)).fetchall())>0

    def delete_user_all(self,id):
        with self.connection:
            return self.cursor.execute('DELETE FROM user WHERE message_id = ?', (id,)).fetchall()

    def get_category(self,id):
        """ Получаем все user over category """
        with self.connection:
            return self.cursor.execute('SELECT category FROM user WHERE message_id=?',(id,)).fetchall()

    def add_new_user(self,category,id):
        with self.connection:
            return self.cursor.execute('INSERT INTO user VALUES(?,?)',(category,id,)).fetchall()
    
    def get_user_by_category(self,cat_id):
        with self.connection:
            return self.cursor.execute('SELECT message_id FROM user WHERE category= ?', (cat_id,)).fetchall()
    
    #category,message_id

    ########################################    LAST LINK    #####################################################################
    def get_last_links(self):
        with self.connection:
            return self.cursor.execute('SELECT link FROM last_link').fetchall()
    def check_last_link(self,cat):
        with self.connection:
            return len(self.cursor.execute('SELECT link FROM last_link WHERE category = ?', (cat,)).fetchall()[0][0])>0
    def get_last_link(self,cat):
        with self.connection:
            return self.cursor.execute('SELECT link FROM last_link WHERE category = ?', (cat,)).fetchall()[0][0]
    
    def update_last_link(self,cat,new_link):
        with self.connection:
            return (self.cursor.execute("""UPDATE last_link SET link = ? WHERE category= ? """,(new_link,cat)))

    ###################################################################################################################            
    
    def add_last_link(self,cat,link):
        with self.connection:
            return self.cursor.execute('INSERT INTO last_link VALUES(?,?)',(cat,link)).fetchall()
    
    ########################################    User info    #####################################################################
   
    def add_user_info(self,id,date_created):
        with self.connection:
            return self.cursor.execute('INSERT INTO user_info VALUES(?,"","","","",?,"",1)',(id,date_created)).fetchall()
    
    def add_new_user_info(self,id,name,surname,username,date_create):
        with self.connection:
            return self.cursor.execute('INSERT INTO new_user_info VALUES(?,?,?,?,?,1,"")',(id,name,surname,username,date_create))
    
    
    ##########################################################  IMPORT #####################################################
    def import_user(self,id,name,surname,username,date_create):
        with self.connection:
            return self.cursor.execute('INSERT INTO import VALUES(?,?,?,?,?,1,"")',(id,name,surname,username,date_create))
    def get_last_row_import(self):
        with self.connection:
            data = self.cursor.execute('SELECT * FROM import ORDER BY row_id ASC LIMIT 1').fetchall()
            if len(data)>0:
                return (list(data[0]))
            return False
    def delete_data(self):
        with self.connection:
            return self.cursor.execute('DELETE FROM import WHERE row_id = (SELECT MIN(row_id) FROM import)')
    def update_post(self,cat,post):
        with self.connection:
            return self.cursor.execute('UPDATE last_link set link = ? WHERE category = ?',(post,cat))

    #db.add_new_user_info(message.from_user.id,message.from_user.first_name,message.from_user.last_name,message.from_user.username,now_time)
    ###################################################################################################################
    
    def check_following(self,id):
        with self.connection:
            return self.cursor.execute('SELECT follow from user_info WHERE message_id = ?',(id)).fetchall()
    
    def unfollow(self,id):
        with self.connection:
            return self.cursor.execute("""UPDATE user_info SET follow = ? WHERE message_id = ? """,(0,id))
    
    def follow(self,id):
        with self.connection:
            return (self.cursor.execute("""UPDATE user_info SET follow = ? WHERE message_id = ? """,(1,id)))
    
    ###################################################################################################################            
    def check_user_info(self,id):
        with self.connection:
            return len(self.cursor.execute('SELECT * FROM user_info WHERE message_id = ?', (id,)).fetchall())>0
    
    def check_new_user_info(self,id):
        with self.connection:
            return len(self.cursor.execute('SELECT * FROM new_user_info WHERE id = ?', (id,)).fetchall())>0
    
    def delete_user_info_all(self,id):
        with self.connection:
            return self.cursor.execute('DELETE FROM user_info WHERE message_id = ?', (id,)).fetchall()
    
    def delete_new_user_info_all(self,id):
        with self.connection:
            return self.cursor.execute('DELETE FROM new_user_info WHERE id = ?', (id,)).fetchall()
    ###############ADMIN#############

    def delete_admin(self,username):
        with self.connection:
            return self.cursor.execute('DELETE FROM admin WHERE username = ?', (username,))
    
    def add_admin(self,username):
        with self.connection:
            return self.cursor.execute('INSERT INTO admin VALUES(?)', (username,))
    def get_admin_list(self):
        with self.connection:
            data = self.cursor.execute('SELECT username from admin').fetchall()
            admin_list=[]
            for admin in data:
                admin_list.append(admin[0])
            return admin_list
    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()
