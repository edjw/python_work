# Scrape W4MPJobs

This uses CasperJS on top of PhantomJS to scrape the HTML of W4MPJobs, then Python and Beautiful Soup to parse the HTML and send what I'm interested in over email.

<http://www.w4mpjobs.org/SearchJobs.aspx?search=nmwandabove>

## PhantomJS and CasperJS

W4MPJobs uses ASPX which I can't get Beautiful Soup to handle.

Also, as this is running on Raspberry Pi and no armhf build of Selenium is available, I have to use PhantomJS which is built forr armhf in the Debian repository.

`apt-get install phantomjs`

`npm install -g casperjs`

CasperJS uses the index.js file to select the radio buttons I want by CSS selector, wait for the page to load, scrape the HTML I want, and save it as a file. It only saves paid jobs outside of London at the moment.

## Python and Beautiful Soup

scraper.js opens the file saved by CasperJS, cleans up the html, makes a plaintext version of the html and sends it as an email using Mailgun

## Crontab

Run it regularly with cron.

`crontab -e`

`2 12 * * Wed export QT_QPA_PLATFORM=offscreen && casperjs /path/to/script/index.js && python3 /path/to/script/scraper.py`

There's a bug in PhantomJS in the Debian repository that means you have to do the `export QT_QPA_PLATFORM=offscreen` before you run casperjs