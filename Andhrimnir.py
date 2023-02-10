
from selenium.webdriver.common.by import By
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from src.CreateExcelSheet import createExcelFile
import credentials
from src.CrawlPage import goThroughPage
from selenium.webdriver.common.by import By
PAGES = 3

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
            # Percentage and ratio
            combined.append([user, values[i], round((
                values[i][1]/values[i][0]) * 100, 1), 
                values[i][0] // values[i][1]])
        except ZeroDivisionError:
            combined.append([user, values[i], 0, 0])
    return combined


# Set the options for the driver.
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--disable-setuid-sandbox')
options.add_argument("--window-size=1920,1080")
options.add_argument("--start-maximized")
options.add_argument("--incognito")
# If you want to open Chrome
path = ChromeDriverManager().install()
driver = webdriver.Chrome(executable_path=path, options=options)
driver.command_executor.set_timeout(40)
driver.get('http://eetlijst.nl/login.php')
# Wait for the page to load.
driver.implicitly_wait(5)

username = driver.find_element(By.NAME, "login")
password = driver.find_element(By.NAME, "pass")
username.send_keys(credentials.username)
password.send_keys(credentials.password)
# Clicking the cookie banner if it exists.
try:
    banner = driver.find_element(By.CLASS_NAME, "cc-btn")
    driver.execute_script("arguments[0].click();", banner)
except Exception:
    pass
# Send the login form to continue
login = driver.find_element(By.NAME, "dologin").click()
# Navigate to the history page.
driver.find_element(By.XPATH, "//*[@class='r']//a[2]").click()

# Go through the first page
result = goThroughPage(driver)
updateValues(result[0])
USERS = result[1]

# Loop over the remaining pages
for i in range(PAGES):
    # Next page
    driver.find_element(By.NAME, "Volgende 25 ->").click()
    # Crawl the page
    result = goThroughPage(driver)
    updateValues(result[0])

# Prepare the final results
combined = combineUsersAndValues(USERS, VALUES)
# Stop the driver
driver.quit()
# Create the excel file.
createExcelFile(combined)
