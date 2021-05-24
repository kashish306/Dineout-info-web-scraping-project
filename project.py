import requests
from bs4 import BeautifulSoup
import pandas
import argparse
import connect

parser = argparse.ArgumentParser()
parser.add_argument("--page_max", help="enter no. of pages to be parsed: ", type=int)
parser.add_argument("--dbname", help="enter teh db name: ", type=str)

args = parser.parse_args()

dineout_url = "https://www.dineout.co.in/pune-restaurants/welcome-back?p="
page_max = args.page_max
scraped_info_list = []
connect.connect(args.dbname)


for page in range(1, page_max):
    req = requests.get(dineout_url + str(page))
    content= req.content

    s = BeautifulSoup(content, "html.parser")
    all_dineout_locations = s.find_all("div", {"class":"restnt-card restaurant"})

    for location in all_dineout_locations:
        location_dict = {}
        #location_dict["name"] = location.find("a", {"href":"/pune/"}).text
        location_dict["location"] = location.find("div", {"class":"restnt-info cursor"}).text
        location_dict["details"] = location.find("div", {"class":"detail-info"}).text
        location_dict["totaloffers"] = location.find("li", {"class":"ellipsis"}).text
        #location_rating = location.find("div", {"class":"restnt-rating-widget"}).text

        try:
            location_dict["offerdetails"] = location.find("div", {"class":"offers-info-wrap"}).text
        except AttributeError:
            location_dict["offerdetails"] = None

        #parent_cuisines_list = location.find("div",{"class":"detail-info"})
        #cuisines_list = []
        #for cuisine in parent_cuisines_list.find_all("span",{"class":"double_line-ellipsis"}):
            #cuisines_list.append(cuisine.find("a",{"data-w-onclick":"stopClickPropagation|w1-restarant"}).text)
        #location_dict["cuisines"] = ', '.join(cuisines_list)

        scraped_info_list.append(location_dict)
        connect.insert_into_table(args.dbname, tuple(location_dict.values()))

        #print(location_address,location_name,location_totaloffers,location_offerdetails,cuisines_list)
dataFrame = pandas.DataFrame(scraped_info_list)
#dataFrame.to_csv("Dineout.csv")
connect.get_info(args.dbname)
