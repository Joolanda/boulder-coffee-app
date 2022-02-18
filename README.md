# boulder-coffee-app
A website build with Flask and Bootstrap that lists climbing-and boulderhalls with wifi and good coffee. Use gunicorn, a WSGI server and Heroku to host.

## Description
The goal for this project was to create a professional portfolio project after succesfully completed my 100 Days of Python Pro Bootcamp. First, I built the back-end. My climber REST API. For testing my endpoints, I used Postman. 
Read the Documentation here: https://documenter.getpostman.com/view/10997891/UVkiSyGP

Secondly I developed my front end, a workable website that uses this data, localhosting with wtforms and csv-file. 

... but then I've stretched my coding skills! I used Alchemy and Bootstrap to display the sportcafes. development, create a website that uses this data. For external hosting parts of the code in main.py had to be rewritten. The latest version of Boulder Coffee App should display all sportcafes, but it should also allow people to add new cafes or delete cafes.

Resulting in a Flask App which is then hosted using Gunicorn and Heroku. Indeed, normal web servers cannot run Python applications,
so after production a special type of server was created (WSGI = Web Server Gateway Interface ) to run python applications.

## brainstorming - text slides
- Want to work in a pleasant atmosphere with great coffee?
- Start your workday with expresso and climbing?
- Latte Macchiato after a good boulder session?

Checkout my collection of boulder- and climbinghall bistro's with good expresso, latte and more.

## Planned updates:
- [ ] Form with validation? (Add a new bistro)
- [ ] Develop new version with users?
- [ ] Button, handling update price
- [ ] Heroku hosting
- [ ] subpages re-directing
