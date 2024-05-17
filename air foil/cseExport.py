from tkinter import filedialog
import csv
class Export:
    def __init__(self, code, x_coords =0, y_coords =0):
        self.directory = filedialog.askdirectory()
        self.code = code
        self.x_coords = x_coords
        self.y_coords = y_coords
        
    def export_data(self):
        if self.directory:
            self.file_name = f"{self.directory}/{self.code}_coords_data.csv"
            with open(self.file_name, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([f"{self.code}"])
                writer.writerow(["x","y"])
                writer.writerows(zip(self.x_coords,self.y_coords))
                print(self.file_name)
        else:
            pass
