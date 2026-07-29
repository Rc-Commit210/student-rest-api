install:
	pip install -r requirements.txt

run:
	python run.py

test:
	python -m pytest -v

migrate:
	flask db upgrade

makemigrations:
	flask db migrate -m "Auto Migration"

freeze:
	pip freeze > requirements.txt

clean:
	rm -rf __pycache__
	rm -rf .pytest_cache