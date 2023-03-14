ifeq ($(OS), Windows_NT)
py_exe := python
else
py_exe := python3
endif

install:
	pip3 install -r requirements.txt
run:
	$(py_exe) main.py