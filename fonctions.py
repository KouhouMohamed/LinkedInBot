import time
from selenium import webdriver

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


#chrome browser path
path_browser =r"C:\Users\medko\Desktop\Stage\Scripts\chromedriver.exe"

#hide the browser
options = webdriver.ChromeOptions()
options.add_argument("headless")


class LinkedinBot:
    def __init__(self,user_name,pass_word):
        
        self.browser = webdriver.Chrome(path_browser)
        self.base_url = "https://www.linkedin.com/"
        self.login_url = self.base_url + 'login'
        self.feed_url = self.base_url + 'feed'

        #login informations
        self.username = user_name
        self.password = pass_word

    #fonction to open the browser and go to the url
    def _nav(self,url):
        try:
            self.browser.get(url)
            time.sleep(5)
        except:
            pass
    
    #login to the account
    def login(self):
        self._nav(self.login_url)
        self.browser.find_element_by_id('username').send_keys(self.username)
        self.browser.find_element_by_id('password').send_keys(self.password)
        self.browser.find_element_by_xpath("//button[contains(text(), 'S’identifier')]").click()


    def search(self,student_name):
        search_result = []
        r = self.browser.find_element_by_id("ember16")
        search = r.find_element_by_tag_name("input")
        search.send_keys(student_name)
        search.send_keys(Keys.RETURN)
        try:
            main = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "search-results-container"))
            )
            if self.browser.find_element_by_class_name('search-results-container'):
                main = self.browser.find_element_by_class_name('search-results-container')
                div = main.find_element_by_class_name("display-flex")
                div = div.find_element_by_tag_name("div")
                div = div.find_element_by_tag_name("div")
                div = div.find_element_by_tag_name("div")
                #print(div.get_attribute('innerHTML'))
                try:
                    ul = div.find_element_by_tag_name("ul")
                    lis = ul.find_elements_by_tag_name("li")
                    for li in lis:
                        try:
                            a = li.find_element_by_tag_name("a")
                            search_result.append(a.get_attribute('href'))
                        except:
                            pass
                except:
                    self.school = "account not found"
                    self.image = "account not found"
        finally:
            pass
        return search_result

    #fonction to found school's name
    def searchSchool(self,url):
        self._nav(url)
        try :
            #find the div with class 'pv-entity__degree-info' where the name of school in
            if self.browser.find_element_by_class_name('pv-entity__degree-info'):
                div = self.browser.find_element_by_class_name('pv-entity__degree-info')
                #extract the name of school
                if div.find_element_by_tag_name('h3'):
                    h2 = div.find_element_by_tag_name('h3')
                    self.school = h2.text
            if self.browser.find_element_by_class_name('pv-top-card__photo'):
                image = self.browser.find_element_by_class_name('pv-top-card__photo')
                print(image.get_attribute('innerHTML'))
                self.image = image.get_attribute('src')
                    
        #in case of none exestance of school name
        except :
            self.school = "None"
            self.image = "No image found"
            pass

    #Closing the browser
    def quit(self):
        self.browser.quit()
# ------------------------------------------- Other functions

#To extract link from the string that is the result of google research
def find_link(url):
    url_ret = ""
    i = url.find("https")
    j = url.find("&")
    url_ret = url[i:j+1]
    url_ret = url_ret.replace("&","/")
    return url_ret

