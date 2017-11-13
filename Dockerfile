FROM python:3.6

COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY apply.sh delete.sh operator.py ./

ENTRYPOINT ["python", "operator.py"]
