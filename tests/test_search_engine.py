import pytest
from bs4 import BeautifulSoup
from engine.search_engine import fetch_proxy_list, get_site_data, get_start_point_links_set


class TestEngineClass():

    def setup(self):
        self.start_point = 'yandex.ru'
        self.search_request = 'Star Wars'


    def test_proxy_list_is_list(self):
        lst = fetch_proxy_list()
        print(lst)
        assert isinstance(lst, list)
    

    def test_proxy_list_data_exists(self):
        lst = fetch_proxy_list()
        assert len(lst) > 0
    

    def test_get_site_data_is_soup(self):
        soup = get_site_data(self.start_point)
        assert isinstance(soup, BeautifulSoup)


    def test_get_start_point_links_set(self):
        
        site_data = get_site_data(self.start_point, self.search_request)
        start_point_links = get_start_point_links_set(site_data, self.start_point)
        assert isinstance(start_point_links, set)


    def teardown(self):
        print("This is teardown. All tests are finished")
