source ./venv/bin/activate
pip freeze | grep -v "pkg-resources" > requirements.txt
cd apps
python3 manage.py makemigrations
python3 manage.py migrate
deactivate
git status
