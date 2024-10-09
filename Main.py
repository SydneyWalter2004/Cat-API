from dotenv import load_dotenv
import os
import requests
import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO

load_dotenv()

api_key = os.getenv('API_KEY')

# Function to fetch a random cat image from the Cat API
def get_cat_image():
    url = "https://api.thecatapi.com/v1/images/search"
    headers = {
        "x-api-key": api_key
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        img_url = data[0]['url']
        return img_url
    else:
        return None

def update_cat_image():
    img_url = get_cat_image()
    if img_url:
        # Fetch the image from the URL
        img_response = requests.get(img_url)
        img_data = img_response.content
        
        # Convert the image to a format Tkinter can use
        img = Image.open(BytesIO(img_data))
        img = img.resize((400, 400)) 
        img_tk = ImageTk.PhotoImage(img)
        
        cat_image_label.config(image=img_tk)
        cat_image_label.image = img_tk 

root = tk.Tk()
root.title("Random Cat Image Generator")

cat_image_label = tk.Label(root)
cat_image_label.pack(padx=20, pady=20)

generate_button = tk.Button(root, text="Generate Random Cat Image", command=update_cat_image)
generate_button.pack(pady=10)

update_cat_image()

root.mainloop()
