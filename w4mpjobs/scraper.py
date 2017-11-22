from re import sub
from requests import post
from bs4 import BeautifulSoup
import html2text

jobs_string_html = ''

with open("html_scraped.html") as workingfile:
    webpage_html = BeautifulSoup(workingfile, 'html.parser')

jobs = webpage_html.select('.job-advert')

for job in jobs:
    job = str(job)
    jobs_string_html = jobs_string_html + job + '<br>'

# I should probably actually use BeautSoup for this cleanup below instead of regular expressions

replacements = {
    ' class="post-19 post type-post status-publish format-standard hentry category-uncategorized tag-boat tag-lake job-advert" id="post-19"': "",
    '<div class="clearer"></div>':"",
    '<div class="jobadvertdetailbox" id="jobtitle">.*</div>':"",
    'JobDetails.aspx': "http://www.w4mpjobs.org/JobDetails.aspx",
    '<div itemscope="" itemtype="http://schema.org/JobPosting">': "",
    '</div>\n</article>': '</article>',
    '<strong>.*</strong>\/': "",
    '<span itemprop="title">': '<strong><span itemprop="title">',
    '</span>\n.*</div>': '</span></strong></div>',
}

for original, new in replacements.items(): # iterate through replacements dictionary
    jobs_string_html = sub(original, new, jobs_string_html)

jobs_string_text = html2text.html2text(jobs_string_html)

def send_email():
    """Sends email using Mailgun"""
    email_data = {
        "from": "W4MP Jobs <name@mailgun.domain.tld>",
        "to": ["name@domain.tld"],
        "subject": "This week's W4MPJobs",
        "text": jobs_string_text,
        "html": jobs_string_html
    }

    return post(
        "https://api.mailgun.net/v3/mailgun.domain.tld/messages",
        auth=("api", "API_Key"),
        data=email_data)

send_email()
