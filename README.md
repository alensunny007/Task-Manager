To generate a secret_key use:
python -c "import secrets; print(secrets.token_hex(16))"

for dependencies add these via terminal:
pip install flask psycopg2-binary flask-login flask-sqlalchemy flask-wtf python-dotenv

add these in requirements.txt by :
pip freeze > requirements.txt

your db_url and secret_key(without_quotes) must be in .env and this .env must added to gitignore

db_url format:DB_URL=postgresql://username:password@host:port/dbname

for creating tabele first, set all the models you needed in app.models then use flask shell:
from app.models import db
db.create_all()
check the table is created using pgadmin4
