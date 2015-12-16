virtualenv env -p python3
echo ‘Virtualenv set up with python3’
source env/bin/activate
echo ’Virtualenv activated’
cd src
echo ‘setup complete, to start the server run: python manage.py runserver’