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
        "from": "Charity Comms Jobs <ed@mailgun.edjw.co.uk>",
        "to": ["ed@johnsonwilliams.co.uk"],
        "subject": "This week's Charity Comms Jobs",
        "text": jobs_string_text,
        "html": jobs_string_html
    }

    return post(
        "https://api.mailgun.net/v3/mailgun.edjw.co.uk/messages",
        auth=("api", "key-73f69b0422dc19357ae1ad473269f617"),
        data=email_data)

send_email()
