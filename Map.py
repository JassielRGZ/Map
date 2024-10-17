import pandas as pd
from PIL import Image, ImageDraw, ImageTk
import tkinter as tk

df = pd.read_excel('ExportData.xlsx')
location_names = df['Location']  # Assuming the column is named 'Location'

###Map Coordinates

coordinates = {
    "Women's Hospital": (600, 2450),
    'Emergency Room': (1850, 1900),
    # Add more location names and their coordinates

}

# Load campus map
campus_map = Image.open('Map.jpg')
draw = ImageDraw.Draw(campus_map)

# Load the pin icon image
pin_icon = Image.open('pinicon.png')
pin_icon = pin_icon.resize((350, 350))  # Resize the pin icon if necessary

# Define a pin (image instead of red circle)
for location in location_names:
    if location in coordinates:
        x, y = coordinates[location]
        # Paste the pin icon directly at the location, using the pin_icon as the mask to handle transparency
        campus_map.paste(pin_icon, (x, y), pin_icon)  # Notice the third argument for mask

# Save the map with pins
campus_map.save('campus_map_with_pins.jpg')

### Displaying in a Python Window
# Create a Tkinter window
root = tk.Tk()
root.title("Campus Map with Pins")

# Load the image with pins
campus_map = Image.open('campus_map_with_pins.jpg')
campus_map = campus_map.resize((1000, 800))  # Resize if necessary
img = ImageTk.PhotoImage(campus_map)

# Create a label to display the image
label = tk.Label(root, image=img)
label.pack()

# Start the GUI loop
root.mainloop()

