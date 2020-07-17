import sqlite3

class DBWorker:
	def __init__(self):
		self.dbname = 'database.db'
		self.conn = sqlite3.connect(self.dbname, check_same_thread = False)
		self.cursor = self.conn.cursor()

	def close(self):
		self.conn.close()

	def create_table(self):
		query = """CREATE TABLE IF NOT EXISTS stoks
				(user_id integer primary key,
				 company text,
				 dat text)"""
		self.cursor.execute(query)
		self.conn.commit()

	def append_stoks(self, id, company):
		query = "SELECT company FROM stoks WHERE user_id = {id}".format(id = id)
		self.cursor.execute(query)
		prev_company = cursor.fetchone()
		company = str(prev_company) + "," + str(company)
		query = "UPDATE stoks SET company = {company} WHERE user_id = {id}".format(company = company, id = id)
		self.cursor.execute(query)
		self.conn.commit()

	def insert_string(self, id, company):
		query = "SELECT * FROM stoks WHERE user_id == {id}".format(id = id)
		self.cursor.execute(query)
		result = self.cursor.fetchone()
		if result == None:
			query = "INSERT INTO stoks (user_id, company) VALUES({id},'{company}')".format(id = id, company = company)
			print(query)
			self.cursor.execute(query)
			self.conn.commit()
		else:
			query = "SELECT company FROM stoks WHERE user_id = {id}".format(id = id)
			self.cursor.execute(query)
			prev_company = self.cursor.fetchone()[0]
			print(prev_company)
			company = str(prev_company) + "," + str(company)
			query = "UPDATE stoks SET company = '{company}' WHERE user_id = {id}".format(company = company, id = id)
			print(query)
			self.cursor.execute(query)
			self.conn.commit()

	def delete_company(self, id, company):
		query = "SELECT company FROM stoks WHERE user_id = {id}".format(id = id)
		self.cursor.execute(query)
		ex_company = self.cursor.fetchone()[0]
		try: 
			ex_company.remove(company)
			query = "UPDATE stoks SET company = {company} WHERE user_id = {id}".format(company = ex_company, id = id)
			self.cursor.execute(query)
			result = 'Succses'
		except:
			result = 'Error'
		self.conn.commit()
		return result
