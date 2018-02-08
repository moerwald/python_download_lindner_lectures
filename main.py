import requests
from bs4 import BeautifulSoup
import urllib.parse
import time
from progress.bar import Bar
import os

if __name__ == "__main__":

    # Create download folder
    download_folder = "downloaded_pdfs"
    if not os.path.exists(f"./{download_folder}"):
        os.mkdir(download_folder)

    # Fetch main page, including the links we want to download
    main_url = "https://www.ict.tuwien.ac.at/lva/384.081/infobase/"
    modules = "module.html"

    joined_main_url = urllib.parse.urljoin(main_url, modules)
    print(f"Downloading pdfs from: {joined_main_url}")

    response = requests.get(joined_main_url) # Get the main site
    soup = BeautifulSoup(response.text, "html.parser")

    links = soup.select("a") # Fetch all link elements from the HTML response
    links_to_download = [l["href"] for l in links if "pdf (view)" in l] # We only want to download the PDFs with two slides per page

    for link in Bar("Downloading").iter(links_to_download):
        pdf_name = link
        pdf_url = urllib.parse.urljoin(main_url, pdf_name)
        response_including_pdf = requests.get(pdf_url)

        # Store the received binary data
        with open(f"{download_folder}/{pdf_name}", mode="wb") as file:
            file.write(response_including_pdf.content)
        time.sleep(2) # Don't send GET-requests to fast

    # Print summary
    downloaded ="\r\n     ".join(links_to_download)
    print("Summary of downloaded files:")
    print(downloaded)