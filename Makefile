ifeq ($(OS), Windows_NT)
py_exe := python
else
py_exe := python3
endif

install:
	pip3 install -r requirements.txt
run:
	$(py_exe) main.py
docker:
	docker build -t chatbot .
	docker run -p 8080:8080 chatbot
