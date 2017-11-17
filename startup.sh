#!/bin/bash

set -eo pipefail

kubectl apply -f crd.yaml

exec side8-k8s-operator --resource elasticsearchs --fqdn db.side8.io --version v1
