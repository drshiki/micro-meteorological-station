import Tkinter as tk;
import tkFont
import time
import BMP180.BMP180_driver as BMP180
import DHT11.DHT11_driver as DHT11
import BH1750.BH1750_driver as BH1750
import MySQLdb

class app(tk.Frame):
	
	items = [
		{'item':'temperature','unit':'*C'},
		{'item':'humidity','unit':'% RH'},
		{'item':'pressure','unit':'hPa'},
		{'item':'sea_level_press','unit':'hPa'},
		{'item':'illuminance','unit':'lx'},
		{'item':'location','unit':' '},
		{'item':'altitude','unit':'m'},
		{'item':'API','unit':''},
		{'item':'rainfall','unit':''}
	]
	def __init__(self,master=None):
		
		tk.Frame.__init__(self, master, width=400,height=300,padx=100,pady=20)
		self.grid_propagate(0)
		
		self.grid()
		#self.createWidgets(v)
	
	def createWidgets(self,dict):
		for i in range(len(self.items)):
			self.add_item_panel(i+1, 0, self.items[i]['item'], self.items[i]['unit'],dict)
			
	def add_item_panel(self, _row, _col, _item, _unit,dict):
		self.item = tk.Label(self, text=_item + ' : ')
		self.item.grid(row=_row, column=_col,sticky=tk.E)
		self.temp_data = tk.Label(self, textvariable=dict[_item])
		self.temp_data.grid(row=_row, column=_col+1)		
		self.unit = tk.Label(self, text=_unit)
		self.unit.grid(row=_row, column=_col+2, sticky=tk.W)


def get_data():
	global data_dict
	conn = MySQLdb.Connection(host="localhost", user="root", passwd="123456",
charset="UTF8")
	conn.select_db('mms')
	cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
	cursor.execute("select * from t_data where item_id = (select max(item_id)from t_data)")
	conn.commit()
	tmp = cursor.fetchall()[0]
	data_dict['humidity'].set(tmp['humidity'])
	data_dict['temperature'].set(tmp['temperature'])
	data_dict['pressure'].set(tmp['pressure'])
	data_dict['sea_level_press'].set(tmp['sea_level_press'])
	data_dict['illuminance'].set(tmp['illuminance'])
	data_dict['API'].set(tmp['api'])
	data_dict['location'].set(0)
	data_dict['altitude'].set(tmp['altitude'])
	data_dict['rainfall'].set(tmp['rainfall'])
	cursor.close()
	conn.close()
	return data_dict

def update_text():
	get_data();
	a.after(3000,update_text)
a = app()

data_dict={'humidity' : tk.IntVar(), 'temperature' : tk.IntVar(), 'pressure' : tk.IntVar(), 'sea_level_press' :tk.IntVar() , 'illuminance' : tk.IntVar(), 'altitude' : tk.IntVar(), 'API' : tk.IntVar(), 'location' : tk.IntVar() , 'rainfall':tk.IntVar()}
get_data()
a.createWidgets(data_dict)
a.master.title('micro-meteorological-station')
update_text()
a.mainloop()

