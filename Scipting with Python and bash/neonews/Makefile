VENV_DIR := venv
APP_NAME := cli.py

install:
	python3 -m venv $(VENV_DIR)
	. $(VENV_DIR)/bin/activate && pip install --upgrade pip && pip install -r requirements.txt


run:
	. $(VENV_DIR)/bin/activate && python $(APP_NAME)


create-db:
	. $(VENV_DIR)/bin/activate && python scripts/create_dynamodb.py


sync-news:
	. $(VENV_DIR)/bin/activate && python scripts/fetch_news.py


export-briefings:
	python scripts/fetch_news.py --export


clean:
	rm -rf $(VENV_DIR)