import pandas as pd
from PIL import Image, ImageDraw, ImageTk
import tkinter as tk

# Load data from Excel
df = pd.read_excel(r'\\renfs1\homeshares$\rdrgj36\Desktop\Python\ExportData.xlsx')
location_names = df['Location']
ticket_ids = df['Ticket ID']

# Map coordinates along with ticket IDs for each location
coordinates = {
    "Women's Hospital": (650, 230),
    'Emergency Room': (1850, 1900),
    'Medical Office Building': (1240, 525),
    'Plastics and Reconstructive Surgery': (1230, 510),
    'Orthopedic Sports and Therapy Institute Clinic': (1050, 380),
    'Oncology Institute': (630, 200),
    'GME Family Medicine': (940, 550), 
    "Women's Cafeteria": (610, 210),
    'Human Resources': (690, 80),
    'Diabetes and Endocrinology Institute': (910, 200)
    # Add more locations and coordinates as needed
}

# Compile a dictionary with locations as keys and associated Ticket IDs
location_requests = {}
for index, location in location_names.items():
    ticket_id = ticket_ids[index]
    if location in coordinates:
        if location in location_requests:
            location_requests[location].append(ticket_id)
        else:
            location_requests[location] = [ticket_id]

# Load the campus map image
campus_map = Image.open('Map.png')
draw = ImageDraw.Draw(campus_map)

# Load the pin icon image
pin_icon = Image.open('pinicon.png')
pin_icon = pin_icon.resize((50, 50))

# Place the pin icons onto the map
for location, (x, y) in coordinates.items():
    campus_map.paste(pin_icon, (x, y), pin_icon)

# Save the map with pins
campus_map.save('campus_map_with_pins.jpg')

# Function to convert RGB to hex color
def rgb_to_hex(rgb):
    return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'

# Function to show service requests when a pin is clicked
def show_service_requests(location):
    # Create a new top-level window for the pop-up
    popup = tk.Toplevel(root)
    popup.title(f"Service Requests for {location}")
    popup.overrideredirect(True)  # Remove window decorations
    
    # Display the Ticket IDs in the pop-up
    requests = location_requests.get(location, [])
    if requests:
        request_text = "\n".join([f"Ticket ID: {id}" for id in requests])
    else:
        request_text = "No service requests found."

    label = tk.Label(popup, text=request_text, padx=10, pady=10)
    label.pack()

    # Add a close button to the pop-up
    close_button = tk.Button(popup, text="Close", command=popup.destroy)
    close_button.pack(pady=10)

    # Center the pop-up on the screen
    popup.update_idletasks()  # Update "requested size" of the popup
    x = (popup.winfo_screenwidth() // 2) - (popup.winfo_width() // 2)
    y = (popup.winfo_screenheight() // 2) - (popup.winfo_height() // 2)
    popup.geometry(f"+{x}+{y}")  # Move to the center of the screen

    # Function to enable dragging the popup
    def start_drag(event):
        popup.x = event.x
        popup.y = event.y

    def drag(event):
        x = popup.winfo_x() - popup.x + event.x
        y = popup.winfo_y() - popup.y + event.y
        popup.geometry(f"+{x}+{y}")

    # Bind mouse events for dragging
    popup.bind("<Button-1>", start_drag)
    popup.bind("<B1-Motion>", drag)

# Tkinter setup to display the map with clickable pins
root = tk.Tk()
root.title("Campus Map with Pins")

# Load the saved image with pins
campus_map_with_pins = Image.open('campus_map_with_pins.jpg')
campus_map_with_pins = campus_map_with_pins.resize((1000, 800))  # Resize if necessary
img = ImageTk.PhotoImage(campus_map_with_pins)

# Label to display the image
label = tk.Label(root, image=img)
label.pack()

# Create invisible buttons for each pin to make them clickable
for location, (x, y) in coordinates.items():
    # Check if coordinates are within image dimensions
    if 0 <= x < campus_map_with_pins.width and 0 <= y < campus_map_with_pins.height:
        # Adjust button placement to center it over the pin (50x50 pixels)
        btn = tk.Button(root, command=lambda loc=location: show_service_requests(loc), borderwidth=0, highlightthickness=0)
        btn.place(x=x - 25, y=y - 25, width=50, height=50)  # Center button over the pin
        
        # Get the color at the pin location and set the button's background to that color
        color = campus_map_with_pins.getpixel((x, y))
        btn.configure(bg=rgb_to_hex(color), highlightbackground=rgb_to_hex(color))  # Match button color to the map


# Start the GUI loop
root.mainloop()
