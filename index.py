from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import csv
from time import sleep
import random
from setuptools import ssl_support

# Login information
user_name = ""
password = ""

# User information
following_list = []
followers_list = []

# page users
users_on_current_page = []

# URL
url = "https://www.instagram.com/accounts/login/?source=auth_switcher"


# Driver
drive = None

# Class bot
class bot:

    def __init__(self, url, UN, PW):
        # Class variables
        self.url = url
        self.username = UN
        self.password = PW
        self.drive = drive
        self.currentURL = self.url

        # BeautifulSoup
        self.soup = None
        self.get_content = None
        self.list_Of_account_on_current_page = []

    # Takes the source code from the website and transform it to the beautifulsoup
    def get_request_and_content(self, current_url):
        self.currentURL = current_url
        self.soup = BS(self.currentURL, "lxml")

    def find_all_users_current_page_and_check(self):

        for userLinks in self.soup.find_all("a", href=True, title=True):

            if(userLinks.text not in following_list):
                users_on_current_page.append(userLinks.text)


        self.check_user(users_on_current_page)

    def check_user(self, list):

        for user in list:
            sleep(0.5)
            self.drive.get("https://www.instagram.com/" + user + "/")
            try:
                parent = self.drive.find_element_by_class_name("k9GMp ")

                user_amount_followers = parent.find_element_by_css_selector("li:nth-child(2) .g47SY ").text
                user_amount_following = parent.find_element_by_css_selector("li:nth-child(3) .g47SY ").text

                print("Followers: " +user_amount_followers)
                print("Following: " +user_amount_following)

            except:
                print("Something went wrong...")


            print(self.drive.current_url)

    # Find your own followers
    def check_own_followers(self):
        self.drive.get("https://www.instagram.com" + "/" + user_name + "/")
        following_a = self.drive.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[3]/a")
        following_a.click()
        sleep(2)

        scro1ler_container = self.drive.find_element_by_xpath('/html/body/div[4]/div/div[2]')

        sleep(2)

        my_followers = int(self.drive.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span").text)

        for scroller in range(int(my_followers/2)):
            self.drive.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scro1ler_container)
            sleep(random.randint(0, 2 * my_followers)/1600)
            print("<-- INSIDE SCROLLER -->")

        print(" <-- DONE -->")

        self.get_request_and_content(self.drive.page_source)

        for followers in self.soup.find_all(class_="FPmhX notranslate _0imsa"):
             name_of_follower = followers['title']
             following_list.append(str(name_of_follower))

             with open("myFollowers.csv", mode="w") as myFollowers_file:
                myFollowers_writer = csv.writer(myFollowers_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

                myFollowers_writer.writerow(["Following, Followers"])
                for insert_csv in following_list:
                    myFollowers_writer.writerow([insert_csv])

   # function that logs in the account
    def login(self):
        # Makes the webdrive
        self.drive = webdriver.Firefox()
        self.drive.get(self.url)
        self.drive.implicitly_wait(10)

        # finds the attribues, which has username and password as a value
        userNameInput = self.drive.find_element_by_name("username")
        passwordInput = self.drive.find_element_by_name("password")

        userNameInput.clear()
        passwordInput.clear()

        # Sends the username and password to the input box
        userNameInput.send_keys(user_name)
        passwordInput.send_keys(password)

        # clicks on the login button
        login_button = self.drive.find_element_by_xpath("/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div[4]/button/div")
        self.drive.implicitly_wait(10)
        login_button.click()

        # clicks on the pop up side
        self.drive.implicitly_wait(10)
        NoNotefication = self.drive.find_element_by_xpath("/html/body/div[4]/div/div/div[3]/button[2]")
        NoNotefication.click()

    # main
    def main_(self):
        self.drive.get("https://www.instagram.com/")
        sleep(1)
        self.get_request_and_content(self.drive.page_source)
        sleep(0.5)
        self.find_all_users_current_page_and_check()






bot_1 = bot(url, user_name, password)
bot_1.login()
bot_1.check_own_followers()
bot_1.main_()




