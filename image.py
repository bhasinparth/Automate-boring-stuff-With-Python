from io import BytesIO
import urllib
import urllib.request
import tkinter as tk
from PIL import Image, ImageTk
import requests
from bs4 import BeautifulSoup

location=input("Enter the Location ")
url = "https://www.shutterstock.com/search?searchterm="+location+"&search_source=base_search_form&category=Holidays"
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html5lib')
quote_html = soup.findAll('div', attrs = {'class': 'img-wrap'})
quote=quote_html[0]
quote
quote.img['src']
img_url="https:"+quote.img['src']


root = tk.Tk()
with urllib.request.urlopen(img_url) as u:
    raw_data = u.read()
im = Image.open(BytesIO(raw_data))
image = ImageTk.PhotoImage(im)
label = tk.Label(image=image)
label.pack()
root.mainloop()
