import csv
import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import asksaveasfile
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np


def interpola_ramp(x1,x2,y1,y2):
    tmp_y = []
    tmp_x = []
    for x in range(int(x1),int(x2)):
        y = y1 + ((x - x1)/(x2 - x1)) * (y2 - y1)
        tmp_y.append(y)
        tmp_x.append(x)
    return tmp_x,tmp_y


def crea_ramp_asc(start_time,durata,start_ftp,end_ftp,start_plot):
    x_ramp = []
    y_ramp = []
    parziale = {'start':0, 'end':0, 'ftp_start':0, 'ftp_end':0}
    start_parz = start_time
    num_parz = end_ftp - start_ftp + 1
    durata_parz = round(durata / num_parz, 2)
    ramp = []
    for ftp in range(start_ftp,end_ftp+1):
        parziale = {'start':0, 'end':0, 'ftp_start':0, 'ftp_end':0}
        parziale['start'] = start_parz
        parziale['end'] = start_parz + durata_parz
        parziale['ftp_start'] = ftp
        parziale['ftp_end'] = ftp
        x_ramp.append(start_parz)
        y_ramp.append(ftp)
        x_ramp.append(start_parz + durata_parz)
        y_ramp.append(ftp)
        start_parz = start_parz + durata_parz
        ramp.append(parziale)
    return ramp, start_parz, x_ramp, y_ramp
        

def crea_ramp_disc(start_time,durata,start_ftp,end_ftp,start_plot):
    x_ramp = []
    y_ramp = []
    parziale = {'start':0, 'end':0, 'ftp_start':0, 'ftp_end':0}
    start_parz = start_time
    num_parz = start_ftp - end_ftp + 1
    durata_parz = round(durata / num_parz, 2)
    ramp = []
    for ftp in reversed(range(end_ftp,start_ftp+1)):
        parziale = {'start':0, 'end':0, 'ftp_start':0, 'ftp_end':0}
        parziale['start'] = start_parz
        parziale['end'] = start_parz + durata_parz
        parziale['ftp_start'] = ftp
        parziale['ftp_end'] = ftp
        x_ramp.append(start_parz)
        y_ramp.append(ftp)
        x_ramp.append(start_parz + durata_parz)
        y_ramp.append(ftp)
        start_parz = start_parz + durata_parz
        ramp.append(parziale)
    return ramp, start_parz, x_ramp, y_ramp


def apri_csv():
    label_saved['text'] = ""
    file_path = filedialog.askopenfilename(initialdir="./", filetypes=[("csv files", "*.csv")])
    file_name = (file_path.split('/'))[-1]
    file_no_ext = (file_name.split("."))[0]
    global nome_file_output
    nome_file_output = file_no_ext
    open_file.set(f"{file_name} loaded")
    global intervalli
    intervalli = []
    csvfile = open(file_path,"r")
    csv_reader = csv.reader(csvfile, delimiter=',')
    parziale = {'start':0, 'end':0, 'ftp_start':0, 'ftp_end':0}
    start_time = 0
    start_plot = 0
    intestazione = True
    x = []
    y = []
    for row in csv_reader:
        if intestazione:
            intestazione = False
            continue
        start_ftp = int(row[1])
        end_ftp = int(row[2])
        durata = float((row[3].strip('"')).replace(",","."))    # need to clean up the csv downloaded from gsheet
        if start_ftp == end_ftp:
            parziale = {'start':0, 'end':0, 'ftp_start':0, 'ftp_end':0}
            parziale['start'] = start_time
            parziale['end'] = start_time+durata
            parziale['ftp_start'] = start_ftp
            parziale['ftp_end'] = end_ftp
            x.append(start_time)
            y.append(start_ftp)
            x.append(start_time+durata)
            y.append(end_ftp)
            start_time = start_time+durata
            intervalli.append(parziale)
        elif start_ftp<end_ftp:
            ramp,end_time,x_ramp, y_ramp = crea_ramp_asc(start_time, durata, start_ftp, end_ftp, start_plot)
            start_time = end_time
            intervalli = intervalli + ramp
            x = x + x_ramp
            y = y + y_ramp
        else:
            ramp,end_time,x_ramp, y_ramp = crea_ramp_disc(start_time, durata, start_ftp, end_ftp, start_plot)
            start_time = end_time
            intervalli = intervalli + ramp
            x = x + x_ramp
            y = y + y_ramp
        start_plot = start_plot + durata
    visualizza_allenamento(x,y)


