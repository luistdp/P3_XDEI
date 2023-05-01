import ngsi_ld
import json


# PARA LA CREACIÓN DE LAS ENTIDADES, EN ALGUNOS CASOS SE HA UTILIZADO ngsi-ld.batch_create
# CON EL PROPÓSITO DE REDUCIR EL NÚMERO DE CONSULTAS A ORION

# AÑADIDOS DOS BUILDINGS EN A CORUÑA
building5 = {
    "id": "urn:ngsi-ld:Building:store005",
    "type": "Building",
    "category": {"type": "Property", "value": ["commercial"]},
    "address": {
      "type": "Property", 
      "value": {"streetAddress": "Avenida Ernesto Che Guevara", "addressRegion": "A Coruña", "addressLocality": "Perillo", "postalCode": "15172"},
      "verified": {"type": "Property", "value": True}
    },
    "location": {"type": "GeoProperty", "value": {"type": "Point", "coordinates": [-8.376475, 43.335578]}
    },
    "name": {"type": "Property", "value": "Autoservicios Familia"},
    "furniture":[
        {
            "type": "Relationship",
            "datasetId": "urn:ngsi-ld:Relationship:1",
            "object": "urn:ngsi-ld:Shelf:unit011"
        },
        {
            "type": "Relationship",
            "datasetId": "urn:ngsi-ld:Relationship:2",
            "object": "urn:ngsi-ld:Shelf:unit012"
        },
        {
            "type": "Relationship",
            "datasetId": "urn:ngsi-ld:Relationship:3",
            "object": "urn:ngsi-ld:Shelf:unit013"
        }
    ],
    "@context":"http://context/tutorials-context.jsonld"
}

headers = ngsi_ld.set_headers(context_link=None)
code = ngsi_ld.create_entity(building5, headers=headers)

building6 = {
    "id": "urn:ngsi-ld:Building:store006",
    "type": "Building",
    "category": {"type": "Property", "value": ["commercial"]},
    "address": {
      "type": "Property", 
      "value": {"streetAddress": "Ctra. Coruña Santiago", "addressRegion": "A Coruña", "addressLocality": "Coruña", "postalCode": "15174"},
      "verified": {"type": "Property", "value": True}
    },
    "location": {"type": "GeoProperty", "value": {"type": "Point", "coordinates": [-8.391196, 43.328730]}
    },
    "name": {"type": "Property", "value": "Alcampo"},
    "furniture":[
        {
            "type": "Relationship",
            "datasetId": "urn:ngsi-ld:Relationship:1",
            "object": "urn:ngsi-ld:Shelf:unit014"
        },
        {
            "type": "Relationship",
            "datasetId": "urn:ngsi-ld:Relationship:2",
            "object": "urn:ngsi-ld:Shelf:unit015"
        },
        {
            "type": "Relationship",
            "datasetId": "urn:ngsi-ld:Relationship:3",
            "object": "urn:ngsi-ld:Shelf:unit016"
        }
    ],
    "@context":"http://context/tutorials-context.jsonld"
}
headers = ngsi_ld.set_headers(context_link=None)
code = ngsi_ld.create_entity(building6, headers=headers)


# AÑADIDAS 6 SHELFS PARA SUPLIR LOS NUEVOS BUILDINGS. 3 POR BUILDING

shelf11 = {
    "id": "urn:ngsi-ld:Shelf:unit011",
    "type": "Shelf",
    "location": {
      "type": "GeoProperty",
      "value": {"type": "Point", "coordinates": [-8.376475, 43.335578]}
    },
    "maxCapacity": {"type": "Property", "value": 50},
    "numberOfItems": {"type": "Property", "value": 15},
    "name": {"type": "Property", "value": "Corner Unit"},
    "stocks": {
      "type": "Relationship", "object": "urn:ngsi-ld:Product:010"
    },
    "locatedIn" : {
      "type": "Relationship", "object": "urn:ngsi-ld:Building:store005",
      "requestedBy": {"type": "Relationship", "object": "urn:ngsi-ld:Person:bob-the-manager"},
      "installedBy": {"type": "Relationship", "object": "urn:ngsi-ld:Person:employee001"},
      "statusOfWork": {"type": "Property", "value": "completed"}
    },
    "@context": "http://context/tutorials-context.jsonld"
}

shelf12 = {
    "id": "urn:ngsi-ld:Shelf:unit012",
    "type": "Shelf",
    "location": {
      "type": "GeoProperty",
      "value": {"type": "Point", "coordinates": [-8.376475, 43.335578]}
    },
    "maxCapacity": {"type": "Property", "value": 50},
    "numberOfItems": {"type": "Property", "value": 15},
    "name": {"type": "Property", "value": "Corner Unit"},
    "stocks": {
      "type": "Relationship", "object": "urn:ngsi-ld:Product:011"
    },
    "locatedIn" : {
      "type": "Relationship", "object": "urn:ngsi-ld:Building:store005",
      "requestedBy": {"type": "Relationship", "object": "urn:ngsi-ld:Person:bob-the-manager"},
      "installedBy": {"type": "Relationship", "object": "urn:ngsi-ld:Person:employee001"},
      "statusOfWork": {"type": "Property", "value": "completed"}
    },
    "@context": "http://context/tutorials-context.jsonld"
}

