import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
API_KEY = os.getenv('API_KEY')

# Function to get image of the specified cat breed
def get_cat_image(breed_name=None):
    headers = {
        'x-api-key': API_KEY
    }

    if breed_name:
        # Fetch breeds and find matching breed_id
        breeds_url = "https://api.thecatapi.com/v1/breeds"
        response = requests.get(breeds_url, headers=headers)
        if response.status_code != 200:
            messagebox.showerror("Error", "Failed to fetch breeds.")
            return
        
        breeds = response.json()
        breed_id = None
        for breed in breeds:
            if breed_name.lower() in breed['name'].lower():
                breed_id = breed['id']
                break
        
        if not breed_id:
            messagebox.showerror("Error", f"No breed found for '{breed_name}'.")
            return
        
        url = f"https://api.thecatapi.com/v1/images/search?breed_ids={breed_id}"
    else:
        # Get a random cat image if no breed is specified
        url = "https://api.thecatapi.com/v1/images/search"

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        image_url = response.json()[0]['url']
        show_image(image_url)
    else:
        messagebox.showerror("Error", "Failed to retrieve cat image.")

# Function to display the image
def show_image(image_url):
    response = requests.get(image_url)
    img_data = response.content
    img = Image.open(BytesIO(img_data))
    img = img.resize((400, 400), Image.LANCZOS)
    
    img_tk = ImageTk.PhotoImage(img)
    
    label_image.config(image=img_tk)
    label_image.image = img_tk  # Keep reference to avoid garbage collection

# Function to handle the breed search
def search_breed():
    breed_name = entry_breed.get()
    get_cat_image(breed_name)

# Create the main window
root = tk.Tk()
root.title("Cat Image Generator")

# Create search box and label
label_breed = tk.Label(root, text="Enter Cat Breed:")
label_breed.pack()

entry_breed = tk.Entry(root)
entry_breed.pack()

# Create button to generate breed image
button_breed = tk.Button(root, text="Search Cat Breed", command=search_breed)
button_breed.pack()

# Create button for random cat image
button_random = tk.Button(root, text="Generate Random Cat Image", command=lambda: get_cat_image(None))
button_random.pack()

# Label to display the image
label_image = tk.Label(root)
label_image.pack()

# Run the application
root.mainloop()
