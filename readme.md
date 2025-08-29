flask db init
flask db migrate -m "create role table"
flask db upgrade
source venv/bin/activate
pip freeze > requirements.txt

