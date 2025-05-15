# Krakow Guide
#### Video Demo: https://www.youtube.com/watch?v=LYma4TBgsdo
#### Description:


My project is a website written using software tools, such as Python, Flask, SCSS, Jinja, SQLite and JavaScript a little. The website is designed to provide information about attractions and other places necessary for tourism in Cracow. Site visitors can see a list of locations, read about them, register, and create their own list of locations to visit.

#### Let's move on to the files that take place in the program:
**layout.html** - a template for all pages of the site. Contain head of .html file, navbar, login modal window, footer and a place for pages contant.
**index.html** - main page.
**apology.html** - page with error message. Appear, when you enter wrong password, enter invalid email, use username was took before and so on.
**category.html** - just a page with all categories (nothing special)
**article.html** - it is generate a page for location.
**profile.html** - page for profile. There are profile information, opportunities for change email, password, username, log out and user's favourite locations.
**register.html**  - page for registration form.

***app.py*** - main program file\
helpers.py - there are several additional functions\
    def apology - render apology message, if something goes wrong\
    def login_required - decorate routes to require login\
    def crop_to_aspect - cut image for needable format\
    def is_valid_email and def is_valid_username - validate email and username respectively

**guide.db** - database file.\
__Database schema:__\
CREATE TABLE sights (sight_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT NOT NULL, address TEXT, mark NUMERIC, categories TEXT, photos TEXT, description TEXT);
CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, email TEXT NOT NULL, hash TEXT NOT NULL);
CREATE TABLE favourites (favourite_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, user_id INTEGER NOT NULL, sight_id INTEGER NOT NULL);
CREATE TABLE categories (category_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT NOT NULL, fullname TEXT NOT NULL);
CREATE UNIQUE INDEX username ON users (username);
CREATE UNIQUE INDEX email ON users (email);


styles.scss
index.js
and a bunch of location's pictures