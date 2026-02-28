.PHONY: install test lint run format docker-build docker-test

install:
	pip install -r requirements.txt
	pip install pytest ruff

test:
	pytest tests/ -v

lint:
	ruff check .

format:
	ruff format .

run:
	python main.py

docker-test:
	docker-compose run --rm sotm-test

docker-sim:
	docker-compose run --rm sotm-sim

clean:
	rm -rf __pycache__ .pytest_cache
	rm -f *.csv
	rm -f *.png
