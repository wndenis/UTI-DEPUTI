import wikipedia
import requests
import shutil

from bs4 import BeautifulSoup

def save_image(id, full_name):
    wikipedia.set_lang("ru")
    search_results = wikipedia.search(full_name, results=1)

    # if needed, check more articles in future
    result = search_results[0]
    normalized_name = result.replace(",", "")
    
    if normalized_name == full_name:
        page = wikipedia.page(result)
        page_req = requests.get(page.url)
        
        soup = BeautifulSoup(page_req.text, features="html.parser")
        portrait_container = soup.find("td", {"class": "infobox-image"})
        if portrait_container:
            portrait = portrait_container.find("img")
            if portrait:
                portrait_url = "https:" + portrait["src"]
        
        response = requests.get(portrait_url, stream=True)
        with open(f"static/faces/person_{id}.jpg", "wb") as local_file:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, local_file)
            return True
        del response
