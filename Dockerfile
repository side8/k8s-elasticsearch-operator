FROM python:3.6

RUN pip install --no-cache-dir git+https://github.com/side8/k8s-operator@master

COPY apply delete ./

ENTRYPOINT ["side8-operator", "--resource", "elasticsearchs", "--fqdn", "db.side8.io", "--version", "v1" ]
