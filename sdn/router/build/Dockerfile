FROM sdn-base:latest

#COPY router /opt/router
COPY requirements.txt /opt/router/

RUN pip install -r /opt/router/requirements.txt
RUN export FLASK_APP=/opt/router/start.py

CMD python -m flask run