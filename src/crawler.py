#!-*- coding: utf8 -*-
from selenium.webdriver.common.keys import Keys
from sklearn.naive_bayes import MultinomialNB
from selenium import webdriver
from bs4 import BeautifulSoup

import pandas
import time
import nltk
import os


class Message:
    """This class access the whatsapp, seek for unread messages and replies it.

    """
    def __init__(self):
        self.path = os.path.abspath(os.getcwd() + os.sep + os.pardir + '/dependencies/chromedriver.exe')
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--user-data-dir=./User_Data')
        self.driver = webdriver.Chrome(self.path, options=self.options)
        self.url = 'https://web.whatsapp.com'

        self.driver.get('http://web.whatsapp.com')

        self.nltk = NLTK(MultinomialNB)

        self.librarian = self.nltk.cleaning_dict()
        self.model = self.nltk.fit(self.librarian)

    def get_unread(self):
        """This function gets the unread chats and click on it.

        Returns
        -------

        """
        try:
            unread_chat = self.driver.find_element_by_class_name('P6z4j')
            unread_chat.click()

            time.sleep(5)

            self.get_last_message()

        except Exception as e:
            e.args
            pass

    def get_source_code(self):
        """This function gets the source code from whatsapp web and retunrn it.

        Returns
        -------
        BeautifulSoup(html, 'html5lib') : bs4.BeautifulSoup
            Parsed html.

        """
        html = self.driver.page_source
        return BeautifulSoup(html, 'html.parser')

    def get_last_message(self):
        """This functions get the last unread message.

        Returns
        -------

        """
        soup = self.get_source_code()

        lst_msg = soup.find_all('span', {'class': 'selectable-text invisible-space copyable-text'})
        try:
            msg = lst_msg[-1].text

            input_box = self.driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
            input_box.send_keys(self.nltk.pred(self.model, msg, self.librarian))
            input_box.send_keys(Keys.ENTER)

        except Exception as e:
            e.args
            pass

    def __call__(self, *args, **kwargs):
        """Main function

        Parameters
        ----------
        args
        kwargs

        Returns
        -------

        """
        print('Starting API')
        input()

        while True:
            self.get_unread()


class NLTK:
    """This class make the natural language processing for a given text input.

    """
    def __init__(self, model=MultinomialNB):
        self.dataFrame = pandas.read_csv(os.path.abspath(os.getcwd() + os.sep + os.pardir + '/data/dataset.csv'), sep=';')
        self.stopwords = nltk.corpus.stopwords.words("portuguese")
        self.stemmer = nltk.stem.RSLPStemmer()

        self.df_values = self.dataFrame['phrase']
        self.df_tags = self.dataFrame['answer']

        self.lowerText = self.df_values.str.lower()
        self.df_token = [nltk.tokenize.word_tokenize(i) for i in self.lowerText]

        self.model = model()

    # Used in main function
    def cleaning_dict(self):
        """This function creates and fill a set of stem valid words.

        Returns
        -------
        valid_words : dict
            Dictionary with stem valid words.

        """
        dictionary = set()
        for i in self.df_token:
            valid_words = [self.stemmer.stem(nxDF) for nxDF in i if nxDF not in self.stopwords]
            dictionary.update(valid_words)

        tuples = zip(dictionary, range(len(dictionary)))

        return {word: i for word, i in tuples}

    # Used in fit
    def vectorise(self, txt, librarian):
        """This function vectorises a text input.

        Parameters
        ----------
        txt : str
            Text input.
        librarian : dict
            Dictionary with stem valid words.
        Returns
        -------
        vectorized_array : list
            List with the frequency of the Text input.

        """
        vectorized_array = [0] * len(librarian)
        for word in txt:
            if len(word) > 0:
                stem = self.stemmer.stem(word)
                if stem in librarian:
                    position = librarian[stem]
                    vectorized_array[position] += 1

        return vectorized_array

    def fit(self, librarian):
        """This function fits the chosen model.

        Parameters
        ----------
        librarian : dict
            Dictionary with stem valid words.
        Returns
        -------
        model : sklearn.Model
            Fitted model.

        """
        x = [self.vectorise(txt, librarian) for txt in self.df_token]
        y = self.df_tags

        return self.model.fit(x, y)

    def pred(self, model, phrase, librarian):
        """This function makes prediction for the given text input.

        Parameters
        ----------
        model : sklearn.Model
            Fitted model.
        phrase : str
            Inputted text.
        librarian : dict
            Dictionary with stem valid words.
        Returns
        -------
        x[0] : str
            Answer for the given text input.

        """
        phrase_ = self.vectorise(nltk.tokenize.word_tokenize(phrase), librarian)
        x = model.predict([phrase_])

        return x[0]

    def __call__(self, *args, **kwargs):
        """Main function

        Parameters
        ----------
        args
        kwargs

        Returns
        -------

        """
        self.__init__(MultinomialNB)
        librarian = self.cleaning_dict()
        model = self.fit(librarian)

        while True:
            phrase = input('Input a phrase: ')
            print(self.pred(model, phrase, librarian))


if __name__ == '__main__':
    Message().__call__()
