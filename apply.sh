#!/bin/bash

kubectl apply -f <( envsubst < es.yaml.template ) >&2
echo '{"master": {"replicas": '${current_master_replicas}'}}'
echo "========================" >&2
