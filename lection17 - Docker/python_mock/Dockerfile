FROM python:3.9


COPY requirements.txt /requirements.txt
RUN pip3.9 install -r /requirements.txt && rm -rf /requirements.txt

WORKDIR /code
CMD ["pytest", "-s", "-l", "-v", "tests/test.py", "--alluredir", "/tmp/alluredir"]