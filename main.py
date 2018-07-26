"""
This is the main program to create the Fred Data Downloader application interface
"""
##---import Tkinter libraries---
from Tkinter import *
import ttk
import tkFileDialog
import tkMessageBox
##------------------------------##
from config import freq_list, FRED_ID_NAME, FRED_FREQUENCY_NAME, APP_NAME, DEFAULT_START_DATE, DEFAULT_END_DATE
from fred_request import *

class App:
	"""
	Tkinter application class definition
	"""
	##------------------Helper Functions-------------------------##
	def __setup_treeview(self, cols):
		"""
		Function to setup the table that displays the query results
		"""

		self.treeview = ttk.Treeview(self.frame)
		self.treeview.grid(row=1, columnspan=3)
		self.treeview['columns'] = cols
		## find the FRED ID column index and Frequency column index in the query table
		self.id_index = cols.index(FRED_ID_NAME)
		self.freq_index = cols.index(FRED_FREQUENCY_NAME)

		## create the heading for all the columns
		for item in cols:
			self.treeview.heading(item, text=item)
			self.treeview.column(item, anchor='center', width=100)
		## set the double click action onDoubleClick for each row
		self.treeview.bind("<Double-1>", self.OnDoubleClick)

	def __loadTable(self):
		""" 
		Function to load the query result to the treeview frame defined above
		"""
		data = [tuple(x) for x in self.__search_result.to_records(index=False)]
		for i in data:
			self.treeview.insert('', END, text=i[self.id_index], values=i) 


	## initializer
	def __init__(self, master):
		"""
		Function to initialize the Tkinter application class. 

		In other words, draw all the necessary widgets on the Tkinter canvas
		"""
		self.frame = Frame(master)
		self.frame.grid()
		## Add a quit button
		self.button = Button(self.frame, text="QUIT", fg="red", command=self.frame.quit)
		self.button.grid(row=0, column=0)
		## Add a search box
		self.search_text = Entry(self.frame)
		self.search_text.grid(row=0, column=1)
		self.search_text.bind('<Return>', self.search)
		self.search_text.focus_set()

		## Add a search button
		self.search_button = Button(self.frame, text="Search", command=self.search)
		self.search_button.grid(row=0, column=2)

		## Initialize two empty frames
		## treeview is the query result table
		self.treeview = None
		## dialog_frame is the download section
		self.dialog_frame = None

		##--------------- On click implementation------------------------##

	def search(self, event=None):
		""" 
		Function to define the onClick action of the search button and <Return> action on the search textbox
	
		"""
		## hide the download dialog frame if it has been created
		if self.dialog_frame is not None:
			self.dialog_frame.grid_forget()

		## Query from FRED series search webservice 
		dq = fred_data_query(self.search_text.get())
		dq.search()
		self.__search_result = dq.get_result()

		if self.__search_result is not None and len(self.__search_result) !=0:
			## exist query results then we will populate the treeview
			if self.treeview is None:
				self.__setup_treeview(tuple(self.__search_result.columns))
			else:
				self.treeview.grid_forget()
				self.__setup_treeview(tuple(self.__search_result.columns))
			self.__loadTable()
		else:
			## if there is no query result, then return a label saying there is no data
			if self.treeview !=None:
				self.treeview.grid_forget()
			self.treeview = Label(self.frame, text="No data related to the search key words!").grid(row=1, columnspan=3)

	def clear(self):
		"""
		Function to clear download section
		"""
		self.dialog_frame.grid_forget()

	def OnDoubleClick(self, event):
		"""
		Function to create the download section 
		"""

		## retrieve the selected item from the query list
		item = self.treeview.selection()[0]
		self.__download_series_id = self.treeview.item(item, "text")

		## if a download sectioon is present, remove it before creating a new one
		if self.dialog_frame != None:
			self.dialog_frame.grid_forget()

		## make a download frame below the query result
		self.dialog_frame = Frame(self.frame)
		self.dialog_frame.grid(row=2, columnspan=3) 
		Label(self.dialog_frame, text="Please input your dates and frequency to download!").grid(row=0, columnspan=3, sticky='w')
		Label(self.dialog_frame, text='Start Date (YYYY-MM-DD):').grid(row=1, column=0, sticky='w') 
		self.start_date = Entry(self.dialog_frame, background='white', width=24)  
		self.start_date.grid(row=1, column=1, sticky='w')  
		self.start_date.focus_set() 
		Label(self.dialog_frame, text='END Date (YYYY-MM-DD):').grid(row=2, column=0, sticky='w') 
		self.end_date = Entry(self.dialog_frame, background='white', width=24)  
		self.end_date.grid(row=2, column=1, sticky='w') 
		Label(self.dialog_frame, text='Frequency:').grid(row=3, column=0, sticky='w')
		self.var = StringVar(self.dialog_frame)
		self.var.set(self.treeview.item(item, "value")[self.freq_index])
		self.freq_menu = OptionMenu(self.dialog_frame, self.var, *freq_list.keys()).grid(row=3, column=1, sticky='w')
		## Download button
		Button(self.dialog_frame, text='Download', command=self.download).grid(row=4, column=0, sticky='w')
		## Cancel button
		Button(self.dialog_frame, text='Cancel', command=self.clear).grid(row=4, column=1, sticky='w')

	def download(self):
		""" 
		Function to download the FRED data and call the save file box
		"""
		start_date = self.start_date.get()
		end_date = self.end_date.get()
		freq = freq_list[self.var.get()]
		if start_date == '':
			## set as default
			start_date = DEFAULT_START_DATE
		if end_date == '':
			## set as default
			end_date = DEFAULT_END_DATE

		### download the selected FRED data
		dd = fred_data_downloader(self.__download_series_id, 
								  observation_start_date=start_date, 
								  observation_end_date=end_date,
								  freq=freq)
		dd.retrieve()
		data = dd.get_data()

		## call the save as filename dialog and get the path
		filename = tkFileDialog.asksaveasfilename(filetypes=[('CSV File', '*.csv')], 
												title = "Save file", confirmoverwrite=False, ) 
		try:
			## if there is data and file path is correct, then save the data as csv
			data.to_csv(filename, index=False)
			self.dialog_frame.grid_forget()
		except:
			tkMessageBox.showinfo("Error", "Incorrect Path or No Data so either change your input or file path")

root = Tk()
root.title(APP_NAME)
app = App(root)
root.mainloop()
root.destroy()