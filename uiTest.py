import tkinter as tk
import os
from tkinter import ttk
from tkinter import filedialog, messagebox

import mosiac_script as script

def select_input_directory():
    folder_selected = filedialog.askdirectory()
    if not folder_selected:
        return
   

    # Check the first sub-directory
    subdirs = [d for d in os.listdir(folder_selected) if os.path.isdir(os.path.join(folder_selected, d))]
    if subdirs:
        first_subdir = os.path.join(folder_selected, subdirs[0])
        if not check_paths(first_subdir):
            messagebox.showerror("Error", "اختبار الملف اللي داخله الملفات فيها example/vricon_raster_1over30asec/dsm/data")
            return
    else:  
         messagebox.showerror("Error", "اختبار الملف اللي داخله الملفات فيها example/vricon_raster_1over30asec/dsm/data")
         return
        

    input_folder_entry.delete(0, tk.END)
    input_folder_entry.insert(0, folder_selected)

def select_output_directory():
    folder_selected = filedialog.askdirectory()
    output_folder_entry.delete(0, tk.END)
    output_folder_entry.insert(0, folder_selected)
def check_paths(base_path):
    required_paths = [
        "vricon_raster_1over30asec/dsm/data",
        "vricon_raster_1over30asec/dtm/data"
    ]
    for path in required_paths:
        if not os.path.exists(os.path.join(base_path, path)):
            return False
    return True    

def run_mosaic():
    input_folder = input_folder_entry.get()
    output_folder = output_folder_entry.get()
    number_of_bands = number_of_bands_dropdown.get()
    pixel_types_value= pixel_type_dropdown.get()
    root.destroy()
    script.mosiac_to_raster(input_folder,output_folder,number_of_bands,pixel_types_value)



    

root = tk.Tk()
root.title("Mosaic to New Raster")

# Input rasters directory
ttk.Label(root, text="Select the Directory with the list of directories to process:").grid(row=0, column=0, sticky='w', padx=10, pady=5)
input_folder_entry = ttk.Entry(root, width=50)
input_folder_entry.grid(row=0, column=1, padx=10, pady=5)
ttk.Button(root, text="Browse", command=select_input_directory).grid(row=0, column=2, padx=10, pady=5)

# Output location directory
ttk.Label(root, text="Output Folder (where the mosaics will be):").grid(row=1, column=0, sticky='w', padx=10, pady=5)
output_folder_entry = ttk.Entry(root, width=50)
output_folder_entry.grid(row=1, column=1, padx=10, pady=5)
ttk.Button(root, text="Browse", command=select_output_directory).grid(row=1, column=2, padx=10, pady=5)

# Pixel type
ttk.Label(root, text="Pixel Type:").grid(row=2, column=0, sticky='w', padx=10, pady=5)
pixel_types = ["8_BIT_UNSIGNED", "8_BIT_SIGNED", "16_BIT_UNSIGNED", "16_BIT_SIGNED", "32_BIT_UNSIGNED", "32_BIT_SIGNED", "32_BIT_FLOAT", "64_BIT"] 
pixel_type_dropdown = ttk.Combobox(root, values=pixel_types, state='readonly')
pixel_type_dropdown.grid(row=2, column=1, padx=10, pady=5)

# Number of bands
ttk.Label(root, text="Number of Bands:").grid(row=3, column=0, sticky='w', padx=10, pady=5)
number_of_bands_values = ["1", "2", "3", "4", "5"]
number_of_bands_dropdown = ttk.Combobox(root, values=number_of_bands_values, state='readonly')
number_of_bands_dropdown.grid(row=3, column=1, padx=10, pady=5)

# Execute button
ttk.Button(root, text="Start", command=run_mosaic).grid(row=4, columnspan=3, pady=20)

root.mainloop()
