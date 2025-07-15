To generate a secret_key use:
python -c "import secrets; print(secrets.token_hex(16))"

for dependencies add these via terminal:
pip install flask psycopg2-binary flask-login flask-sqlalchemy flask-wtf python-dotenv

add these in requirements.txt by :
pip freeze > requirements.txt

your db_url and secret_key must be in .env and this .env must added to gitignore