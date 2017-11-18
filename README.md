# [side8.io](http://side8.io) Kubernetes Elasticsearch Operator


## Usage

Create the operator namespace by running `kubectl create namespace operator`.

Run `kubectl deploy https://raw.githubusercontent.com/side8/k8s-elasticsearch-operator/master/operator.yaml` to deploy the Elasticsearch operator into your cluster.

Once configured you can deploy and interact with `Elasticsearch` resources:
```
$ cat es.yaml

apiVersion: "db.side8.io/v1"
kind: ElasticSearch
metadata:
  name: es-test-yo
spec:
  master:
    replicas: 3
  data:
    replicas: 4

$ kubectl apply -f es.yaml
```

## Settings

| field                | description                     | default |
|----------------------|---------------------------------|---------|
| spec.master.replicas | sets the number of master nodes |       3 |
| spec.data.replicas   | sets the number of data nodes   |       2 |
