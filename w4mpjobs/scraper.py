"""Scrapes data from W4MPJobs, parses it a bit, emails it"""

from re import sub
from mechanicalsoup import StatefulBrowser, Form
from requests import post
from bs4 import BeautifulSoup
from html2text import html2text

def scrape_HTML(url):
    """Scrapes the HTML from W4MPJobs"""
    browser = StatefulBrowser()
    page = browser.open(url)
    form = Form(page.soup.form)

    # Selects all on the number of results radio button
    number_results_data = {"ctl00$MainContent$RadioButtonList2": 9999}
    form.set_radio(number_results_data)

    # Selects NWM or more on salary radio button
    salary_data = {"ctl00$MainContent$rblSalary": "nmwormore"}
    form.set_radio(salary_data)

    # Selects outside London on the location radio button – other options commented out
    location_data = {"ctl00$MainContent$rblJobs": "outside"}
    # location_data = {"ctl00$MainContent$rblJobs": "inlondon"}
    # location_data = {"ctl00$MainContent$rblJobs": "both"}
    form.set_radio(location_data)

    # Submits the form
    response = browser.submit(form, page.url)

    # Gets response as text
    response = response.text

    # Closes the browser
    browser.close()

    return response


def process_HTML(full_html):
    """Parses the HTML scraped"""
    full_html = BeautifulSoup(full_html, "lxml")
    html_jobs_string = ''
    jobs = full_html.select('.job-advert')

    for job in jobs:
        job = str(job)
        html_jobs_string = html_jobs_string + job + '<br>'

    replacements = {
        ' class="post-19 post type-post status-publish format-standard hentry category-uncategorized tag-boat tag-lake job-advert" id="post-19"': "",
        '<div class="clearer"></div>':"",
        '<div class="jobadvertdetailbox" id="jobtitle">.*</div>':"",
        'JobDetails.aspx': "http://www.w4mpjobs.org/JobDetails.aspx",
        '<div itemscope="" itemtype="http://schema.org/JobPosting">': "",
        '</div>\n</article>': '</article>',
        r'<strong>.*</strong>/': "",
        '<span itemprop="title">': '<strong><span itemprop="title">',
        '</span>\n.*</div>': '</span></strong></div>'
    }

    for original, new in replacements.items(): # iterate through replacements dictionary
        html_jobs_string = sub(original, new, html_jobs_string)

    text_jobs_string = html2text(html_jobs_string)

    return html_jobs_string, text_jobs_string


def send_email(html_jobs_string, text_jobs_string):
    """Sends email using Mailgun"""
    email_data = {
        "from": "W4MP Jobs <name@mailgun.domain.tld>",
        "to": ["name@domain.tld"],
        "subject": "This week's W4MPJobs",
        "text": text_jobs_string,
        "html": html_jobs_string
    }

    return post(
        "https://api.mailgun.net/v3/mailgun.domain.tld/messages",
        auth=("api", "API_Key"),
        data=email_data)


webpage_html = scrape_HTML("http://www.w4mpjobs.org/SearchJobs.aspx")

jobs_string_html, jobs_string_text = process_HTML(webpage_html)

send_email(jobs_string_html, jobs_string_text)
