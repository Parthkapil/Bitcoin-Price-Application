import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import matplotlib.animation as animation
from matplotlib import style
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker

import tkinter as tk
from tkinter import ttk

import urllib
import pandas as pd
import numpy as np
import json
import numpy.core._methods
import numpy.lib.format

LARGE_FONT=("Verdana", 12)
MID_FONT=("Verdana", 10)
SMALL_FONT=("Verdana", 8)
style.use("fivethirtyeight")

f = plt.figure()

exchage = "BTC-e"
DatCounter = 9000


lightColor = "#00A3E0"
darkColor = "#183A54"
chartLoad = True


def loadChart(run):
	global chartLoad

	if run == "start":
		chartLoad = True
	elif run == "stop":
		chartLoad = False

def tutorial():
	
	def page2():
		tut.destroy()
		tut2 = tk.Tk()

		def page3():
			tut2.destroy()
			tut3 = tk.Tk()

			tut3.wm_title("part 3")

			label = ttk.Label(tut3, text="YOU CAN CLICK ON THE RESUME/PAUSE MENU TO STOP THE \n GRAPH TO BE LIVE .", font=MID_FONT)
			label.pack(side="top", fill="x", pady=10)
			b1 = ttk.Button(tut3, text="Done", command=tut3.destroy)
			b1.pack()
			tut3.mainloop()

		label = ttk.Label(tut2, text="YOU CAN CLICK IN THE EXCHANGE MENU AND CHOOSE FROM \n WHICH EXCHANGE YOU WANT THE CHART TO BE DISPLAYED", font=MID_FONT)
		label.pack(side="top", fill="x", pady=10)
		b1 = ttk.Button(tut2, text="Next", command=page3)
		b1.pack()
		tut2.mainloop()

	tut = tk.Tk()
	tut.wm_title("Tutorial")
	label = ttk.Label(tut, text="What do you need help with?", font=MID_FONT)
	label.pack(side="top", fill="x", pady=10)
	b1 = ttk.Button(tut, text="OVERVIEW OF THE APPLICATION", command=page2)
	b1.pack()
	b2 = ttk.Button(tut, text="How do i trade with this client?", command= lambda: popupmsg("Not completed yet."))
	b2.pack()
	b3 = ttk.Button(tut, text="Indicator Questions/Help ", command=lambda: popupmsg("Not completed yet."))
	b3.pack()

	tut.mainloop()


def changeExchange(toWhat, pn):
	global exchage
	global DatCounter
	global programName

	exchage = toWhat
	programName = pn
	DatCounter = 9000


def popupmsg(msg):
	popup = tk.Tk()
	popup.wm_title("!")
	label = ttk.Label(popup, text=msg, font=MID_FONT)
	label.pack(side="top", fill="x", pady=10)
	B1 = ttk.Button(popup,text="okay", command= popup.destroy)
	B1.pack()
	popup.mainloop()



