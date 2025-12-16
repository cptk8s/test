venv:
	python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt

test:
	. .venv/bin/activate && pytest -q

build:
	docker build -t myflaskapi:latest .

run:
	docker run -p 5000:5000 myflaskapi:latest
