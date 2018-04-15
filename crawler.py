import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import json
import re

home_page = "https://www.ifood.com.br/delivery/salvador-ba"

restaurant_links = [
    "https://www.ifood.com.br/delivery/salvador-ba/croasonho---salvador-shopping-caminho-das-arvores",
]

categories_map = {
    "Lanches": "123123",
}

for link in restaurant_links:
    restaurant = {}
    chorme = webdriver.Chrome()
    chorme.get(home_page)
    chorme.get(link)

    title = chorme.find_element_by_css_selector('h1.name')
    restaurant["url"] = link
    restaurant["name"] = title.text.strip()

    category_element = chorme.find_element_by_css_selector('div.info-category-price span')
    restaurant["category"] = categories_map[category_element.text.strip()]
    description = chorme.find_element_by_css_selector('div.info-description')
    restaurant["description"] = description.text.strip()

    info_elements = chorme.find_elements_by_css_selector('div#menuContent div.info')
    item_categories_list = []

    for info in info_elements:
      category_obj = {}
      itens_list = []

      item_category_name = info.find_element_by_css_selector('div.results-section h3')
      category_obj["name"] = item_category_name.text.strip()

      itens_list_elements = info.find_elements_by_css_selector('div.results-section div.list li')

      for item_element in itens_list_elements:
        item_obj = {}
        try:
          image_element = item_element.find_element_by_css_selector('div.result div.photo-item img')
          image_url = image_element.get_attribute('src')
          item_obj["image_url"] = image_url
        except:
          item_obj["image_url"] = None

        item_name = item_element.find_element_by_css_selector('div.text-wrap h4')
        item_obj["name"] = item_name.text
        item_description = item_element.find_element_by_css_selector('div.text-wrap p')
        item_obj["description"] = item_description.text.strip()
        try:
          item_price = item_element.find_element_by_css_selector('div.result-actions span span.price-now')
          item_obj["price"] = item_price.text.strip()
        except:
          item_price = item_element.find_element_by_css_selector('div.result-actions span')
          m = re.search('(R\$.*)', item_price.text.strip())
          if m:
            found = m.group(1)
            item_obj["price"] = found

        itens_list.append(item_obj)

      category_obj["itens"] = itens_list
      item_categories_list.append(category_obj)

    restaurant["item_categories"] = item_categories_list

    with open('data.json', 'w') as outfile:
      json.dump(restaurant, outfile)

chorme.quit()
