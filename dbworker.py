import sqlite3


class DBWorker:
	def __init__(self):
		self.dbname = 'database.db'
		self.connected = False

	def open_connection(self):
		if not self.connected:
			self.conn = sqlite3.connect(self.dbname, check_same_thread = False)
			self.cursor = self.conn.cursor()
			self.connected = True

	def close_connection(self):
		if self.connected:
			self.conn.close()
			self.connected = False

	def create_table(self):
		self.open_connection()
		query = """CREATE TABLE IF NOT EXISTS stoks
				(user_id integer primary key,
				 company text,
				 dat text)"""

	def insert_company(self, id, company):
		self.open_connection()
		query = "SELECT * FROM stoks WHERE user_id == {id}".format(id = id)
		self.cursor.execute(query)
		result = self.cursor.fetchone()
		if result == None:
			query = "INSERT INTO stoks (user_id, company) VALUES({id},'{company}')".format(id = id, company = str(company).upper())
			self.cursor.execute(query)
			self.conn.commit()
		else:
			query = "SELECT company FROM stoks WHERE user_id = {id}".format(id = id)
			self.cursor.execute(query)
			prev_company = set(self.cursor.fetchone()[0].split(','))
			prev_company.add(company.upper())
			query = "UPDATE stoks SET company = '{company}' WHERE user_id = {id}".format(company = prev_company, id = id)
			self.cursor.execute(query)
			self.conn.commit()
		self.close_connection()

	def delete_company(self, id, company):
		self.open_connection()
		query = "SELECT company FROM stoks WHERE user_id = {id}".format(id = id)
		self.cursor.execute(query)
		ex_company = self.cursor.fetchone()[0].split(',')
		try:
			ex_company.remove(company.upper())
			query = "UPDATE stoks SET company = '{company}' WHERE user_id = {id}".format(company = ','.join(ex_company), id = id)
			self.cursor.execute(query)
			result = 'Succses'
		except:
			result = 'Error'
		self.conn.commit()
		self.close_connection()
		return result
		

	def all_company(self, id):
		self.open_connection()
		query = "SELECT company FROM stoks WHERE user_id = {id}".format(id = id)
		self.cursor.execute(query)
		companys = self.cursor.fetchone()[0].split(',')
		self.close_connection()
		return companys

	def all_data(self):
		self.open_connection()
		query = "SELECT user_id, dat FROM stoks WHERE dat <> 'NULL'" 
		self.cursor.execute(query)
		dates = self.cursor.fetchall()
		self.close_connection()
		return dates
		

	def insert_date(self, id, dat):
		self.open_connection()
		query = "UPDATE stoks SET dat = '{dat}' WHERE user_id = {id}".format(dat = dat, id = id)
		print(query)
		self.cursor.execute(query)
		self.conn.commit()
		self.close_connection()
		
