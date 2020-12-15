# BeezBlog

## Author 
[Barnabas-Kamau] (https://github.com/barnabas27)

#Live Link:


## Description.
- BeezBlog is a personal blogging website where you can create and share opinions and other users can read and comment on them. It has an additional feature in that it displays random quotes to inspire the users.

## User Stories
What the user does:
* Register an account by signing up.
* Comment on blogs
* Subscribe for notification of any new blogs.
* See random quotes on the site

## Writer Stories:
* Can create a blog from the application
* Can delete comments that one finds not up-to standard.
* Can update or delete blogs


## Setup Installations Requirements
* To run the application, in your terminal:
    1. Clone or download the Repository
    2. Create a virtual environment
    3. Read the requirements file and install all the requirements alternatively you  could run pip3 install -r requirements.txt to automatically install all the requirements.
    4. Prepare environment variables
    5. export your DATABASE_URL and SECRET_KEY
    6. Run chmod a+x start.sh
    7. Run ./start.sh
    8. Access the application throught the link or local server 'localhost:5000'

#### For the user to operate you need to install:
* Python and its subsequent versions.
* pip





## BDD
| Behaviour | Input | Output |
| :---------------- | :---------------: | ------------------: |
|After the installation | Run the command ```$ ./start.sh```| Displays the link<br>*'localhost:5000'|
|Landing on home page| Press ctrl button + left click| Opens Home Page and displays random quotes|
|To view the random quotes | Click ```home```/continously refresh page|  Displays Home page with random quotes after every refresh|
|Open all blogs|Click on the ``` blogs ```|Directs you to where all the blogs are |
|To add new blog | navigate to ```create a blog```|A form appears where you add a blog. |
|To subscribe|navigate to the ```subscribe```button|A form appears and prompts user to subscribe|
|To comment on any blog|once signed in navigate to ```comment```|Leave a respectful comment|


## Technologies used
* python3
* flask frameworks
* Html,CSS(bootstrap)
* PostgreSQL
* Pip

## known bugs
* No known bugs at the moment
## Contact information
* for questions of contributions:
[bkamau032@gmail.com]

## License
* [[License:MIT]](LICENSE.md)
* copyright (c) 2020 **Barnabas Kamau**