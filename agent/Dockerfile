FROM sdn-base:latest

COPY agent /opt/agent
COPY requirements.txt /opt/agent/

RUN pip install -r /opt/agent/requirements.txt
RUN export FLASK_APP=/opt/agent/start.py

CMD python -m flask run