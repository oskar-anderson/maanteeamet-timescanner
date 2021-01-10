# Maanteeamet Time Scanner
This Python program will scan available driving exam times from "Maanteeamet" e-service website and sends an email notification about new openings.


## REQUIREMENTS:
Program is written in python and uses Selenium with Chrome WebDriver.

### Installations:
1. Python
2. Google Chrome
3. Compatible version of [Chromedriver](https://chromedriver.chromium.org) needs to be placed in the main root folder as "chromedriver.exe".

### Config:
1. Rename "userdata-default.yaml" to "userdata.yaml"
2. Sending emails requires a Google account with "Less secure apps" enabled. Go to <https://myaccount.google.com/security>. 
   This account is only used for sending emails. Account info goes into "userdata.yaml".
3. Edit "userdata.yaml" to fit your needs


## About
This program was initially made in Dec 2019, when Maanteeamet e-service only allowed to reserve times in the current month +2 months ahead. 
This meant that all times were constantly taken but on every new month new times were unlocked.
Reserved times could easily be changed within 3 workdays without any extra charge.
So people with a old time, they did not want, would migrate to the new times and create opening for their previous time.

This created a trading environment for better times:

- https://www.facebook.com/groups/arkeksamiteajaduleeesti - active community about driving exams
- https://xn--sidueksam-q7a.ee/ - very sketchy website, now closed, that offered 15€/month subscription service to receive notifications about free times

This program was created out of necessity to not manually refresh a page or pay 15€.
Using it I got a time in 5 hours :smile:

Since then the Maanteeamet system has changed - times are now listed publicly and it is possible to reserve later times.
Since I already have a driving license I do not have access to the e-service and cannot confirm how well parts of the program still function.
To compensate I updated the program to work with the public data.
If you do have access to the e-service feel free to improve this program. 


For a similar program done in Java check out: 
<https://github.com/outworld-umd/maanteeamet-checker>