def visualizza_allenamento(x,y):
    
    #0-50 grigio | 50-80 blu | 80-90 verde | 90-105 giallo | 105-115 arancio | >115 rosso
    f0 = tk.Frame(master=root)
    f = Figure(figsize=(5,2), dpi=100)
    ax = f.add_subplot(111)
    ax.plot(x, y, alpha=0)
    ax.fill_between(x, y, color='silver', interpolate=True, alpha=1, where=([i < 60 for i in y]))
    ax.fill_between(x, y, color='dodgerblue', interpolate=True, alpha=1, where=([60<=i<75 for i in y]))
    ax.fill_between(x, y, color='forestgreen', interpolate=True, alpha=1, where=([75<=i<90 for i in y]))
    ax.fill_between(x, y, color='gold', interpolate=True, alpha=1, where=([90<=i<=105 for i in y]))
    ax.fill_between(x, y, color='darkorange', interpolate=True, alpha=1, where=([105<i<115 for i in y]))
    ax.fill_between(x, y, color='red', interpolate=True, alpha=1, where=([i>=115 for i in y]))
    canvas = FigureCanvasTkAgg(f, f0)
    canvas._tkcanvas.grid(column=0, row=2,rowspan=3, columnspan=4)
    f0.grid(column=0, row=2,rowspan=3, columnspan=4)
        

def salva_mrc():
    descrizione = text_descr.get('1.0','end')
    nome_file = nome_file_output + ".mrc"
    nome_allenamento = nome_str.get()
    output_mrc = open(nome_file,"w")
    if len(nome_allenamento)>0:
        output_mrc.write(f"[COURSE HEADER]\nVERSION = 2\nUNITS = ENGLISH\nDESCRIPTION = {descrizione}\nFILE NAME = {nome_allenamento}\nMINUTES PERCENT\n[END COURSE HEADER]\n")
    else:
        output_mrc.write(f"[COURSE HEADER]\nVERSION = 2\nUNITS = ENGLISH\nDESCRIPTION = {descrizione}\nFILE NAME = {nome_file}\nMINUTES PERCENT\n[END COURSE HEADER]\n")
    output_mrc.write("[COURSE DATA]\n")
    for segmento in intervalli:
        start = "{:.2f}".format(segmento['start'])
        end = "{:.2f}".format(segmento['end'])
        output_mrc.write(f"{start} {segmento['ftp_start']}\n{end} {segmento['ftp_end']}\n")
    output_mrc.write("[END COURSE DATA]")
    output_mrc.close()
    label_saved['text'] = f"saved {nome_file}"


def enable_save(*args):
    if len(open_file.get())>0:
        button_save.config(state='normal')


intervalli = []
nome_file_output = ""
root = tk.Tk()
root.title("MRC creator")
button_open = tk.Button(root,text="Open CSV", command=apri_csv, font=('Helvetica',12, 'bold'))
open_file = tk.StringVar(root)
open_file.trace("w",enable_save)
label_open_file = tk.Label(master=root, textvariable=open_file)

button_save = tk.Button(root,text="Save .MRC", command=salva_mrc, font=('Helvetica',12, 'bold'))
button_save.config(state='disabled')
label_saved = tk.Label(master=root, text="")

nome_str = tk.StringVar(root)
label_nome = tk.Label(master=root, text="Workout name:")
entry_nome = tk.Entry(root, textvariable=nome_str, width=50)

descr_str = tk.StringVar(root)
label_descr = tk.Label(master=root, text="Workout description:")
text_descr = tk.Text(root, height=10, width=60)

button_open.grid(column=0, row=0)
label_open_file.grid(column=1, row=0)
label_nome.grid(column=0, row=1)
entry_nome.grid(column=1, row=1)
label_descr.grid(column=0, row=5)
text_descr.grid(column=0, row=6, columnspan=2)

button_save.grid(column=0, row=7)
label_saved.grid(column=1, row=7)

root.mainloop()