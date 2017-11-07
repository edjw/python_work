'''Scrapes Charity Comms Sector Jobs and emails it to one person. For personal use only. Happy to remove this.'''

import requests
from bs4 import BeautifulSoup

# Use this if you want live scraping
#
url = "https://www.charitycomms.org.uk/my-career/sector-jobs"
res = requests.get(url)
res.raise_for_status()
webpage_html = BeautifulSoup(res.text, 'html.parser')
#
#
# Or use this below if you already have a local HTML file
#
#
# with open ("jobs.html") as workingfile:
#    webpage_html = BeautifulSoup(workingfile, 'html.parser')
#
#

job_titles_stripped = [] #We'll put stripped HTML into these lists
job_links_stripped = []
job_descriptions_stripped = []
job_details_stripped = []
final_output = [] # And this is where the final output will go

job_divs = webpage_html.select("#all .job .col-sm-9") #making a variable for the common container for info I want to scrape

for job_div in job_divs: #iterate through the containers and select info for all of them
    job_titles = job_div.select("h3 a")
    job_links = job_div.select("h3 a")
    job_descriptions = job_div.select("p:nth-of-type(2)")
    job_details = job_div.select("p:nth-of-type(3)")

    for job_title in job_titles:
        job_title = job_title.get_text() # get_text strips html tags like <p>text</p>
        job_titles_stripped.append(job_title) # puts stripped HTML into stripped lists

    for job_link in job_links:
        job_link = job_link['href'] #to get the url that something links to
        job_links_stripped.append(job_link)

    for job_description in job_descriptions:
        job_description = job_description.get_text()
        # removes multiple spaces in the middle or around this data
        job_description = " ".join(job_description.split())
        job_descriptions_stripped.append(job_description)

    for job_detail in job_details:
        job_detail = job_detail.get_text()
        job_detail = " ".join(job_detail.split())
        job_details_stripped.append(job_detail)

for i in range(len(job_divs)): #get the job title, description etc in order and put them all together inside final_output
    output = str(job_titles_stripped[i]) + "\n" + str(job_links_stripped[i]) + "\n" + str(job_descriptions_stripped[i]) + "\n" + str(job_details_stripped[i]+ "\n\n")
    final_output.append(output)

# Uncomment this to save output as local .txt file
#
# with open("output.txt", 'w') as file_object:
#     for i in range(len(job_divs)):
#         file_object.write(str(job_titles_stripped[i]) + "\n" + str(job_links_stripped[i]) + "\n" + str(job_descriptions_stripped[i]) + "\n" + str(job_details_stripped[i]+ "\n\n"))
# file_object.close()

def send_email():
    """Sends email using Mailgun"""
    email_data = {
        "from": "Name <email@mailgun.domain.tld>",
        "to": ["email@domain.tld"],
        "subject": "Subject line",
        "text": final_output
    }

    return requests.post(
        "https://api.mailgun.net/v3/mailgun.domain.tld/messages",
        auth=("api", "$API_KEY"),
        data=email_data)

send_email()
