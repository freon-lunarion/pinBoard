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
4. Navigate to running server page (http://127.0.0.1:8000 port may be different based on configuration)

### Feature Tryout Instructions




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
