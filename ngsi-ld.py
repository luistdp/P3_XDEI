import requests
import json
import pprint

base_path = 'http://localhost:1026/ngsi-ld/v1'
LINK = "<http://context/tutorials-context.jsonld>; rel='http://www.w3.org/ns/json-ld#context'; type='application/ld+json'"
# Operaciones CRUD sobre entidades

def set_headers(context_link = None,
                content_type = "application/ld+json"):
    headers = dict()
    if context_link:
        headers["Link"] = context_link
    if content_type:
        headers["Content-Type"] = content_type
    return headers

def create_entity(entity,headers):
    request = base_path + '/entities/'
    r = requests.post(request, data=json.dumps(entity),
                      headers=headers)
    print(r.text)
    return r.status_code

def list_entities(type = "", options = "count",
                  attrs = None, headers = None):
    request = base_path + '/entities/'
    if options in ['count', 'keyValues','values']:
        request += f'?options={options}'
    if type is not None:
        request += f'&type={type}'
    if attrs is not None:
        request += f'&attrs={attrs}'
    r = requests.get(request,
                     headers=headers)
    return (r.status_code, json.loads(r.text))

def read_entity(entity_id, headers = None):
    request = base_path + f'/entities/{entity_id}'
    r = requests.get(request,headers=headers)
    return (r.status_code, json.loads(r.text))

def delete_entity(entity_id,headers = None):
    request = base_path + f'/entities/{entity_id}'
    r = requests.delete(request,headers=headers)
    return r.status_code

# Operaciones CRUD sobre atributos

def read_attr(entity_id,attr,headers = None):
    request = base_path + f'/entities/{entity_id}'
    request = request + f'?attrs={attr}&options=keyValues'
    r = requests.get(request,headers=headers)
    return (r.status_code, json.loads(r.text))

def update_attr(entity_id, attr_vals, headers = None):
    request = base_path + f'/entities/{entity_id}'
    request = request + '/attrs'
    r = requests.patch(request, data=json.dumps(attr_vals), 
                      headers=headers)
    print(r.text)
    return r.status_code

def delete_attr(entity_id, attr, headers = None):
    request = base_path + f'/entities/{entity_id}'
    request = request + f'/attrs/{attr}'
    r = requests.delete(request,headers=headers)
    return r.status_code
