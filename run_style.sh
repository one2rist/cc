source env/bin/activate
cd apps
autopep8 --in-place -r .
flake8 . --max-line-length=127
deactivate
cd ..
git status
