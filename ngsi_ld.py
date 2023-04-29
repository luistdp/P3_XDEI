import requests
import json
import pprint

base_path = 'http://localhost:1026/ngsi-ld/v1'
LINK = "<http://context/tutorials-context.jsonld>; rel='http://www.w3.org/ns/json-ld#context'; type='application/ld+json'"
# Operaciones CRUD sobre entidades

def set_headers(context_link = None,
                content_type = "application/ld+json"):
    headers = dict()
    if content_type:
        headers["Content-Type"] = content_type
    if context_link:
        headers["Link"] = context_link
    return headers

def create_entity(entity,headers):
    request = base_path + '/entities/'
    r = requests.post(request, data=json.dumps(entity),
                      headers=headers)
    return r.status_code

def list_entities(type = "", options = "count",
                  attrs = None, q = None, headers = None):
    request = base_path + '/entities/'
    if options in ['count', 'keyValues','values']:
        request += f'?options={options}'
    if type is not None:
        request += f'&type={type}'
    if attrs is not None:
        request += f'&attrs={attrs}'
    if q is not None:
        request += f'&q={q}'
    r = requests.get(request,
                     headers=headers)
    print(r.text)
    return (r.status_code, json.loads(r.text))

def read_entity(entity_id, headers = None):
    request = base_path + f'/entities/{entity_id}'
    r = requests.get(request,headers=headers)
    return (r.status_code, json.loads(r.text))

def delete_entity(entity_id,headers = None):
    request = base_path + f'/entities/{entity_id}'
    r = requests.delete(request,headers=headers)
    print(r.text)
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

def batch_create(entity_attr_list, headers = None):
    request = base_path + '/entityOperations/upsert?options=update'
    r = requests.post(request, data = json.dumps(entity_attr_list), 
                      headers=headers)
    print(r.text)
    return r.status_code

def batch_update(entity_attr_list, headers = None):
    request = base_path + '/entityOperations/update'
    r = requests.post(request,data=json.dumps(entity_attr_list),
                       headers=headers)
    print(r.text)
    return r.status_code

def batch_delete(entity_id_list, headers = None):
    request = base_path + '/entityOperations/delete'
    r = requests.post(request,json = entity_id_list, headers=headers)
    print(r.text)
    return r.status_code

if __name__ == "__main__":
    headers = set_headers(context_link=LINK, content_type=None)
    pprint.pprint(list_entities(type="Product", headers=headers))
    test = [
        {'id': 'urn:ngsi-ld:Product:012',
   'name': {'type': 'Property', 'value': 'Beer'},
   'price': {'currency': {'type': 'Property', 'value': 'EUR'},
             'type': 'Property',
             'value': 0.99},
   'size': {'type': 'Property', 'value': 'S'},
   'type': 'Product'},
  {'id': 'urn:ngsi-ld:Product:013',
   'name': {'type': 'Property', 'value': 'Red Wine'},
   'price': {'currency': {'type': 'Property', 'value': 'EUR'},
             'type': 'Property',
             'value': 10.99},
   'size': {'type': 'Property', 'value': 'M'},
   'type': 'Product'}
    ]
    headers = set_headers(context_link=LINK, content_type="application/json")
    status = batch_create(test,headers=headers)
    print(status)
    headers = set_headers(context_link=LINK, content_type=None)
    pprint.pprint(list_entities(type="Product", headers=headers))
    test = [
        {'id': 'urn:ngsi-ld:Product:012',
   'name': {'type': 'Property', 'value': 'Snow'},
   'price': {'currency': {'type': 'Property', 'value': 'EUR'},
             'type': 'Property',
             'value': 10000},
   'size': {'type': 'Property', 'value': 'S'},
   'type': 'Product'},
  {'id': 'urn:ngsi-ld:Product:013',
   'name': {'type': 'Property', 'value': 'Blue Wine'},
   'price': {'currency': {'type': 'Property', 'value': 'EUR'},
             'type': 'Property',
             'value': 50000},
   'size': {'type': 'Property', 'value': 'M'},
   'type': 'Product'}
    ]
    headers = set_headers(context_link=LINK, content_type="application/json")
    batch_update(test, headers=headers)
    headers = set_headers(content_type="application/json")
    #pprint.pprint(list_entities(type="Shelf", headers=headers))
    batch_delete(['urn:ngsi-ld:Product:012','urn:ngsi-ld:Product:013'],headers=headers)
    headers = set_headers(context_link=LINK,content_type=None)
    pprint.pprint(list_entities(type="Shelf",options="keyValues",headers=headers))