# define the name of the virtual environment directory
VENV := venv
IMAGE := myapp

# default target, when make executed without arguments
all: env

help: ## Shows the help
	@echo 'Usage: make <OPTIONS> ... <TARGETS>'
	@echo ''
	@echo 'Available targets are:'
	@echo ''
	@grep -E '^[ a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
        awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ''

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	./$(VENV)/bin/pip3 install -r requirements.txt --upgrade pip

env: $(VENV)/bin/activate ## venv is a shortcut target

run: env ## to run a code
	./$(VENV)/bin/python3 app/main.py

clean: ## remove generated files
	@rm -rf $(VENV)
	@rm -rf files

run-docker: ## run the app with docker and copy files from docker to local
	docker build -t $(IMAGE) . 
	docker run -v $(PWD)/files:/app/files $(IMAGE)
	docker rm -f $$(docker ps -a -q --filter="ancestor=$(IMAGE)")
	docker rmi $(IMAGE)

delete-docker: ## delete generated container and image
	docker rm -f $$(docker ps -a -q --filter="ancestor=$(IMAGE)")
	docker rmi $(IMAGE)

.PHONY: all env run clean run-docker delete-docker