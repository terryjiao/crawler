import time
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
from queue import Queue


def parseRecipe(url, driver, queue, basicUrl, set, f):
    # init the driver
    driver.get(url)
    # wait for dynamically loading the webpages
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    f.write("[\n")
    # recipeUrl: string
    f.write("recipeUrl: " + url + "\n")

    # recipeName: string
    recipeName = soup.h1.string
    f.write("recipeName: " + recipeName + "\n")

    # recipePhoto: string
    recipePhoto = soup.find('div', class_='recipe-details-image').img['src']
    f.write("recipePhoto: " + recipePhoto + "\n")

    # ingredients: string[]
    f.write("ingredients: ")
    ingredientLines = soup.find('div', class_='recipe-ingredients')
    for line in ingredientLines.ul.find_all('li'):
        ingredient = ""
        for element in line.contents:
            if hasattr(element, 'text'):
                ingredient = ingredient + element.text
        f.write(ingredient + ", ")
    f.write("\n")

    # ratings: float
    reviews = soup.find('div', class_='primary-info-left-wrapper')
    review = None
    if len(reviews.contents) >= 3:
        review = reviews.contents[2]
        rate = 0.0
        for fullStar in review.find_all('span', class_='full-star'):
            rate = rate + 1.0
        for halfStar in review.find_all('span', class_='half-star'):
            rate = rate + 0.5
        f.write("rating: " + str(rate) + "\n")
    else:
        f.write("rating: " + "None" + "\n")

    # cookTime: string
    cookTime = soup.find('div', class_='summary-item-wrapper').contents[1].span.string
    f.write("cookTime: " + cookTime + "minutes\n")

    # serve: number
    serving = soup.find('div', class_='servings').input['value']
    f.write("servings: " + serving + "\n")

    f.write("]\n")

    # tags
    # tags = soup.find('div', class_ = 'recipe')
    # for tag in tags.contents:
    #     print(tag.li.a['title'])

    # add related recipes to crawler queue
    relatedRecipes = soup.find('div', class_='related-carousel').find_all('div', class_='single-recipe')
    for relatedRecipe in relatedRecipes:
        fullUrl = basicUrl + relatedRecipe.a.get('href')
        if fullUrl not in set:
            if not queue.full():
                set.add(fullUrl)
                queue.put(fullUrl)


def main():
    target = 'https://www.yummly.com/recipes'
    req = requests.get(url=target)
    basicUrl = 'https://www.yummly.com'
    html = req.text
    bf = BeautifulSoup(html)
    texts = bf.find_all('a', class_='link-overlay')
    driver = webdriver.Chrome()
    set = {basicUrl}
    queue = Queue(1000)

    # init file
    f = open("output.txt", 'a', encoding='utf-8')
    f.write("{\n")

    # add first group of recipe to crawler queue
    for link in texts:
        fullUrl = basicUrl + link.get('href')
        if fullUrl not in set:
            set.add(fullUrl)
            queue.put(fullUrl)

    while not (queue.empty() & len(set) > 1000):
        parseRecipe(url=queue.get(), driver=driver, queue=queue, basicUrl=basicUrl, set=set, f=f)

    f.write("}")


if __name__ == '__main__':
    main()
