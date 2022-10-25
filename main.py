import requests
import json
import csv
from bs4 import BeautifulSoup
from helpers import read_config
from variables import MAIN_URL


class Categories:
    def __init__(self, config: dict):
        self.config = config
        self.categories = self._get_categories()
        
    def _get_categories(self):
        '''
        Get categories tree
        return list
        format [{
            name: str,
            id: str,
            sub_categories: [
                {name: str, id: str}, ...
            ]
               }, ...]
        '''
        categories_tree = []
        html = requests.get(MAIN_URL).text
        soup = BeautifulSoup(html, features="html.parser")
        categories_html = soup.find_all('li', attrs={'class': 'lev1'})

        for cat_html in categories_html:
            category_tree = {
                            'name': None, 
                            'id': None, 
                            'sub_categories': []
                            }

            cat_a_element = cat_html.find('a', attrs={'class': 'catalog-menu-icon'})
            cat_id = self._get_id(cat_a_element['href'])
            cat_name = cat_a_element['title']
            category_tree.update({'name': cat_name.replace(',',''), 'id': cat_id})
            
            sub_popup = cat_html.find('div', attrs={'class': 'popup-items-inner'})
            sub_a_elements = sub_popup.find_all('a')
            for sub_a in sub_a_elements:
                sub_id = self._get_id(sub_a['href'])
                sub_name = sub_a.contents[0]
                category_tree['sub_categories'].append({'name': sub_name.replace(',',''), 'id': sub_id})
            categories_tree.append(category_tree)
        return categories_tree

    def _get_id(self, uri: str):
        return uri.split('/')[-2]
        

class CategoriesSaver:
    def __init__(self, categories: Categories, config: dict):
        self.config = config
        self.categories = categories.categories

    def save(self):
        with open(f'{self.config["output_directory"]}/categories.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['name', 'id', 'parent_id']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()

            for cat in self.categories:
                writer.writerow({'name': cat['name'], 'id': cat['id'], 'parent_id': ''})
                for sub in cat['sub_categories']:
                    writer.writerow({'name': sub['name'], 'id': sub['id'], 'parent_id': cat['id']})
    