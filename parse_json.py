import requests
import json
from urllib.parse import urlparse

# Feed taken from https://github.com/tsopenteam/gundem
URL = "https://raw.githubusercontent.com/tsopenteam/gundem/refs/heads/master/gundem.json"

def check_add_link(dict, link, add_sub_links=True):
    parsed_url = urlparse(link)
    hostname = parsed_url.hostname
    path = parsed_url.path

    if hostname in dict:
        # If hostname exist, add path into sub_urls list
        if add_sub_links == True:
            dict[hostname]['sub_urls'].append(link)
        dict[hostname]['count'] += 1
    else:
        # Create new JSON format for hostname
        if add_sub_links == True:
            dict[hostname] = {
                "count": 1,
                "sub_urls": [link]
            }
        else:
            dict[hostname] = {
                "count": 1
            }

def process_links(json_file, add_sub_links=False):
    overall_links_dict = {}
    each_year_links_dict = {}
    year = 0

    for each_podcast in json_file["list"]:
        if (int(each_podcast["year"]) != int(year)):
            year = each_podcast["year"]
            each_year_links_dict[year] = {}

        for each_content in each_podcast["content"]:
            if each_content["contentLink"] != []:
                for each_link in each_content["contentLink"]:
                    check_add_link(overall_links_dict, each_link, add_sub_links)
                    check_add_link(each_year_links_dict[year], each_link, add_sub_links)
    return overall_links_dict, each_year_links_dict

def save_to_json(url_dict, json_path):
    sorted_urls = dict(sorted(url_dict.items(), key=lambda item: item[1]['count'], reverse=True))

    data = {"urls": sorted_urls}

    with open(json_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)


def get_json(test_mode=False):
    if test_mode == False:
        json_req = requests.get(URL)
        #print(json_req.text)

        json_format = json.loads(json_req.text)
        #print(json_file)
        return json_format
    else:
        with open("test_data/test.json", "r+", encoding="utf8") as json_req:
            data = json.load(json_req)
            #print(data)
            return data

def get_parse_and_save(test_mode=False, add_sub_links=False):
    json_file = get_json(test_mode=test_mode)
    overall_links = {}
    each_year_links = {}

    overall_links, each_year_links = process_links(json_file, add_sub_links)

    # Create artifact files
    save_to_json(overall_links, "out/overall.json")
    for each_year in each_year_links:
        save_to_json(each_year_links[each_year], "out/year_{}.json".format(each_year))

# # Added for testing purposes, should not be run in project
# if __name__ == '__main__':
#     get_parse_and_save(test_mode=True)
