#!-*- coding: utf8 -*-
from selenium import webdriver
import random
import time
import os


class Forms:
    def __init__(self):
        self.url = 'https://forms.gle/5aUdsK1TfkTDwJzg8'
        self.path = os.path.abspath(os.getcwd() + os.sep + os.pardir + '/dependencies/chromedriver.exe')
        self.driver = webdriver.Chrome(self.path)

        self.f_list = open('/Users/brunopaes/Documents/OneDrive/Acadêmico/ESPM/Misc/05.4 - Python_Playground/Scripts/Scraper/Data/first_names.txt', 'r', encoding='utf-8').read().split(',')
        self.l_list = open('/Users/brunopaes/Documents/OneDrive/Acadêmico/ESPM/Misc/05.4 - Python_Playground/Scripts/Scraper/Data/last_names.txt', 'r', encoding='utf-8').read().split(',')

        self.mail_sulfix = [
            '{}{}@gmail.com',
            '{}{}@hotmail.com',
            '{}{}@yahoo.com',
            '{}{}@bol.com'
        ]

    def access_page(self):
        self.driver.get(self.url)

    def generate_random_names(self):
        f_name = random.choice(self.f_list)
        l_name = random.choice(self.l_list)

        return f_name.strip(' '), l_name.strip(' ')

    def fill_form(self):
        f_name = self.generate_random_names()[0]
        l_name = self.generate_random_names()[1]

        name = self.driver.find_element_by_xpath('//*[@id="mG61Hd"]/div/div[2]/div[2]/div[1]/div/div[2]/div/div[1]/div/div[1]/input')
        name.send_keys('{} {}'.format(f_name, l_name))

        sulfix = random.choice(self.mail_sulfix)

        mail = self.driver.find_element_by_xpath('//*[@id="mG61Hd"]/div/div[2]/div[2]/div[2]/div/div[2]/div/div[1]/div/div[1]/input')
        mail.send_keys(sulfix.format('{}{}'.format(f_name, l_name), random.randint(1, 999)))

        address = self.driver.find_element_by_xpath('//*[@id="mG61Hd"]/div/div[2]/div[2]/div[3]/div/div[2]/div[1]/div[2]/textarea')
        address.send_keys('Rua Joaquim Távora 1240')

        # time_ = random.randint(1, 20)
        # time.sleep(time_)
        time.sleep(4)

        submit = self.driver.find_element_by_xpath('//*[@id="mG61Hd"]/div/div[2]/div[3]/div[1]/div/div/content/span')
        submit.click()

    def __call__(self, *args, **kwargs):
        while True:
            self.access_page()
            self.fill_form()


if __name__ == '__main__':
    Forms()()
