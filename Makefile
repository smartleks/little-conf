.PHONY: all help check build test build_image lint autoformat runbash

IMAGE_NAME=simple-settings

LINTER_IMAGE=builder.local:18079/common/python_linters:latest
LINTER_PULL_POLICY=--pull always
LINTER_BASE_CMD=docker run ${LINTER_PULL_POLICY} -it --rm -v ${PWD}:/sources/ --network=host
PIP_INDEX_URL=http://builder.local:8081/repository/pypi_all/simple


GREEN := $(shell tput -Txterm setaf 2)
RESET := $(shell tput -Txterm sgr0)


all: help

help: # autohelp
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' Makefile | sort -g -s -r | awk 'BEGIN {FS = ":"}; {printf "\033[36m%-35s\033[0m # %s\n", $$1, $$2}' | sed -e 's/#.*## //g'
	@echo

check: lint build_package runtests  ## Run all checks

build: runtests build_image  ## Build package
	@docker run --rm -v /tmp/dist:/app/dist -e PIP_INDEX_URL=${PIP_INDEX_URL} ${IMAGE_NAME} poetry build || exit=$?
	@echo "${GREEN}Packet upload to /tmp/dist${RESET}"
	@echo "${GREEN}Type: pip install /tmp/dist/little_conf-0.0.0.tar.gz${RESET}"

test: runtests  ## Run tests

runtests: build_image  ## Run tests
	docker run --rm ${IMAGE_NAME} python -m pytest tests/
	docker run --rm -e service_env='empty' ${IMAGE_NAME} python -m pytest tests/test_simple.py -k 'test_empty_conf_set_by_env'

build_image:  ## Build image
	docker build --network=host -t ${IMAGE_NAME} .

lint:  ## Run linters
	${LINTER_BASE_CMD} --entrypoint run.sh ${LINTER_IMAGE} /sources/
	${LINTER_BASE_CMD} --entrypoint mypy.sh ${LINTER_IMAGE} /sources/

autoformat: ## Run autoformatters
	${LINTER_BASE_CMD} --user `id -u`:`id -g` --entrypoint autoformat.sh ${LINTER_IMAGE} /sources/

runbash: build_image  # Run bash in docker
	docker run --rm -it \
	--network host \
	--cpus=1 \
	-e PYTHONDONTWRITEBYTECODE=1 \
	-e PYTHONUNBUFFERED=1 \
	-e CONFIG_ENV=local \
	--name=${IMAGE_NAME} \
	-v `pwd`:/app \
	--entrypoint=bash \
	${IMAGE_NAME}
