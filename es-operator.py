import kubernetes
from pprint import pprint
import sys
from six import iteritems
import subprocess
import os
import yaml


try:
    kubernetes.config.load_incluster_config()
    print( "configured in cluster with service account" )
except:
    try:
        kubernetes.config.load_kube_config()
        print( "configured via kubeconfig file" )
    except:
        print( "No Kubernetes configuration found" )
        sys.exit(1)

# print(dir(kubernetes.client))
# custom_objects_api_instance = kubernetes.client.ExtensionsApi()


class CustomObjectsApiWithUpdate(kubernetes.client.CustomObjectsApi):
    def update_namespaced_custom_object(self, group, version, namespace, plural, name, body, **kwargs):
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.update_namespaced_custom_object_with_http_info(group, version, namespace, plural, name, body, **kwargs)
        else:
            (data) = self.update_namespaced_custom_object_with_http_info(group, version, namespace, plural, name, body, **kwargs)
            return data

    def update_namespaced_custom_object_with_http_info(self, group, version, namespace, plural, name, body, **kwargs):
        all_params = ['group', 'version', 'namespace', 'plural', 'name', 'body']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_namespaced_custom_object" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'group' is set
        if ('group' not in params) or (params['group'] is None):
            raise ValueError("Missing the required parameter `group` when calling `update_namespaced_custom_object`")
        # verify the required parameter 'version' is set
        if ('version' not in params) or (params['version'] is None):
            raise ValueError("Missing the required parameter `version` when calling `update_namespaced_custom_object`")
        # verify the required parameter 'namespace' is set
        if ('namespace' not in params) or (params['namespace'] is None):
            raise ValueError("Missing the required parameter `namespace` when calling `update_namespaced_custom_object`")
        # verify the required parameter 'plural' is set
        if ('plural' not in params) or (params['plural'] is None):
            raise ValueError("Missing the required parameter `plural` when calling `update_namespaced_custom_object`")
        # verify the required parameter 'name' is set
        if ('name' not in params) or (params['name'] is None):
            raise ValueError("Missing the required parameter `name` when calling `update_namespaced_custom_object`")
        # verify the required parameter 'body' is set
        if ('body' not in params) or (params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `update_namespaced_custom_object`")


        collection_formats = {}

        resource_path = '/apis/{group}/{version}/namespaces/{namespace}/{plural}/{name}'.replace('{format}', 'json')
        path_params = {}
        if 'group' in params:
            path_params['group'] = params['group']
        if 'version' in params:
            path_params['version'] = params['version']
        if 'namespace' in params:
            path_params['namespace'] = params['namespace']
        if 'plural' in params:
            path_params['plural'] = params['plural']
        if 'name' in params:
            path_params['name'] = params['name']

        query_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/merge-patch+json', 'application/strategic-merge-patch+json'])

        # Authentication setting
        auth_settings = ['BearerToken']

        return self.api_client.call_api(resource_path, 'PATCH',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='object',
                                        auth_settings=auth_settings,
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)



custom_objects_api_instance = CustomObjectsApiWithUpdate()
extensions_v1beta2_api_instance = kubernetes.client.ExtensionsV1beta1Api()

fqdn = 'db.side8.io'
version = 'v1'
resource = 'elasticsearchs'

print ("\nCalling list_namespaced_custom_object for 'telemetry' namespace\n")


def parse(o, prefix=""):
    def flatten(lis):
        new_lis = []
        for item in lis:
            if type(item) == type([]):
                new_lis.extend(flatten(item))
            else:
                new_lis.append(item)
        return new_lis
            
    try:
        return {
            "str": lambda : (prefix, o),
            "int": lambda : parse(str(o), prefix=prefix),
            "NoneType": lambda : parse("", prefix=prefix),
            "list": lambda : flatten([parse(io, "{}{}{}".format(prefix, "_" if prefix else "", ik).upper()) for ik, io in enumerate(o)]),
            "dict": lambda : flatten([parse(io, "{}{}{}".format(prefix, "_" if prefix else "", ik).upper()) for ik, io in o.items()]),
        }[type(o).__name__]()
    except KeyError:
        raise


w = kubernetes.watch.Watch()
for event in w.stream(custom_objects_api_instance.list_cluster_custom_object, fqdn, version, resource, _request_timeout=60):
    namespace = event['object']['metadata']['namespace']
    name = event['object']['metadata']['name']
    deletion_timestamp = event['object']['metadata']['deletionTimestamp']
    kind = event['object']['kind']
    uid = event['object']['metadata']['uid']
    resource_version = event['object']['metadata']['resourceVersion']
    try:
        finalizers = event['object']['metadata']['finalizers']
    except KeyError:
        finalizers = []
    api_version = event['object']['apiVersion']
    event_type = event['type']
    # print("Event: {} {} named {} in {}".format(event['type'], event['object']['kind'], event['object']['metadata']['name'], event['object']['metadata']['namespace']))
    if event_type in ["ADDED", "MODIFIED"]:
        spec = event['object']['spec']
        subprocess_env = dict([("_DOLLAR", "$")] + parse(event['object'], prefix="K8S"))
        # subprocess_env = {"K8S_METADATA_NAMESPACE": namespace, "K8S_METADATA_NAME": name, "K8S_SPEC_MASTER_REPLICAS": str(spec['master']['replicas'])}
        if deletion_timestamp is not None:
            if "OldSchoolGC" in finalizers:
                try:
                    subprocess.check_call(["/bin/bash", "delete.sh"], env=dict(list(os.environ.items()) + list(subprocess_env.items())))
                except kubernetes.client.rest.ApiException as e:
                    if e.status != 404:
                        raise
                custom_objects_api_instance.update_namespaced_custom_object(fqdn, version, namespace, resource, name, {"metadata": {"ResourceVerion": resource_version, "finalizers": [list(filter(lambda f:  f != "OldSchoolGC", finalizers))]}, "kind": kind, "apiVersion": api_version, "name": name})
            else:
                custom_objects_api_instance.delete_namespaced_custom_object(fqdn, version, namespace, resource, name, body=kubernetes.client.V1DeleteOptions())
        else:
            if "OldSchoolGC" not in finalizers:
                custom_objects_api_instance.update_namespaced_custom_object(fqdn, version, namespace, resource, name, {"metadata": {"finalizers": ["OldSchoolGC"]}, "kind": kind, "apiVersion": api_version, "name": name})
            else:
                # subprocess.check_call(["/bin/bash", "apply.sh"], env=dict(list(os.environ.items()) + list(subprocess_env.items())))
                process = subprocess.Popen(["/bin/bash", "apply.sh"], env=dict(list(os.environ.items()) + list(subprocess_env.items())), stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1)
                out, err = process.communicate()
                status = yaml.load(out)
                # custom_objects_api_instance.update_namespaced_custom_object(fqdn, version, namespace, resource, name, {"kind": kind, "apiVersion": api_version, "name": name, "status": status})
                custom_objects_api_instance.update_namespaced_custom_object(fqdn, version, namespace, resource, name, {"status": status})
                print("out yo: {}".format(out))
                print("error yo: {}".format(err))