def animate(i):
	global refreshRate
	global DatCounter

	if chartLoad:
		try:
			if exchage == "BTC-e":
				a = plt.subplot2grid((6,4), (0,0), rowspan=5, colspan=4)
				a2 = plt.subplot2grid((6,4), (5,0),sharex=a, rowspan=1, colspan=4)

				dataLink = "https://wex.nz/api/3/trades/btc_usd?limit=2000"
				data = urllib.request.urlopen(dataLink)
				data = data.read().decode("utf-8")
				data = json.loads(data)        

				data = data["btc_usd"]
				data = pd.DataFrame(data)

				data["datestamp"] = np.array(data['timestamp']).astype("datetime64[s]")
				allDates = data["datestamp"].tolist()

				buys = data[data.type=="bid"].copy()   
				buyDates = (buys["datestamp"]).tolist()


				sells = data[data.type=="ask"].copy()
				sellDates = (sells["datestamp"]).tolist()

				volume = data["amount"]

				a.clear()

				a.plot_date(buyDates, buys["price"], lightColor, label="BUYS")
				a.plot_date(sellDates,sells["price"],darkColor, label="SELLS")

				a2.fill_between(allDates, 0, volume, facecolor=darkColor)

				a.xaxis.set_major_locator(mticker.MaxNLocator(5)) #prints dates in tilted style
				a.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M:%S"))
				plt.setp(a.get_xticklabels(), visible = False)

				a.legend(bbox_to_anchor=(0, 1.02, 1, .102), loc=3,
						ncol=2, borderaxespad=0)	
				title = "BTC-e\nLast price:-"+str(data["price"][0])	
				a.set_title(title)

			elif exchage == "Bitstamp":
				a = plt.subplot2grid((6,4), (0,0), rowspan=5, colspan=4)
				a2 = plt.subplot2grid((6,4), (5,0),sharex=a, rowspan=1, colspan=4)

				dataLink = "https://www.bitstamp.net/api/transactions"
				data = urllib.request.urlopen(dataLink)
				data = data.read().decode("utf-8")
				data = json.loads(data)        

				data = pd.DataFrame(data)

				data["datestamp"] = np.array(data['date'].apply(int)).astype("datetime64[s]")
				dateStamp = data["datestamp"].tolist()

				volume = data["amount"].apply(float).tolist()

				a.clear()

				a.plot_date(dateStamp, data["price"], lightColor, label="BUYS")
				

				a2.fill_between(dateStamp, 0, volume, facecolor=darkColor)

				a.xaxis.set_major_locator(mticker.MaxNLocator(5)) #prints dates in tilted style
				a.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M:%S"))
				plt.setp(a.get_xticklabels(), visible = False)

				a.legend(bbox_to_anchor=(0, 1.02, 1, .102), loc=3,
						ncol=2, borderaxespad=0)

				title = "BITSTAMP \nLast price:-"+str(data["price"][0])	
				a.set_title(title)

			elif exchage == "Bitfinex":
				a = plt.subplot2grid((6,4), (0,0), rowspan=5, colspan=4)
				a2 = plt.subplot2grid((6,4), (5,0),sharex=a, rowspan=1, colspan=4)

				dataLink = "https://api.bitfinex.com/v1/trades/btcusd?limit=2000"
				data = urllib.request.urlopen(dataLink)
				data = data.read().decode("utf-8")
				data = json.loads(data)        

				data = pd.DataFrame(data)

				data["datestamp"] = np.array(data['timestamp']).astype("datetime64[s]")
				allDates = data["datestamp"].tolist()

				buys = data[data.type=="buy"].copy()   
				buyDates = (buys["datestamp"]).tolist()


				sells = data[data.type=="sell"].copy()
				sellDates = (sells["datestamp"]).tolist()

				volume = data["amount"].apply(float).tolist()

				a.clear()

				a.plot_date(buyDates, buys["price"], lightColor, label="BUYS")
				a.plot_date(sellDates,sells["price"],darkColor, label="SELLS")

				a2.fill_between(allDates, 0, volume, facecolor=darkColor)

				a.xaxis.set_major_locator(mticker.MaxNLocator(5)) #prints dates in tilted style
				a.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M:%S"))
				plt.setp(a.get_xticklabels(), visible = False)

				a.legend(bbox_to_anchor=(0, 1.02, 1, .102), loc=3,
						ncol=2, borderaxespad=0)	
				title = "BITFINEX\nLast price:-"+str(data["price"][0])	
				a.set_title(title)

		except Exception as e:
			print("Failed because of: ",e)



