from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep
from datetime import date, datetime
from textblob import TextBlob as tb
import re, random, csv
import pycountry
from timeCalc import pushDate
import threading
from selenium.webdriver.common.keys import Keys

# DATE
day_today = date.today().day
month_today = date.today().month
year_today = date.today().year

if(day_today < 10):
    day_today = "0{}".format(day_today)

if(month_today < 10):
    month_today = "0{}".format(month_today)


date_today = "{}/{}/{}".format(day_today,month_today,year_today)

# URL
URL = "https://www.instagram.com/accounts/login/?source=auth_switcher"
URL_s = "https://www.instagram.com"

# COMMON VALUES
XPATH_FOLLOWINGBOX_LEN = "/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span"
XPATH_FOLLOWERSBOX_LEN = "/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span"

# Driver
drive = None


# Class bot
class bot:

    def __init__(self):
        # Class variables
        # MAIN VARIABLES
        self.url = URL
        self.username = None
        self.password = None
        self.drive = drive
        self.source_code = None
        self.dictOfTags = None

        #
        self.followed = 0
        self.liked = 0
        self.maxFollowing = 5
        self.maxLiking = 10
        self.languages = []

        self.commented = 0
        self.commentMax = 3

        # CSV
        self.file = None
        self.followers_old = []
        self.followers_old_name = []
        self.following_old = []
        self.following_old_name = []
        self.list = []

        # login
        self.error_login = False

        # Login_page variables
        self.login_success = False

        # USER INFORMATION
        self.following_list = []
        self.followers_list = []
        self.followers_date = []
        self.following_date = []

        # TAGFINDER
        self.listOfPhotos_t = []
        self.dl = False
        self.boy_activated = None
        self.girl_activated = None

        # BEAUTIFULSOUP
        self.soup = None

    # TAKES THE SOURCE CODE FROM THE WEBSITE AND TRANSFORM IT TO THE BEAUTIFULSOUP
    def get_bs(self, sourcecode):
        self.source_code = sourcecode
        self.soup = BS(self.source_code, "lxml")

    def blockkHandler(self):
        try:
            block_text = self.drive.find_element_by_xpath("/html/body/div[4]/div/div/div[1]/div")
            if(block_text.is_displayed()):
                print("BLOCK HAPPENED")
                return False
        except:
            return True

    # FUNCTION THAT TRIES TO GET THE BIO TEXT AND THE USERNAME OF THE USER
    def checkUser(self):
        language = None
        getName = None
        name = None
        self.drive.implicitly_wait(20)
        try:
            getName = (self.drive.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/div[2]/h1").text).\
                encode("UTF-8").decode()
            language_dec = tb(getName).detect_language()
            language = pycountry.languages.get(alpha_2=language_dec)
            language = language.name
            print("LANGUAGE: ", language)

            # Values for filtering
            start = 0
            end = 0
            breaker = False
            twoWord = False
            name = None

            for n in range(len(getName)):
                if (breaker == False):
                    if (getName[n].isupper()):
                        start = n
                        breaker = True

                elif (getName[n].isupper()):
                    end = n
                    twoWord = True
                    break

            if (twoWord == False):
                end = len(getName)
                name = getName[start:end]
            else:
                name = getName[start:end]

            print("Name: ", name)

        except:
            print("No name wroted")
            name = None

        try:
            language_dec = self.drive.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/div[2]/span").text.encode('UTF-8').decode()
            language_dec = remove_emojis.sub(r"",language_dec)
            print(language_dec)
            language_dec = tb(language_dec).detect_language()
            language = pycountry.languages.get(alpha_2=language_dec)
            language = language.name
            print("LANGUAGE: ", language)
        except:
            language = "None"

        return language, name

    def pauseFunction(actionName):
        sec = 0
        wait_time = 120 # SECONDS

        for _ in range(wait_time):
            sleep(1)
            sec += 1
            print("SEC --> {} ({})".format(sec, actionName))

            if(sec == wait_time):
                if(actionName == "like"):
                    self.like_now = True
                    self.liked = 0
                elif(actionName == "follow"):
                    self.follow_now = True
                    self.followed = 0
                else:
                    self.comment_now = True
                    self.commented = 0

    def pauseCode(self):

        whenPause = "23:30"
        pauseTime = 3600 * 8 # 8 hours

        hour = datetime.now().strftime("%H")
        minute = datetime.now().strftime("%M")

        timeNow = "{}:{}".format(hour,minute)

        if(whenPause == timeNow):
            sleep(pauseTime)

    # HASHTAG FUNCTION. iT GOES TO THE HASHTAG AND LIKING, FOLLOWING
    def tagFinder(self, dict_hashtags, follow, like, languages, girl, boy, comment, commentList):
        self.dictOfTags = dict_hashtags
        self.follow_now = follow
        self.like_now = like
        self.languages = languages
        self.girl_activated = girl
        self.boy_activated = boy

        self.comment_now = comment
        self.commentList = commentList

        lang = None
        name = None
        lang_corr = None
        time_now_like = None
        text_time_like = None
        text_time_follow = None
        time_now_follow = None
        breakingTime = 50 # BREAK TIME IN HOUR

        # GOES TO THE TAGS
        for tags in self.dictOfTags.keys():
            self.listOfPhotos_t = []
            url_t = "https://www.instagram.com/explore/tags/{tag}/".format(tag=tags)
            amount_users = self.dictOfTags.get(tags)
            self.drive.get(url_t)
            sleep(1)
            self.get_bs(self.drive.page_source)
            ft = True
            limit = 0

            # SCROLLING DOWN UNTIL THE AMOUNT OF PHOTOS IS EQUAL TO THE WEIGHT OF THE  HASHTASH
            while(ft):
                self.drive.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(1)

                for o in self.soup.find_all(class_="Nnq7C weEfm"):
                    for l in o.find_all("a"):
                        limit += 1

                        if (len(self.listOfPhotos_t) >= amount_users):
                            ft = False
                            break

                        elif(l["href"] not in self.listOfPhotos_t and limit > 9):
                            self.listOfPhotos_t.append(l["href"])

                self.get_bs(self.drive.page_source)

            text_amount = " Hashtag: ({}) Amount of photos -> ".format(tags)
            print(text_amount,len(self.listOfPhotos_t))

            gender_of_user = None
            gender_correct = None
            listOfPhotoURl = []

            # GO TO PHOTO aND USER
            for q in self.listOfPhotos_t:
                self.pauseCode()

                if(q in listOfPhotoURl):
                    continue

                sleep(10)
                try:
                    self.drive.get(URL_s+q) # PHOTO URL
                    sleep(3)
                    path_user = self.drive.find_element_by_css_selector(".PQo_0.RqtMr .e1e1d a")
                    path_user.click()  # CLICK ON THE USER HYPERLINK
                    sleep(1)
                    len_followers_raw = self.drive.find_element_by_xpath(XPATH_FOLLOWERSBOX_LEN).get_attribute("title")
                    len_following_raw = self.drive.find_element_by_xpath(XPATH_FOLLOWINGBOX_LEN).text
                    len_followers_cooked = float(len_followers_raw.replace(".", "").replace(",", ""))
                    len_following_cooked = float(len_following_raw.replace(".", "").replace(",", ""))
                except:
                    pass

                else:

                    # GETS THE LANGUAGE AND NAME OF THE USER
                    if(self.girl_activated  == True or self.boy_activated == True or len(self.languages) != 0):
                        lang, name = self.checkUser()

                    ## CHECKING NAME AND DETERMINES THE GENDER OF THE USER
                    if (self.girl_activated == True or self.boy_activated == True):
                        if(name != None):
                            with open("names.csv", "r", encoding="UTF-8") as rd_file:
                                rd = csv.reader(rd_file)
                                for x in rd:
                                    if (x[0] == name):
                                        print("Name from CSV: ", x[0], "G:",x[1])
                                        gender_of_user = x[1]
                                        if (gender_of_user == "girl"):
                                            if (self.girl_activated == 1):
                                                gender_correct = True
                                                break
                                            else:
                                                gender_correct = False

                                        elif (gender_of_user == "boy"):
                                            if (self.boy_activated == 1):
                                                gender_correct = True
                                                break
                                            else:
                                                gender_correct = False
                                    else:
                                        gender_correct = False

                                rd_file.close()
                        else:
                            gender_correct = False

                    else:
                        gender_correct = True

                    if (len(self.languages) != 0):
                        for lg in self.languages:
                            if (lg == lang):
                                lang_corr = True
                                break
                            else:
                                lang_corr = False
                    else:
                        lang_corr = True

                # CHECKING THE LANGUAGES
                if(self.follow_now == True and self.followed < self.maxFollowing):
                    if(gender_correct == True and lang_corr == True):
                        self.drive.find_element_by_css_selector(".BY3EC").click()
                        self.followed += 1
                        print("FOLLOWED -->> {} ".format(self.followed))
                    else:
                        pass
                else:
                    if(self.follow_now == True):
                        self.follow_now = False
                        f_thread = threading.Thread(target=self.pauseFunction, args=("follow",))
                        f_thread.start()

                sleep(5)

                # FOLLOWING IF like_NOW IS TRUE
                if(self.like_now == True and self.liked < self.maxLiking):
                    if(gender_correct == True and lang_corr == True):
                        self.drive.get(URL_s+q)
                        self.drive.find_element_by_css_selector(".fr66n > button:nth-child(1)").click()
                        self.liked += 1
                        print("LIKED -->> {} ".format(self.liked))
                    else:
                        pass

                else:
                    if(self.like_now == True):
                        self.like_now = False
                        l_thread = threading.Thread(target=self.pauseFunction, args=("like",))
                        l_thread.start()

                if (self.comment_now == True and self.commented < self.commentMax):
                    if (gender_correct == True and lang_corr == True):
                        self.drive.get(URL_s + q)
                        textarea = self.drive.find_element_by_xpath('//textarea')
                        textarea.click()
                        sleep(1)
                        textarea2 = self.drive.find_element_by_tag_name('textarea')
                        textarea2.send_keys(self.commentList[random.randint(0, len(self.commentList)-1)])
                        sleep(2)
                        buttonSubmitComment = self.drive.find_element_by_css_selector(".y3zKF").click()
                        self.commented += 1

                else:
                    if (self.comment_now == True):
                        self.comment_now = False
                        c_thread = threading.Thread(target=self.pauseFunction, args=("comment",))
                        c_thread.start()

                listOfPhotoURl.append(q)
                sleep(60)

    # GO INTO THE USER AND FINDS ALL FOLLOWERS AND FOLLOWING ACCOUNTS
    def find_own_data(self, foll_box_XPATH, len_foll_XPATH, list):
        self.drive.get("https://www.instagram.com" + "/" + self.username + "/")
        try:
            following_a = self.drive.find_element_by_xpath(foll_box_XPATH)
            following_a.click()
        except:
            pass
        else:
            sleep(2)

            #scro1ler_container = self.drive.find_element_by_xpath("/html/body/div[4]/div/div")
          #  scro1ler_container = driver.find_element_by_xpath('//body/div[3]/div/div[2]/div/div[2]')
            scro1ler_container = self.drive.find_element_by_css_selector(".pbNvD")
            scro1ler_container = self.drive.find_element_by_xpath("//div[@class='isgrP']")

            sleep(2)

            len_of = int(self.drive.find_element_by_xpath(len_foll_XPATH).text)
            sleep(5)

            for scroller in range(int(len_of/2)):

                self.drive.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', scro1ler_container)
                sleep(random.randint(0, 2 * len_of)/600)

            sleep(1)
            self.get_bs(self.drive.page_source)

        for followers in self.soup.find_all(class_="FPmhX notranslate _0imsa"):
            f = followers['title']
            list.append(str(f))

    def readOldCSV(self, file, list_f, list_n):
        try:
            with open(file, mode="r", newline='') as short:
                fo_read = csv.reader(short)

                self.list = next(fo_read)

                for m in fo_read:
                    list_f.append([''.join(m[0]), ''.join(m[1])])
                    list_n.append(''.join(m[0]))

                short.close()
        except:
            pass

    def unfollower(self):
        push = 10
        date_from_started = date_today

        pathFile = "{}-(following)_new.csv".format(self.username)
        with open(pathFile, "r") as re:
            rd = csv.reader(re)
            next(rd)

            # for line in rd:
            #     user = line[0]
            #     situation = pushDate(line[1], date_today, push)
            #     print(situation)

            re.close()

    def appendToDateFile(self, file, list_f, list_old, list_old_n, list_date, kind_1, kind_2):
        with open(file, mode="w", newline='') as short:

            data_writer = csv.writer(short, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            data_writer.writerow([kind_1, kind_2, "LastUpdated: {}".format(date_today)])

            for k in range(len(list_f)):
                if(list_f[k] not in list_old_n):
                    value_1 = [list_f[k], date_today]
                    list_date.append(value_1)
                    data_writer.writerow(value_1)

                elif(list_f[k] in list_old_n):
                    for l in range(len(list_old_n)):
                        if(list_old_n[l] == list_f[k]):
                            value_2 = [list_old[l][0], list_old[l][1]]
                            list_date.append(value_2)
                            data_writer.writerow(value_2)
            short.close()

    # FINDS ALL THE USERS AND INSERTING INTO CSV FILE
    def send_own_data_csv(self):

        # FINDS ALL PEOPLE, WHO THE USER FOLLOW
        self.find_own_data("/html/body/div[1]/section/main/div/header/section/ul/li[3]/a",
                           XPATH_FOLLOWINGBOX_LEN, self.following_list)

        sleep(1)

        # FINDS ALL PEOPLE, WHO ARE FOLLOWING THE USER
        self.find_own_data("/html/body/div[1]/section/main/div/header/section/ul/li[2]/a",
                           XPATH_FOLLOWERSBOX_LEN, self.followers_list)

        # "/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span"
        path_1 = "{}-(followers)_old.csv".format(self.username)
        path_2 = "{}-(following)_old.csv".format(self.username)
        self.readOldCSV(path_1, self.followers_old, self.followers_old_name) # GETS THE OLD DATA FROM CSV
        self.readOldCSV(path_2, self.following_old, self.following_old_name) # GETS THE OLD DATA FROM CSV
        path_3 = "{}-(followers)_new.csv".format(self.username)
        self.appendToDateFile(path_3,
                              self.followers_list, self.followers_old,
                              self.followers_old_name, self.followers_date,
                              "Followers[new]", "date") ## SENDS DATA TO A LIST

        # SENDS THE DATA TO LIST
        path_4 = "{}-(following)_new.csv".format(self.username)
        self.appendToDateFile(path_4, self.following_list,
                              self.following_old, self.following_old_name,
                              self.following_date, "Following[new]", "date")
        self.drive.get(URL_s)

   # FUNCTION THAT LOGGING INTO THE ACCOUNT
    def login(self, username, password, visibleWindow):
        self.username = username
        self.password = password
        visibleWindowV = visibleWindow
        self.error_login = False

        # Makes the webdrive
        if(visibleWindowV == True):
            options = Options()
            options.add_argument('--headless')
            self.drive = webdriver.Firefox(options=options)
        else:
            self.drive = webdriver.Firefox()

        del visibleWindowV

        # GOES TO THE WEBSITE SELF.URL VARIABLE
        self.drive.get(self.url)
        self.drive.implicitly_wait(10)

        # FINDS THE ELEMENT WHERE USERNAME AND PASSWORD IS
        userNameInput = self.drive.find_element_by_name("username")
        passwordInput = self.drive.find_element_by_name("password")
        # CLEARS IT
        userNameInput.clear()
        passwordInput.clear()

        # Sends the username and password to the input box
        userNameInput.send_keys(self.username)
        passwordInput.send_keys(self.password)

        try:
            login_button = self.drive.find_element_by_xpath("/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div[4]/button")
            login_button.click()
        except:
            login_button = self.drive.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[4]/button")
            login_button.click()
        finally:

            try:
                error_message = self.drive.find_element_by_xpath("/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div[7]")
                if(error_message.is_displayed() == True):
                    self.error_login = True
                    self.drive.quit()
            except:
                pass

        if(self.error_login != True):
            try:
                pass_popup = self.drive.find_element_by_xpath("/html/body/div[1]/section/main/div/div/div/div/button")
                pass_popup.click()
                self.drive.get(URL_s)
                self.drive.implicitly_wait(60)
                pass_popup2 = self.drive.find_element_by_css_selector("button.aOOlW:nth-child(2)")
                pass_popup2.click()
            except:
                pass_popup1 = self.drive.find_element_by_css_selector("button.aOOlW:nth-child(2)")
                pass_popup1.click()

            finally:
                self.login_success = True


    # SAVING THE USER INFORMATION ON A CSV FILE
    def save_information_csv(self):
        path = "{}-(followers)_old.csv".format(self.username)
        with open(path, mode="w", newline='') as fb:

            writer_before = csv.writer(fb, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer_before.writerow(["Followers[name], date(DD/MM/YY)]", "LastedUpdated: {}".format(date_today)])

            for n in range(0, len(self.followers_date)):
                writer_before.writerow([self.followers_date[n][0], self.followers_date[n][1]])

            fb.close()

        path = "{}-(following)_old.csv".format(self.username)
        with open(path, mode="w", newline='') as fi:
            writer_before = csv.writer(fi, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer_before.writerow(["Following[name], date(DD/MM/YY)]", "Last Opdated: {}".format(date_today)])

            for p in range(0, len(self.following_date)):
                writer_before.writerow([self.following_date[p][0], self.following_date[p][1]])

            fi.close()



# window = bot()
#
# window.login("shiing33","mudii234234", False)
#
# window.tagFinder({"hello": 22}, False,False,[],False,False, True, ["Nice pic", "Nice"])



