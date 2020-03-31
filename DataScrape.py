import time 
import threading
from selenium import webdriver
from DataRecorder import DataKeeper
from selenium.webdriver.chrome.options import Options


class WebSurfer(object):
    #object gathers releveat info and prints in to console

    def __init__(self):
        self.todaysData = DataKeeper()
        self.threads = []

    def GetSchedule(self,DayNumber,driver):
        #To grap events on a particular day from timetable.

        events = []
        for col in range(1,21):
            try:
                xpath = '/html/body/table[2]/tbody/tr[%s]/td[%s]/table'% (DayNumber,col) 
                module = driver.find_element_by_xpath(xpath +'[1]/tbody/tr/td[1]/font' ).text
                time = driver.find_element_by_xpath('/html/body/table[2]/tbody/tr[1]/td[%s]/font'% col).text
                
                events.append((module,time))

            except:
                pass

        return events

    def OpenTimetable(self):
        #To open timetable and extract data (calls GetSchedule)

        #Specify path to Chrome Webdriver
        driver = webdriver.Chrome(r'/Users/DominicRodriguez/Documents/Python Files/chromedriver')
        driver.get('https://timetables.kcl.ac.uk/KCLSWS/SDB1819RDB/login.aspx?ReturnUrl=%2fkclsws%2fSDB1819RDB%2fdefault.aspx')
        UserName = driver.find_element_by_name('tUserName')
        PassWord = driver.find_element_by_name('tPassword')
        
        #Enter King's College K-number
        UserName.send_keys('*******') 

        #Enter King's login password
        PassWord.send_keys('*******')

        loginB = driver.find_element_by_name('bLogin')
        loginB.click()

        #Find timetable element
        tTable = driver.find_element_by_xpath('//*[@id="LinkBtn_studentMyTimetable"]')
        tTable.click()

        viewTimetable = driver.find_element_by_xpath('//*[@id="bGetTimetable"]')
        viewTimetable.click()

        #TimeTable Open
        DayNumber = time.localtime()[6]  #+2# gives the row in timetable for that day

        #Direct driver to new timetable pop-up window
        window_after = driver.window_handles[1]
        driver.switch_to_window(window_after)  

        events = self.GetSchedule(DayNumber, driver)

        self.todaysData.updateTimeTable(events)
        self.todaysData.reportTimeTable()
        
        if events == []:
            driver.quit()
        
        else:
            #sleep to allow user to see events
            time.sleep(45)

    def OpenFacebook(self):
        options = Options()
        options.add_argument("--disable-notifications")
        driver = webdriver.Chrome(r'/Users/DominicRodriguez/Documents/Python Files/chromedriver', chrome_options=options)
        driver.get('https://www.facebook.com/') #facebook address

        uName = driver.find_element_by_xpath('//*[@id="email"]')
        pWord = driver.find_element_by_xpath('//*[@id="pass"]')

        #enter facebook username
        uName.send_keys('********')
        #enter facebook password
        pWord.send_keys('********')

        #find login button and open
        loginB = driver.find_element_by_id('loginbutton')
        loginB.click()

        #Get number of friend requests, messages and general notifications
        friendRequests = driver.find_element_by_xpath('//*[@id="fbRequestsJewel"]' ).text[0]
        messages = driver.find_element_by_xpath('//*[@id="u_0_d"]').text[0]
        notifications = driver.find_element_by_xpath('//*[@id="u_0_a"]/div[2]/div[3]').text[0]

        FBtot = self.todaysData.updateFacebook(friendRequests,messages,notifications)

        self.todaysData.reportFacebook()

        if FBtot> 0:
            time.sleep(45)
        else:
            driver.quit() 
    

    def OpenOutlook(self):
    
        options = Options()
        options.add_argument("--disable-notifications")
        driver = webdriver.Chrome(r'/Users/DominicRodriguez/Documents/Python Files/chromedriver', chrome_options=options)
        driver.get('http://outlook.com/kcl.ac.uk')

        userNameBox = driver.find_element_by_xpath('//*[@id="userNameInput"]')
        userNameBox.clear()

        #enter Outlook username
        userNameBox.send_keys('*****')

        passwordBox = driver.find_element_by_xpath('//*[@id="passwordInput"]')
        passwordBox.clear()

        #enter outlook password
        passwordBox.send_keys('******')

        signInBox = driver.find_element_by_xpath('//*[@id="submitButton"]')
        signInBox.click()

        noPopUpButton = driver.find_element_by_xpath('//*[@id="idBtn_Back"]')
        noPopUpButton.click()

        try:
            unreadEmails = int(driver.find_element_by_xpath('//*[@id="_ariaId_43"]/div/div/div[1]/div/span').text)
            
            unOpenedEmail = driver.find_element_by_xpath('//*[@id="_ariaId_24"]')
            unOpenedEmail.click()
            

            sender = driver.find_element_by_xpath('//*[@id="_ariaId_24"]/div[2]/div[3]/div[1]/span').text
            subject = driver.find_element_by_xpath('//*[@id="_ariaId_24"]/div[2]/div[4]/div[3]/span[1]').text
            time.sleep(3)

            contents = driver.find_element_by_xpath('//*[@id="Item.MessagePartBody"]').text

            self.todaysData.updateOutlook(unreadEmails,sender, subject, contents)
            self.todaysData.reportOutLook()
            
            time.sleep(45)
        
        except:
            driver.quit()
            self.todaysData.updateOutlook()
        self.todaysData.reportOutlook()

    def run(self):
        #A thread is created for each process.
        
        timeTableThread = threading.Thread(target= self.OpenTimetable)
        FBThread = threading.Thread(target= self.OpenFacebook)
        OutlookThread = threading.Thread(target = self.OpenOutlook)
        
        self.threads = [timeTableThread, FBThread, OutlookThread]

        for thread in self.threads:
            thread.start()
        

#Run the scraping of notifications/events
if __name__ == '__main__':
    Websurfer.run()


