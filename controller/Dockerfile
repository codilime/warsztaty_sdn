FROM sdn-base:latest

COPY sdn /opt/sdn
COPY requirements.txt /opt/sdn/

RUN pip install -r /opt/sdn/requirements.txt
RUN export FLASK_APP=/opt/flaskapp/app.py

CMD export PYTHONPATH="${PYTHONPATH}:${PWD}"; python -m flaskapp.app    