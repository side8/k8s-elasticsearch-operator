#!/bin/bash

# set -vxeo pipefail

echo "START ========================" >&2

# TODO move defaults into CRD resource definition
K8S_SPEC_DATA_REPLICAS=${K8S_SPEC_DATA_REPLICAS:=2}
K8S_STATUS_DATA_REPLICAS=${K8S_STATUS_DATA_REPLICAS:=0}

K8S_SPEC_MASTER_REPLICAS=${K8S_SPEC_MASTER_REPLICAS:=3}
K8S_STATUS_MASTER_REPLICAS=${K8S_STATUS_MASTER_REPLICAS:=0}


if [[ ${K8S_STATUS_DATA_REPLICAS} > ${K8S_SPEC_DATA_REPLICAS} ]] ; then
    curl -fso/dev/null -XPUT -d '{"transient": {"cluster.routing.allocation.exclude._name": "'$(seq -f"${K8S_METADATA_NAME}-data-%g" -s, ${K8S_SPEC_DATA_REPLICAS} ${K8S_STATUS_DATA_REPLICAS})'"}}' ${ES_URL}/_cluster/settings
    while curl -fs ${ES_URL}/_cat/shards?h=n | grep "$(seq -f"${K8S_METADATA_NAME}-data-%g$" -s, ${K8S_SPEC_DATA_REPLICAS} ${K8S_STATUS_DATA_REPLICAS})" >/dev/null ; do
        echo "waiting on moving shards..." >&2
        sleep 5
    done
else
    curl -fso/dev/null -XPUT -d '{"transient": {"cluster.routing.allocation.exclude._name": null}}' ${ES_URL}/_cluster/settings || true
fi

if [[ ${K8S_STATUS_MASTER_REPLICAS} != ${K8S_SPEC_MASTER_REPLICAS} ]] ; then
    # scaling down prep
    # keep min_masters the same, remove 1 master node
    if [[ ${K8S_STATUS_MASTER_REPLICAS} > ${K8S_SPEC_MASTER_REPLICAS} ]] ; then
        export LOCAL_MIN_MASTERS=$(($K8S_STATUS_MASTER_REPLICAS/2+1))
	export K8S_SPEC_MASTER_REPLICAS=$((${K8S_STATUS_MASTER_REPLICAS}-1))
        echo "K8S_SPEC_MASTER_REPLICAS=${K8S_SPEC_MASTER_REPLICAS} K8S_STATUS_MASTER_REPLICAS=${K8S_STATUS_MASTER_REPLICAS} LOCAL_MIN_MASTERS=${LOCAL_MIN_MASTERS}" >&2
        kubectl apply -f <( envsubst < es.yaml.template ) >/dev/null
        [[ ${LOCAL_MIN_MASTERS} -le ${K8S_SPEC_MASTER_REPLICAS} ]] && kubectl -n ${K8S_METADATA_NAMESPACE} rollout status statefulset/${K8S_METADATA_NAME}-data >&2
    # scaling up prep
    # set min_masters to 1 more, keep master nodes the same
    elif [[ ${K8S_STATUS_MASTER_REPLICAS} < ${K8S_SPEC_MASTER_REPLICAS} ]] ; then
	export LOCAL_MIN_MASTERS=$(($(($K8S_STATUS_MASTER_REPLICAS+1))/2+1))
	export K8S_SPEC_MASTER_REPLICAS=${K8S_STATUS_MASTER_REPLICAS}
        echo "K8S_SPEC_MASTER_REPLICAS=${K8S_SPEC_MASTER_REPLICAS} K8S_STATUS_MASTER_REPLICAS=${K8S_STATUS_MASTER_REPLICAS} LOCAL_MIN_MASTERS=${LOCAL_MIN_MASTERS}" >&2
        kubectl apply -f <( envsubst < es.yaml.template ) >/dev/null
        [[ ${LOCAL_MIN_MASTERS} -le ${K8S_SPEC_MASTER_REPLICAS} ]] && kubectl -n ${K8S_METADATA_NAMESPACE} rollout status statefulset/${K8S_METADATA_NAME}-data >&2
	export K8S_SPEC_MASTER_REPLICAS=$((${K8S_STATUS_MASTER_REPLICAS}+1))
    fi
    kubectl -n ${K8S_METADATA_NAMESPACE} rollout status statefulset/${K8S_METADATA_NAME}-master >&2
fi

LOCAL_MIN_MASTERS=$(($K8S_SPEC_MASTER_REPLICAS/2+1))

export K8S_SPEC_MASTER_REPLICAS
export LOCAL_MIN_MASTERS

echo "K8S_SPEC_MASTER_REPLICAS=${K8S_SPEC_MASTER_REPLICAS} K8S_STATUS_MASTER_REPLICAS=${K8S_STATUS_MASTER_REPLICAS} LOCAL_MIN_MASTERS=${LOCAL_MIN_MASTERS}" >&2
kubectl apply -f <( envsubst < es.yaml.template ) >/dev/null
kubectl -n ${K8S_METADATA_NAMESPACE} rollout status statefulset/${K8S_METADATA_NAME}-master >&2
kubectl -n ${K8S_METADATA_NAMESPACE} rollout status statefulset/${K8S_METADATA_NAME}-data >&2

echo '{"data": {"replicas": '${K8S_SPEC_DATA_REPLICAS}'}, "master": {"replicas": '${K8S_SPEC_MASTER_REPLICAS}'}}'
echo "END ========================" >&2
