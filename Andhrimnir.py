
from selenium.webdriver.common.by import By
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from src.CreateExcelSheet import createExcelFile
import credentials
from src.CrawlPage import goThroughPage

PAGES = 1

# The users using eetlijst.nl
USERS = []
# The amount of times a user has cooked
# and the amount of times a user has joined for dinner
VALUES = []


def updateValues(result):
    global VALUES
    if len(VALUES) == 0:
        VALUES = result
    else:
        for i, value in enumerate(result):
            VALUES[i][0] += value[0]
            VALUES[i][1] += value[1]


def combineUsersAndValues(users, values):
    combined = []
    for i, user in enumerate(users):
        try:
            combined.append([user, values[i], round((
                values[i][1]/values[i][0]) * 100, 2)])
        except ZeroDivisionError:
            combined.append([user, values[i], 0])
    return combined


# If you want to open Chrome
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.command_executor.set_timeout(10)
driver.get('http://eetlijst.nl/login.php')

username = driver.find_element(By.NAME, "login")
password = driver.find_element(By.NAME, "pass")
username.send_keys(credentials.username)
password.send_keys(credentials.password)
driver.find_element(By.NAME, "dologin").click()

driver.find_element(By.CLASS_NAME, "cc-btn").click()

driver.find_element(By.XPATH, "//*[@class='r']//a[2]").click()

# Go through page

result = goThroughPage(driver)
updateValues(result[0])
USERS = result[1]

for i in range(PAGES):

    # Next page
    driver.find_element(By.NAME, "Volgende 25 ->").click()

    # Crawl the page
    result = goThroughPage(driver)
    updateValues(result[0])

combined = combineUsersAndValues(USERS, VALUES)

driver.quit()

createExcelFile(combined)
