source env/bin/activate
pip freeze | grep -v "pkg-resources" > requirements.txt
cd apps
python manage.py makemigrations
python manage.py migrate
deactivate
cd ..
git status