shelf13 = {
    "id": "urn:ngsi-ld:Shelf:unit013",
    "type": "Shelf",
    "location": {
      "type": "GeoProperty",
      "value": {"type": "Point", "coordinates": [-8.376475, 43.335578]}
    },
    "maxCapacity": {"type": "Property", "value": 50},
    "numberOfItems": {"type": "Property", "value": 15},
    "name": {"type": "Property", "value": "Corner Unit"},
    "stocks": {
      "type": "Relationship", "object": "urn:ngsi-ld:Product:012"
    },
    "locatedIn" : {
      "type": "Relationship", "object": "urn:ngsi-ld:Building:store005",
      "requestedBy": {"type": "Relationship", "object": "urn:ngsi-ld:Person:bob-the-manager"},
      "installedBy": {"type": "Relationship", "object": "urn:ngsi-ld:Person:employee001"},
      "statusOfWork": {"type": "Property", "value": "completed"}
    },
    "@context": "http://context/tutorials-context.jsonld"
}

shelf14 = {
    "id": "urn:ngsi-ld:Shelf:unit014",
    "type": "Shelf",
    "location": {
      "type": "GeoProperty",
      "value": {"type": "Point", "coordinates": [-8.376475, 43.335578]}
    },
    "maxCapacity": {"type": "Property", "value": 50},
    "numberOfItems": {"type": "Property", "value": 15},
    "name": {"type": "Property", "value": "Corner Unit"},
    "stocks": {
      "type": "Relationship", "object": "urn:ngsi-ld:Product:007"
    },
    "locatedIn" : {
      "type": "Relationship", "object": "urn:ngsi-ld:Building:store006",
      "requestedBy": {"type": "Relationship", "object": "urn:ngsi-ld:Person:bob-the-manager"},
      "installedBy": {"type": "Relationship", "object": "urn:ngsi-ld:Person:employee001"},
      "statusOfWork": {"type": "Property", "value": "completed"}
    },
    "@context": "http://context/tutorials-context.jsonld"
}


shelf15 = {
    "id": "urn:ngsi-ld:Shelf:unit015",
    "type": "Shelf",
    "location": {
      "type": "GeoProperty",
      "value": {"type": "Point", "coordinates": [-8.376475, 43.335578]}
    },
    "maxCapacity": {"type": "Property", "value": 50},
    "numberOfItems": {"type": "Property", "value": 15},
    "name": {"type": "Property", "value": "Corner Unit"},
    "stocks": {
      "type": "Relationship", "object": "urn:ngsi-ld:Product:005"
    },
    "locatedIn" : {
      "type": "Relationship", "object": "urn:ngsi-ld:Building:store006",
      "requestedBy": {"type": "Relationship", "object": "urn:ngsi-ld:Person:bob-the-manager"},
      "installedBy": {"type": "Relationship", "object": "urn:ngsi-ld:Person:employee001"},
      "statusOfWork": {"type": "Property", "value": "completed"}
    },
    "@context": "http://context/tutorials-context.jsonld"
}


shelf16 = {
    "id": "urn:ngsi-ld:Shelf:unit016",
    "type": "Shelf",
    "location": {
      "type": "GeoProperty",
      "value": {"type": "Point", "coordinates": [-8.376475, 43.335578]}
    },
    "maxCapacity": {"type": "Property", "value": 50},
    "numberOfItems": {"type": "Property", "value": 15},
    "name": {"type": "Property", "value": "Corner Unit"},
    "stocks": {
      "type": "Relationship", "object": "urn:ngsi-ld:Product:006"
    },
    "locatedIn" : {
      "type": "Relationship", "object": "urn:ngsi-ld:Building:store006",
      "requestedBy": {"type": "Relationship", "object": "urn:ngsi-ld:Person:bob-the-manager"},
      "installedBy": {"type": "Relationship", "object": "urn:ngsi-ld:Person:employee001"},
      "statusOfWork": {"type": "Property", "value": "completed"}
    },
    "@context": "http://context/tutorials-context.jsonld"
}


# SE HA HECHO UNA ÚNICA PETICIÓN PARA CREAR TODAS LAS SHELFS EN LUGAR DE UNA POR SHELF
payload = [
    shelf11,
    shelf12,
    shelf13,
    shelf14,
    shelf15,
    shelf16
]
code = ngsi_ld.batch_create(payload,headers=headers)


