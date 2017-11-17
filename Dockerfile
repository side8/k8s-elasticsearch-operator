FROM python:3.6

RUN pip install --no-cache-dir git+https://github.com/side8/k8s-operator@master
ADD https://storage.googleapis.com/kubernetes-release/release/v1.7.9/bin/linux/amd64/kubectl /usr/local/bin/kubectl
RUN chmod +x /usr/local/bin/kubectl
RUN apt-get update && apt-get install -y gettext-base

COPY startup.sh apply delete crd.yaml es.yaml.template ./

ENTRYPOINT ["./startup.sh"]
