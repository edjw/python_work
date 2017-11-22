var fs = require('fs');
var html = ""
var casper = require('casper').create();
casper.start('http://www.w4mpjobs.org/SearchJobs.aspx?search=nmwandabove', function () {
    this.waitForSelector('.pagelinks');
});
casper.then(function () {
    this.click('#ctl00_MainContent_RadioButtonList2_4');
});
casper.then(function () {
    this.click('#ctl00_MainContent_rblSalary_1');
});
casper.then(function () {
    this.click('#ctl00_MainContent_rblJobs_1');
});
casper.then(function () {
    this.click('#ctl00_MainContent_btnSearch');
});

casper.then(function () {
    html = html.concat(this.getHTML('div .entry-content', true));
});


casper.then(function () {
    var f = fs.open('scraped_html.html', 'w');
    f.write(html);
    f.close();
});

casper.run();