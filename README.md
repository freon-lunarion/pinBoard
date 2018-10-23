# pinBoard

### App Deployment Instructions

*Requirements:*  
  Python 3, pip3, virtualenv

*First time install:*

1. Download the lastest packages from https://github.com/freon-lunarion/pinBoard/archive/master.zip
2. Unzip master.zip
3. Open terminal, go to unzipped directory
4. Make virtual enviroment by running: virtualenv venv 
5. Activate virtual environment : source venv/bin/active
6. Install dependencies with: pip install -r requirement.txt
7. Run: chmod +x setup.sh
8. Run: ./setup.sh
9. Follow the instructions to make super user (admin)


*Running the server:*

1. Activate the virtualenv with : source venv/bin/activate
2. Open terminal, go to master directory
3. Run: python manage.py runserver
4. Navigate to running server page (http://127.0.0.1:8000 port may be different based on system configuration)

### Feature Tryout Instructions

*Create Posts:*

1. Click the 'Create Post' button on the navigation bar.
2. Choose a type of post to create.
3. For images and youtube videos, input title and url to the resource.
4. For articles and questions, input title and detail of the post. Tags should be separated by comma.
5. Submit the post.


*Vote for Posts, Commments and Answers:*

1. Posts can be voted on home page, with self-sorting feature.
2. Click 'Open' button of a post, go to the post detail page.
3. Posts, Commments and Answers can be voted on post detail page.
4. Comments and Answers will be sorted by score after refreshing the page.


*Save Posts:*

1. Posts can be saved as favorite posts via the save button (heart shaped) on either home page or post detail page.
2. Favorited posts are displayed on user profile page.


*Pin Posts:*

1. Moderators (superusers) can pin posts on home page via the pin button on the card of the post.
2. Pinned posts are displayed on the top of home page.


*Search Posts:*

1. Input in the search bar on the navigation bar, type enter to start the search.
2. Add 'post', 'image', 'youtube' or 'question' to the keywords for searching articles only, images only, videos only or questions only.
3. Type '#' at the beginning to search tags. Tags should be separated by a comma.


*Quiz Sets & Quizzes:*

1. Go to the quiz sets page by clicking the Quiz Sets button in the nav bar.
2. Create a new Quiz Set via the Create Set button
3. Give the set a title and description, as well as the minimum score for a successful quiz tryout (attempt) and number of questions to display during tryout.
4. Click Submit button to create the set.
5. Open an existing quiz set by clicking Open at the bottom of its card.
6. Add new questions via the '...' button followed by the blue New Question button.
7. Type in the question in the detail box, and provide up to 4 multiple choice options in the options areas, being sure to choose which of the options is the right answer.
8. Click the Submit button to add the question to the quiz set.
9. Tryout a quiz via the '...' button followed by the red Tryout button.
10. Clicking the blue tick button on completion gives your results.


*Leaderboard:*

1. Click the 'Leaderboard' button on the navigation bar.
2. Top ten users with highest scores are displayed.


*User Profile:*

1. Click the 'Hello, Username' button on the navigation bar.
2. The user's favorite posts, top five posts with highest scores, all types of posts and quiz sets are displayed on the user profile page.
3. User avatar can be uploaded by clicking the avatar image.

### How To View Source Code

*File Structure:*
pinBoard 
  - blogs 
  - livesession 
  - quiz 
  - shared 
  - pinboard 
    - settings.py 
    - urls.py 
    - wsgi.py
    
  - sample (sample data)
  - manage.py 
  - requirement.txt
  - setup.sh
  
There are three apps in this project: __blogs__, __quiz__ and __shared__. The __blogs__ app is for features dealing with posts, the __quiz__ app is for quiz set feature, and the __shared__ app is for handling shared models and pages such as the user profile model and the user profile page. The nested pinboard directory, contain the project setting (setting.py) and routing files (url.py). Note: that data model is setup for livesession app, but this app is not implemented due to time limit. So it is not installed, and only for further development.

for every app directory contain:
  - migrations
  - static 
  - templates 
  - admin.py 
  - apps.py 
  - forms.py 
  - test.py 
  - urls.py 
  - models.py 
  - views.py 


__models.py__, contain the data layer describing tables, fields attribute and custom user query for data access layer

__urls.py__, contain routing url to views.py fuctions or classes

__views.py__, contain classes or function for backend bussiness logic layer

__forms.py__, __static__ and __templates__, for presentation layer (frontend) to configure django generic forms, put external resources (css,js image) and html templating files respectively  

### Issues

The project is rendered best on Chrome. Small displaying issues may occur on Safari or Firefox.

# Reference Documents
*Python3 & pip*

* Mac: https://docs.python-guide.org/starting/install3/osx/
* Linux https://docs.python-guide.org/starting/install3/linux/
* Windows: https://docs.python-guide.org/starting/install3/win/

*Virtualenv*

* Mac: https://docs.python-guide.org/dev/virtualenvs/#lower-level-virtualenv
* Linux: https://docs.python-guide.org/dev/virtualenvs/#lower-level-virtualenv
* Windows: https://docs.python-guide.org/dev/virtualenvs/#lower-level-virtualenv

Django 2.1 : https://docs.djangoproject.com/en/2.1/