# AÑADIDOS 3 NUEVOS PRODUCTOS

product10 = {
    "id": "urn:ngsi-ld:Product:010",
    "type": "Product",
    "price": {"type": "Property", "value": 0.99, 
      "currency": {"type": "Property", "value": "EUR"}},
    "size": {"type": "Property", "value": "S"},
    "name": {"type": "Property", "value": "Apple"},
    "@context": "http://context/tutorials-context.jsonld"
}

product11 = {
    "id": "urn:ngsi-ld:Product:011",
    "type": "Product",
    "price": {"type": "Property", "value": 0.99, 
      "currency": {"type": "Property", "value": "EUR"}},
    "size": {"type": "Property", "value": "S"},
    "name": {"type": "Property", "value": "Orange"},
    "@context": "http://context/tutorials-context.jsonld"
}

product12 = {
    "id": "urn:ngsi-ld:Product:012",
    "type": "Product",
    "price": {"type": "Property", "value": 0.99, 
      "currency": {"type": "Property", "value": "EUR"}},
    "size": {"type": "Property", "value": "S"},
    "name": {"type": "Property", "value": "Pineapple"},
    "@context": "http://context/tutorials-context.jsonld"
}


# SE HA HECHO UNA ÚNICA PETICIÓN PARA CREAR TODOS LOS PRODUCTS EN LUGAR DE UNA POR PRODUCT

payload = [
    product10,
    product11,
    product12
]
code = ngsi_ld.batch_create(payload,headers=headers)

# AÑADIDOS 3 STOCK ORDERS NUEVAS

stockorder4 = {
    "id": "urn:ngsi-ld:StockOrder:004",
    "type": "StockOrder",
    "requestedFor": {"type": "Relationship", "object": "urn:ngsi-ld:Building:store005"},
    "requestedBy": {"type": "Relationship", "object": "urn:ngsi-ld:Person:bob-the-manager"},
    "orderedProduct": {"type": "Relationship", "object": "urn:ngsi-ld:Product:010"},
    "stockCount": {"type": "Property", "value": 10000},
    "orderDate": {
      "type": "Property", 
      "value": { "@type": "DateTime", "@value": "2023-05-01T12:00:00Z"}
    },
    "@context": "http://context/tutorials-context.jsonld"
}

stockorder5 = {
    "id": "urn:ngsi-ld:StockOrder:005",
    "type": "StockOrder",
    "requestedFor": {"type": "Relationship", "object": "urn:ngsi-ld:Building:store005"},
    "requestedBy": {"type": "Relationship", "object": "urn:ngsi-ld:Person:bob-the-manager"},
    "orderedProduct": {"type": "Relationship", "object": "urn:ngsi-ld:Product:011"},
    "stockCount": {"type": "Property", "value": 10000},
    "orderDate": {
      "type": "Property", 
      "value": { "@type": "DateTime", "@value": "2023-05-01T12:00:00Z"}
    },
    "@context": "http://context/tutorials-context.jsonld"
}

stockorder6 = {
    "id": "urn:ngsi-ld:StockOrder:006",
    "type": "StockOrder",
    "requestedFor": {"type": "Relationship", "object": "urn:ngsi-ld:Building:store005"},
    "requestedBy": {"type": "Relationship", "object": "urn:ngsi-ld:Person:bob-the-manager"},
    "orderedProduct": {"type": "Relationship", "object": "urn:ngsi-ld:Product:012"},
    "stockCount": {"type": "Property", "value": 10000},
    "orderDate": {
      "type": "Property", 
      "value": { "@type": "DateTime", "@value": "2023-05-01T12:00:00Z"}
    },
    "@context": "http://context/tutorials-context.jsonld"
}

# SE HA HECHO UNA ÚNICA PETICIÓN PARA CREAR TODAS LAS STOCK ORDERS EN LUGAR DE UNA POR STOCK ORDER

payload = [
    stockorder4,
    stockorder5,
    stockorder6
]

code = ngsi_ld.batch_create(payload,headers=headers)

# AÑADIDAS DOS PERSONAS

person1 = {
    "id": "urn:ngsi-ld:Person:employee001",
    "type": "Person",
    "name": {"type": "Property", "value": "Luis"},
    "@context": "http://context/tutorials-context.jsonld"
}

person2 = {
    "id": "urn:ngsi-ld:Person:bob-the-manager",
    "type": "Person",
    "name": {"type": "Property", "value": "Bob"},
    "@context": "http://context/tutorials-context.jsonld"
}

# SE HA HECHO UNA ÚNICA PETICIÓN PARA CREAR TODAS LAS PERSON EN LUGAR DE UNA POR PERSON

payload = [
    person1,
    person2
]

code = ngsi_ld.batch_create(payload,headers=headers)
print("Sample Data Created!")