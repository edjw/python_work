
"""Gets the user to enter one or more URLs to be scraped, very imperfectly checks whether a URL was entered, scrapes the HTML from the webpage(s), saves each page's HTML to a separate .html file """

import requests, bs4

def getURLs():
    """Gets the user to enter one or more URLs to be scraped, very imperfectly checks whether a URL was entered"""
    urls = [] #Using a list to allow multiple URLs to be scraped at once
    userInput = None
    while not urls: #When no URL has been entered, ask the user to enter a URL
        userInput = input("Enter a full URL (starting with http:// or https://) to get the HTML for that webpage.\n")
        while userInput.startswith('http') == False: #Imperfectly checks whether the user entered a full URL and tells the user to enter a full URL if they didn't
            userInput = input("That wasn't a URL. Enter a full URL to get the HTML for that webpage.\n")
        urls.append(userInput) #Save the URL to be scraped later

    while urls: #Once at least one URL has been entered, ask if the user's done or wants to scrape more URLs
        userInput = input("Great. Enter another URL or just press Return if you're finished.\n")
        if len(userInput) == 0: #If nothing was entered, then the user just pressed Return so they've finished entering URLs. Skip to the end of the function
            break
        else: 
            while userInput.startswith('http') == False: #Imperfectly checks whether the user entered a full URL and tells the user to enter a full URL if they didn't
                userInput = input("That wasn't a URL. Enter a full URL or just press Return if you're finished.\n")
            urls.append(userInput) #Save the URL to be scraped later
    return urls
urls = getURLs()

def getHTML():
    """Scrapes the HTML from the webpage(s) using requests, saves each page's HTML to a separate .html file"""
    for url in urls: #Because there might be multipe URLs to scrape, iterate through the list  
        r = requests.get(url)
        r.raise_for_status()
        webpage_html = str(bs4.BeautifulSoup(r.text, "html.parser"))
        filenumber = str(urls.index(url)) #Create a variable called filenumber using the index of the url in the list of urls
        filename = "output_" + filenumber + ".html" #This and above line avoid the loop rewriting the file name of the previous file.
        with open(filename, 'w') as file_object: #open a new (or existing) file to be written (or overwritten)
            file_object.write(webpage_html) #write the scraped HTML into the file
            file_object.close #close the file
getHTML()