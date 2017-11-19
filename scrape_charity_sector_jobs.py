'''Scrapes Charity Comms Sector Jobs. For personal use. Happy to take down.'''

from requests import get, post
from bs4 import BeautifulSoup
import html2text

url = "https://www.charitycomms.org.uk/my-career/sector-jobs"
res = get(url)
webpage_html = BeautifulSoup(res.text, 'html.parser')

jobs = webpage_html.select("#all > .job > .row > .col-sm-9")

jobs_string_html = ""

for job in jobs:
    job = str(job)
    jobs_string_html = jobs_string_html + job

jobs_string_html = " ".join(jobs_string_html.split())
jobs_string_html = jobs_string_html.replace("<p><p>", "<p>")
jobs_string_html = jobs_string_html.replace("</p> </p>", "</p>")
jobs_string_html = jobs_string_html.replace(" class=\"col-sm-9\"", "")
jobs_string_html = jobs_string_html.replace("<div>", "")
jobs_string_html = jobs_string_html.replace("</div>", "")

jobs_string_text = html2text.html2text(jobs_string_html)


def send_email():
    """Sends email using Mailgun"""
    email_data = {
        "from": "Charity Comms Jobs <name@mailgun.domain.tld>",
        "to": ["name@domain.tld"],
        "subject": "This week's Charity Comms Jobs",
        "text": jobs_string_text,
        "html": jobs_string_html
    }

    return post(
        "https://api.mailgun.net/v3/mailgun.domain.tld/messages",
        auth=("api", "API_KEY"),
        data=email_data)

send_email()
