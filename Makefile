.DEFAULT_GOAL := help

all: help requirements init

.PHONY: help all

requirements: ## create requirements.txt
	pip freeze > requirements.txt

init: ## pip install
	pip install -r requirements.txt

help: ## generate make help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
