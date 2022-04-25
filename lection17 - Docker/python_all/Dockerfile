FROM python:3.9


COPY requirements.txt /requirements.txt
RUN pip3.9 install -r /requirements.txt && rm -rf /requirements.txt

CMD ["/code/start_tests.sh"]