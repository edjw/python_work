# Scrape W4MPJobs

A previous version of this used CasperJS on top of PhantomJS which used npm and nodejs to install and run. It now uses Mechanical Soup to work through the dynamic forms which is *much* simpler, only uses Python and needs less explanation!

This uses Mechanical Soup, Beautiful Soup and requests to scrape the HTML of [W4MPJobs](http://www.w4mpjobs.org/SearchJobs.aspx), parse the HTML and send what I'm interested in over email.
