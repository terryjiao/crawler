import time
from bs4 import BeautifulSoup
import requests
import threading
import json as js

amount = 0
urlSet = set()
cuisines = ["American", "Asian", "Barbecue", "Cajun&Creole", "Chinese", "Cuban", "English", "French", "German",
            "Greek", "Hawaiian", "Hungarian", "Indian", "Irish", "Italian", "Japanese", "Kid-Friendly",
            "Mediterranean", "Mexican", "Moroccan", "Portuguese", "Southern&SoulFood", "Southwestern", "Spanish",
            "Swedish", "Thai"]
technique = ["Baking", "Blending", "Boiling", "Braising", "Brining", "Broiling", "Browning", "Canning", "Drying",
             "Frosting", "Frying", "Glazing", "Grilling", "Marinating", "Microwaving", "Pickling", "Poaching",
             "Pressure", "Cooking", "Roasting", "Sauteeing", "Slow", "Cooking", "Steaming", "Stir", "Frying",
             "Stuffing"]


def parseWebpage(cuisine, tech, f):
    attempts = 0
    success = False
    global amount
    while attempts < 3 and not success:
        try:
            maxResult = 500
            url = "https://www.yummly.com/recipes?allowedTechnique=technique%5Etechnique-" + tech + "&allowedCuisine=cuisine%5Ecuisine-" + cuisine + "&taste-pref-appended=true&maxResult=" + str(
                maxResult)
            req = requests.get(url)
            soup = BeautifulSoup(req.text, 'lxml')
            data = soup.find('div', class_="structured-data-info").script
            dataJson = js.loads(data.text)
            recipes = dataJson['itemListElement']
            success = True

            for recipe in recipes:
                # init recipeUrl = None
                recipeUrl = None

                # init recipeName = None
                recipeName = None

                # init recipePhoto = None
                recipePhoto = None

                # init ingredients = None
                ingredients = None

                # ratings = None
                ratings = None

                # cookTime = None
                cookTime = None

                # serve = None
                serve = None

                # init tags = recipe["keywords"]
                tags = None

                if 'url' in recipe:
                    recipeUrl = recipe['url']
                    if recipeUrl in urlSet:
                        continue
                    else:
                        urlSet.add(recipeUrl)

                if 'name' in recipe:
                    recipeName = recipe['name']

                if 'image' in recipe:
                    recipePhoto = recipe['image']

                if 'recipeIngredient' in recipe:
                    ingredients = recipe['recipeIngredient']

                if 'aggregateRating' in recipe:
                    ratings = float(recipe["aggregateRating"]['ratingValue'])

                if 'totalTime' in recipe:
                    cookTime = recipe["totalTime"]

                if 'recipeYield' in recipe:
                    serve = recipe['recipeYield']

                if 'keywords' in recipe:
                    tags = recipe["keywords"]

                # encode recipe to Json format
                recipeOutput = dict(recipeUrl=recipeUrl,
                                    recipeName=recipeName,
                                    recipePhoto=recipePhoto,
                                    ingredients=ingredients,
                                    ratings=ratings,
                                    cookTime=cookTime,
                                    serve=serve,
                                    tags=tags,
                                    )
                json_output = js.dumps(recipeOutput, indent=4)
                f.write(json_output + "\n")
                amount = amount + 1
                if amount % 1000 == 0:
                    print(str(amount) + " recipes have been added")

        # handle http connection exceptions
        except ConnectionError:
            # retry for up to 3 attempts
            attempts += 1
            if attempts == 3:
                break
            time.sleep(1)
        # handle other exceptions
        except:
            return


def parseWebpageMuiltiThread(cuisine):
    global amount
    for tech in technique:
        tech = tech.lower()
        attempts = 0
        success = False
        f = open("output/output-" + cuisine + "-" + tech + ".txt", 'w+', encoding='utf-8')
        while attempts < 3 and not success:
            try:
                maxResult = 500
                url = "https://www.yummly.com/recipes?allowedTechnique=technique%5Etechnique-" + tech + "&allowedCuisine=cuisine%5Ecuisine-" + cuisine + "&taste-pref-appended=true&maxResult=" + str(
                    maxResult)
                req = requests.get(url)
                soup = BeautifulSoup(req.text, 'lxml')
                data = soup.find('div', class_="structured-data-info").script
                dataJson = js.loads(data.text)
                recipes = dataJson['itemListElement']
                success = True

                for recipe in recipes:
                    # init recipeUrl = None
                    recipeUrl = None

                    # init recipeName = None
                    recipeName = None

                    # init recipePhoto = None
                    recipePhoto = None

                    # init ingredients = None
                    ingredients = None

                    # ratings = None
                    ratings = None

                    # cookTime = None
                    cookTime = None

                    # serve = None
                    serve = None

                    # init tags = recipe["keywords"]
                    tags = None

                    if 'url' in recipe:
                        recipeUrl = recipe['url']
                        # with lock:
                        #     if recipeUrl in urlSet:
                        #         continue
                        #     else:
                        #         urlSet.add(recipeUrl)

                    if 'name' in recipe:
                        recipeName = recipe['name']

                    if 'image' in recipe:
                        recipePhoto = recipe['image']

                    if 'recipeIngredient' in recipe:
                        ingredients = recipe['recipeIngredient']

                    if 'aggregateRating' in recipe:
                        ratings = float(recipe["aggregateRating"]['ratingValue'])

                    if 'totalTime' in recipe:
                        cookTime = recipe["totalTime"]

                    if 'recipeYield' in recipe:
                        serve = recipe['recipeYield']

                    if 'keywords' in recipe:
                        tags = recipe["keywords"]

                    # encode recipe to Json format
                    recipeOutput = dict(recipeUrl=recipeUrl,
                                        recipeName=recipeName,
                                        recipePhoto=recipePhoto,
                                        ingredients=ingredients,
                                        ratings=ratings,
                                        cookTime=cookTime,
                                        serve=serve,
                                        tags=tags,
                                        )
                    json_output = js.dumps(recipeOutput, indent = 4)
                    f.write(json_output + "\n")
                    amount = amount + 1
                    if amount % 1000 == 0:
                        print(str(amount) + " recipes have been added")

                f.close()
            # handle http connection exceptions
            except ConnectionError:
                # retry for up to 3 attempts
                attempts += 1
                print("retry")
                if attempts == 3:
                    break
                time.sleep(3)
            # handle other exceptions
            except AttributeError:
                # retry for up to 3 attempts
                attempts += 1
                if attempts == 3:
                    break
                time.sleep(3)
                print("retry")
            # handle other exceptions
            except:
                break


def crawler():
    f = open("output1.txt", 'w+', encoding='utf-8')
    f.write("{\n")
    for cuisine in cuisines:
        for tech in technique:
            parseWebpage(cuisine.lower(), tech.lower(), f)
    f.write("}\n")


def multiThreadCrawler():
    for cuisine in cuisines:
        t = threading.Thread(target=parseWebpageMuiltiThread, args=(cuisine.lower(),))
        t.setDaemon(True)
        t.start()
    t.join()

def main():
    crawler()
    # multiThreadCrawler()


if __name__ == '__main__':
    main()
