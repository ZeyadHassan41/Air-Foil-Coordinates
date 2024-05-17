# import libraries
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json

# import madules
import dataScraper   
import searchEngine
import cseExport

# Airfoil Database URL
URL = "https://m-selig.ae.illinois.edu/ads/coord_database.html"

# UI Standard
root_size= "1440x960"
root_bg = "#CDDEEE"
font = ("inter", 16)
button_bg = "#90ADC6"
input_bg = "#ABC7E3"
xpadding = 100
ypadding = 24
font_color = "#333652"

with open('data.json', 'r') as json_file:
    data = json.load(json_file)
    json_file.close()

# Set TK window
root = tk.Tk()
root.title("Airfoil Coords")
root.geometry(root_size)
root.configure(bg= root_bg)

# Plot Canvas 
def plot_coordinates(x_coords, y_coords):
    # Clear any previous plot
    plt.clf()
    # Plotting the coordinates
    plt.plot(x_coords, y_coords)
    plt.xlabel('X Coordinates')
    plt.ylabel('Y Coordinates')
    plt.title('Airfoil Coordinates')
    canvas.draw()
# Plot custom
fig, ax = plt.subplots(figsize=(12, 4))
plt.xlim(0, 1)
plt.ylim(-1, 1)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=1, column=5, rowspan=10, columnspan=8 )

#margin label
xtop =tk.Label(root,bg=root_bg)
xtop.grid(row=0,column=2, columnspan=12)
ytop =tk.Label(root,bg =root_bg,  text="    ")
ytop.grid(row=1,rowspan=10,column=0)

# Search box UI
placeholder = "Search"
entry = tk.Entry(root,fg= font_color, font=font, width=18,
                  bg= input_bg, borderwidth=1 )
entry.grid(row=1, column=1, columnspan= 3)

#search btn Function
def search_enter():
    x_lst.delete(0, tk.END)
    y_lst.delete(0, tk.END)
    global searched_code
    global x_coords
    global y_coords
    searched_code = entry.get()
    search = searchEngine.Search(data,searched_code)
    output =search.search_helper()
    if isinstance(output, list):
        for i in range(len(output)):
            if i % 2 == 0: 
                x_lst.insert(tk.END, output[i])
            else:
                y_lst.insert(tk.END, output[i])
    elif isinstance(output, dict):
        for x_point in output["x"]:
            x_lst.insert(tk.END, x_point)
            x_coords = [float(x) for x in x_lst.get(0, tk.END)]
        for y_point in output["y"]:
            y_lst.insert(tk.END, y_point)
            y_coords = [float(y) for y in y_lst.get(0, tk.END)]
        plot_coordinates(x_coords, y_coords)
    entry.delete(0, tk.END)

#search btn
def enter_key_press(event):
    # Function to handle key press events
    key = event.keysym
    if key == "Return":
        search_enter()
root.bind("<KeyPress>", enter_key_press)
ser_image = tk.PhotoImage(file="web.png").subsample(16,16)
search_btn = tk.Button(root,image=ser_image, bg=button_bg)
search_btn = tk.Button(root,image=ser_image, bg=button_bg,command=search_enter)
search_btn.grid(row=1,column=4)

# X and Y lists Or Suggesttions
x_lst = tk.Listbox(root,bg=input_bg, height=50)
x_lst.grid(row=2, column=1, columnspan=2)
y_lst = tk.Listbox(root,bg=input_bg, height=50)
y_lst.grid(row=2, column=3, columnspan=2)

# export Button
def export_btn_fun():
    export =cseExport.Export(searched_code, x_coords, y_coords)
    export.export_data()

export_btn = tk.Button(root, text="Export", fg= font_color,
                  font=font, 
                  padx=26, pady= 10, 
                  bg= button_bg, borderwidth=1, command=export_btn_fun)
export_btn.grid(row=10, column=1,columnspan= 2)


# DataScraper (updatebtn) function
def upate_data():
      scraper = dataScraper.AirfoilDataScraper(URL)
      scraper.scrape_data()
      scraper.save_data_as_json('data.json')

update_btn = tk.Button(root, text="Update", fg= font_color,
                  font=font, 
                  padx=24, pady= 10, 
                  bg= button_bg, borderwidth=1, command=upate_data)
update_btn.grid(row=10, column=3,columnspan= 2)


#continue running the window
root.mainloop()