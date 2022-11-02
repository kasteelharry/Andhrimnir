from bs4 import BeautifulSoup


def getUsers(element):
    names = []

    # The header
    header = element.table.tbody.tr
    for i, elem in enumerate(header):
        if i > 6:
            try:
                name: str = elem.nobr
                if name is not None:
                    lstrip = str(name)[6:]
                    rstrip = lstrip[:len(lstrip) - 7]
                    names.append(rstrip)
            except Exception as er:
                pass
    return names


def getValueOfPage(element, users):
    rows = element.table.tbody.findAll('tr')
    imagesOnPage = []
    result = []
    for i, elem in enumerate(rows):
        if len(elem) > 40:
            try:
                images = elem.findAll('img')
                if (str(elem.get("title")) == "Verwijder deze regel" or
                        str(elem.get("title")) == "Sla deze regel op"):
                    pass
                for image in images:
                    imagesOnPage.append(str(image.get("title")).split())
            except Exception as er:
                pass
    for user in users:
        eatCount = 0
        cookCount = 0
        for image in imagesOnPage:
            if image[0] == user:
                if image[1] == 'kookte':
                    if len(image) > 2:
                        eatCount += 1
                    eatCount += 1
                    cookCount += 1
                elif image[2] == 'mee':
                    eatCount += 1
                elif image[2] == 'met':
                    eatCount += 2
                elif image[2] == 'niet':
                    pass
        value = [eatCount, cookCount]
        result.append(value)
    return result


def goThroughPage(driver):

    content = driver.page_source
    # content = Path("static.html").read_text()
    # print(content)
    soup = BeautifulSoup(content, features="html5lib")
    # The form with all the data
    element = soup.find('form', attrs={'name': 'kosten'})

    users = getUsers(element)
    result = getValueOfPage(element, users)
    return [result, users]
