import subprocess
import json
import re
from pfpscraper import PFPScraper

def clean_output(output):
    new_string = output[:-4]
    return new_string.split(",\r\n")

def extract_links(output):
    links = []
    for item_json in output:
        item = json.loads(item_json)
        url_property = item["data"]
        site_name = url_property.split()[0]
        pattern = r'<SFURL>(https?://[^<]+)</SFURL>'
        site_url = re.findall(pattern, url_property)
        if site_url == []:
            site_url = ["No URL found"]
        data = {"site_name": site_name, "site_url": site_url[0]}
        links.append(data)
    return links

def run_command(command):
    stdout = subprocess.check_output(command, shell=True).decode('utf-8')
    new_array = clean_output(stdout)
    links = extract_links(new_array)
    results = PFPScraper().scrape(links)
    if results:
        return results    
    


    
