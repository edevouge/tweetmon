image := tweetmon
version := $(shell git describe --abbrev=0 --tags)
registry := ${DOCKER_ID_USER:-default edevouge}

build: ## Build the docker image (version latest)

	docker build -t ${image} .


build-nc: ## Build the docker image without caching (version latest)

	docker build --no-cache -t ${image} .


tag: ## Tag image with last git tag

	docker tag ${image}:latest ${image}:${version}


push: ## Push image to repo

		docker tag ${image}:${version} ${registry}/${image}:${version}
		docker push ${registry}/${image}:${version}


all: build-nc tag push
