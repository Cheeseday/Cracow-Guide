# Krakow Guide
#### Video Demo: https://www.youtube.com/watch?v=LYma4TBgsdo
#### Description:


My project is a website written using software tools, such as Python, Flask, SCSS, Jinja, SQLite, Bootstrap and JavaScript a little. The website is designed to provide information about attractions and other places necessary for tourism in Cracow. Site visitors can see a list of locations, read about them, register, and create their own list of locations to visit.

### Let's move on to the files that take place in the program:
**layout.html** - a template for all pages of the site. Contains head of .html file, navbar, login modal window, footer and a place for pages contant.\
**index.html** - main page.\
**apology.html** - page with error message. Appear, when you enter wrong password, enter invalid email, use username was already took and so on.\
**category.html** - just a page with category links and locations in choosed category.\
**article.html** - it is generate a page for location.\
**profile.html** - page for profile. There are profile information, opportunities for change email, password, username, log out and user's favourite locations.\
**register.html**  - page for registration form.\

***app.py*** - main program file. Contains most of program logic, configurate application. Functions:\
    * def get_db - this function get connection with database.\
    * def query.db - this function is simplify responces to db.\
    * def index - this function provide logic for main page. get sights and favourite locations from database and render template index.html with it.\
    * def login - this function provide logic for log user in program by validating form data and checking is user in database.\
    * def logout - this function log out user by clearing session.\
    * def register - this function register user. It checks is form's data valid (render apology.html, is it not - contains 9 types of user's error), hash the password and insert new user in database. \
    * def profile - this function show user data, user's favourite places and render template profile.html.\
    * def favourite - this function delete from or insert into database choosed favourite place depending on this place already in db or not yet.\
    * def change - this function change password. Check, is form's data valid, validate password, encrypt password, update database if all good.\
    * def changeUsername - this function change username like algorithm above works.\
    * def changeEmail - this function change email like algorithm above works.\
    * def card - this function get all information about choosed card and render a page for it.\ 
    * def category - this function show locations in choosed category and render category.html.\

**helpers.py** - there are several additional functions:\
    * def apology - render apology message, if something goes wrong\
    * def login_required - decorate routes to require login\
    * def crop_to_aspect - cut image for needable format\
    * def is_valid_email and def is_valid_username - validate email and username respectively

**guide.db** - database file.\
__Database schema:__\
CREATE TABLE sights (sight_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT NOT NULL, address TEXT, mark NUMERIC, categories TEXT, photos TEXT, description TEXT);\
CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, email TEXT NOT NULL, hash TEXT NOT NULL);\
CREATE TABLE favourites (favourite_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, user_id INTEGER NOT NULL, sight_id INTEGER NOT NULL);\
CREATE TABLE categories (category_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT NOT NULL, fullname TEXT NOT NULL);\
CREATE UNIQUE INDEX username ON users (username);\
CREATE UNIQUE INDEX email ON users (email);\

**styles.scss** - styles of project, including media queries. A lot of styles provide by Bootstrap, so a lot of styles are in .html files.\ 
**index.js** - a little file, that helps to work modal window perfectly, add class "favourited" for needable card and highlight choosed category on category page\
and **a bunch of location's pictures** - just a pictures for location's cards and profiles.