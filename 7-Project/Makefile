LOCAL_TAG:=$(shell date +"%Y-%m-%d-%H-%M-%S")
LOCAL_IMAGE_NAME="project-mlops:${LOCAL_TAG}"
test:
	pytest tests/

quality_checks:
	isort .
	black .
	pylint --recursive=y

build: quality_checks test 

	docker build -t ${LOCAL_IMAGE_NAME} .

publish: build
	docker push $LOCAL_IMAGE_NAME
	
test_1:
	echo ${LOCAL_TAG} ${LOCAL_IMAGE_NAME}