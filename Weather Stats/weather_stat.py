from csv import DictReader
import re
from datetime import datetime
from tkinter import *
from tkinter import ttk, messagebox

import numpy as np
import matplotlib
from matplotlib.dates import date2num, num2date
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import \
    (FigureCanvasTkAgg, NavigationToolbar2Tk)


class Weather_statistics:

    def __init__(self, master):
        list_datetime, list_barpress = [],[]
        datetime_re = re.compile(r'[\d]{2,4}')
        for year in range(2012, 2016):
            filename = 'Environmental_Data_Deep_Moor_{0}.txt'.format(year)
            print ('Loading {0}'.format(filename))
            for row in DictReader(open(filename, 'r'), delimiter='\t'):
                list_barpress.append(float(row['Barometric_Press']))
                list_datetime.append(date2num(datetime(*list(map(int, datetime_re.findall(row['date       time    ']))))))

        self.datetime_arr = np.array(list_datetime)
        self.barpress_arr = np.array(list_barpress)

        master.title('Weather statistics')
        master.resizable(True, True)
        master.state('zoomed')

        matplotlib.rc('font', size=18)
        fig = Figure()
        fig.set_facecolor((0,0,0,0))
        self.a = fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(fig, master)
        self.canvas.draw()
        toolbar_frame = ttk.Frame(master)
        toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        toolbar.update()
        toolbar_frame.pack(side=TOP, fill=X, expand=1)
        self.canvas._tkcanvas.pack(fill=BOTH, expand=1)

        controls_frame = ttk.Frame(master)
        controls_frame.pack()

        ttk.Label(controls_frame, text = 'Start', font='Arial 18 bold').grid(row=0,  column=0, pady=5)
        ttk.Label(controls_frame, text = '(YYYY-MM-DD HH:MM:SS)', font='Courier 12').grid(row=1, column=0, padx=50, sticky='s')
        self.start = StringVar()
        ttk.Entry(controls_frame, width = 19, textvariable=self.start, font='Courier 12').grid(row=2, column=0, sticky='n')
        self.start.set(str(num2date(self.datetime_arr[0]))[0:19])

        ttk.Label(controls_frame, text = 'End', font='Arial 18 bold').grid(row=0, column=1, pady=5)
        ttk.Label(controls_frame, text = '(YYYY-MM-DD HH:MM:SS)', font='Courier 12').grid(row=1, column=1, padx=50, sticky='s')
        self.end = StringVar()
        ttk.Entry(controls_frame, width = 19, textvariable=self.end, font='Courier 12').grid(row=2, column=1, sticky='n')
        self.end.set(str(num2date(self.datetime_arr[-1]))[0:19])

        ttk.Button(controls_frame, text='Update', command=self._update).grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Style().configure('TButton', font = 'Arial 18 bold')

        self._update()

    def _update(self):

        try:
            start_ = date2num(datetime(*list(map(int, re.findall(r'[\d]{1,4}', self.start.get())))))
            end_ = date2num(datetime(*list(map(int, re.findall(r'[\d]{1,4}', self.end.get())))))
        except Exception as e:
            messagebox.showerror(title='Invalid Date Values', message=e)
            return

        start_idx = np.searchsorted(self.datetime_arr, start_)
        end_idx = np.searchsorted(self.datetime_arr, end_)

        if end_idx <= start_idx:
            messagebox.showerror(title='Invalid Input Values',
                            message='End Date must be after Start Date')
            return

            # calculate slope value
        dy = self.barpress_arr[end_idx] - self.barpress_arr[start_idx]
        dt = self.datetime_arr[end_idx] - self.datetime_arr[start_idx]
        slope = dy / dt

            # plot data & slope line
        self.a.clear()
        self.a.plot_date(self.datetime_arr[start_idx:end_idx],
                             self.barpress_arr[start_idx:end_idx], linewidth=2)
        self.a.plot([self.datetime_arr[start_idx], self.datetime_arr[end_idx]],
                    [self.barpress_arr[start_idx], self.barpress_arr[end_idx]],
                    color='k', linestyle='-', linewidth=2)
        self.a.set_ylabel('Barometric Pressure (inHg)')
        self.a.set_xlabel('Date')

        color = "green" if slope > 0 else 'red'
        text_x = self.datetime_arr[start_idx] + (self.datetime_arr[end_idx] - self.datetime_arr[start_idx])/2
        text_y = self.barpress_arr[start_idx] + (self.barpress_arr[end_idx] - self.barpress_arr[start_idx])/2
        self.a.text(text_x, text_y, '{0:.6f} inHg/day'.format(slope),
                    fontsize=16, horizontalalignment='center',
                    bbox=dict(facecolor=color))

        self.canvas.draw()

def main():
    root = Tk()
    app = Weather_statistics(root)
    root.mainloop()

if __name__ == "__main__": main()