class seaofBTCapp(tk.Tk):
	def __init__(self,*args,**kwargs):

		tk.Tk.__init__(self,*args,**kwargs)    #args can take any number of variables as input
												#kwargs can take any number of dicttionaries as input
		tk.Tk.iconbitmap(self, default="Paomedia-Small-N-Flat-Bitcoin.ico") #change the icon from feather to anything
		tk.Tk.wm_title(self, "BITCOIN PRICE APPLICATION") #change the title of gui from tk to any thing


		container=tk.Frame(self)
		container.pack(side="top", fill='both', expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		
	
		menubar = tk.Menu(container)

		#File Menu
		filemenu = tk.Menu(menubar, tearoff=1)
		filemenu.add_command(label="Save settings", command=lambda: popupmsg("Not Supported yet"))
		filemenu.add_separator()
		filemenu.add_command(label="Exit", command= quit)
		menubar.add_cascade(label="File", menu=filemenu)

		#Exchange menu
		exchageChoice = tk.Menu(menubar, tearoff=1)
		exchageChoice.add_command(label="BTC-e", 
								     command=lambda: changeExchange("BTC-e","btce"))
		exchageChoice.add_command(label="Bitfinex", 
								     command=lambda: changeExchange("Bitfinex","bitfinex"))
		exchageChoice.add_command(label="Bitstamp", 
								     command=lambda: changeExchange("Bitstamp","bitstamp"))
		
		menubar.add_cascade(label="Exchange", menu=exchageChoice)

		

		#Trading menu
		tradeButton = tk.Menu(menubar, tearoff=1)
		tradeButton.add_command(label="Manual Trading",
									command= lambda: popupmsg("not supported yet"))
		tradeButton.add_command(label="Automated Trading",
									command= lambda: popupmsg("not supported yet"))
		tradeButton.add_separator()
		tradeButton.add_command(label="Quick Buy",
									command= lambda: popupmsg("not supported yet"))
		tradeButton.add_command(label="Quick Sell",
									command= lambda: popupmsg("not supported yet"))
		tradeButton.add_separator()
		tradeButton.add_command(label="Set-up Qick Buy/Sell",
									command= lambda: popupmsg("not supported yet"))

		menubar.add_cascade(label="Trading", menu=tradeButton)

		#Resume/Pause client menu
		startStop = tk.Menu(menubar, tearoff=1)
		startStop.add_command(label="Resume", 
								command= lambda: loadChart('start'))
		startStop.add_command(label="Pause", 
								command= lambda: loadChart('stop'))
		menubar.add_cascade(label="Resume/Pause client", menu=startStop)

		#Help menu

		helpmenu = tk.Menu(menubar, tearoff=0)
		helpmenu.add_command(label="Tutorials", command= tutorial)
		menubar.add_cascade(label="Help", menu=helpmenu)



		tk.Tk.config(self, menu=menubar)

		self.frames={}

		for F in (StartPage, BTCe_page):

			frame = F(container, self)

			self.frames[F] = frame

			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame(StartPage)

	def show_frame(self, cont):

		frame = self.frames[cont]
		frame.tkraise()


class StartPage(tk.Frame):
	
	def __init__(self, parent, controller):
		
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text=('''ALPHA BITCOIN TRADING APPLICATION
use at your own risk. There is 
no warranty.'''), font=LARGE_FONT)
		label.pack(padx=10, pady=10)

		button1 = ttk.Button(self, text="AGREE", 
									command= lambda: controller.show_frame(BTCe_page) )
		button1.pack()

		button2 = ttk.Button(self, text="DISAGREE", 
									command= controller.destroy )
		button2.pack()


class PageOne(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label=tk.Label(self, text="Page One ", font=LARGE_FONT)
		label.pack(padx=10, pady=10)

		button1 = ttk.Button(self, text="Go Back To Start Page",
										command=lambda: controller.show_frame(StartPage))
		button1.pack()

class BTCe_page(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label=tk.Label(self, text="GRAPH PAGE ", font=LARGE_FONT)
		label.pack(padx=10, pady=10)

		button1 = ttk.Button(self, text="Go Back To Start Page",
										command=lambda: controller.show_frame(StartPage))
		button1.pack()


		canvas = FigureCanvasTkAgg(f, self)
		canvas.show()
		canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

		toolbar = NavigationToolbar2TkAgg(canvas, self)
		toolbar.update()
		canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)



app = seaofBTCapp()
app.geometry("1280x720")
ani = animation.FuncAnimation(f, animate, interval = 10000)
app.mainloop()
