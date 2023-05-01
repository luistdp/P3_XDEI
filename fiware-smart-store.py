from flask import Flask, render_template, redirect,url_for,request
import ast
import math
import ngsi_ld

app = Flask(__name__)

"""
Información de como pasar datos de formularios de html a flask encontrado aquí:
QUERY: similar a: "send editable values from table to flask"
 - https://copyprogramming.com/howto/5-methods-for-passing-values-from-html-to-python-flask
"""

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/Buildings")
def buildings():
    headers = ngsi_ld.set_headers(context_link=ngsi_ld.LINK,
                                  content_type=None)
    code,buildings = ngsi_ld.list_entities(type="Building", 
                                        headers=headers)
    if code == 200: 
        return render_template("buildings.html",
                           buildings = buildings)
    else: 
        return render_template("error.html", code = code)
    
@app.route("/Products")
def products():
    headers = ngsi_ld.set_headers(context_link=ngsi_ld.LINK,
                                  content_type=None)
    code, products = ngsi_ld.list_entities(type="Product", 
                                        headers=headers)
    data = list()
    for product in products:
        product_id = product["id"]
        # Recuperamos información necesaria para construir valores total_stock y capacity
        code, shelfs = ngsi_ld.list_entities(type="Shelf",options="keyValues",
                                             q=f'stocks=="{product_id}"',headers=headers)
        total_stock, total_capacity = 0,0
        for shelf in shelfs: 
            if "maxCapacity" in shelf:
                total_capacity += shelf["maxCapacity"]
            if "numberOfItems" in shelf:
                total_stock += shelf["numberOfItems"]
        data.append((total_stock,total_capacity))
    data = [(product,more_data) for product,more_data in zip(products,data)]
    if code == 200: 
        return render_template("products.html",
                               data = data)
    else: 
        return render_template("error.html", code = code)

@app.route('/Buildings/update_building/<building_id>', methods = ["GET","POST"])
def update_building(building_id):
    headers = ngsi_ld.set_headers(context_link=ngsi_ld.LINK,
                                  content_type=None)
    building_id = "urn:ngsi-ld:Building:" + building_id
    code, entity = ngsi_ld.read_entity(building_id,
                                       headers=headers)
    del entity["id"]
    del entity["furniture"]
    entity["name"] = request.form.get("name", type=str)
    entity["address"]["value"]["addressLocality"] = request.form.get("addressLocality", type=str)
    entity["address"]["value"]["addressRegion"] = request.form.get("addressRegion", type=str)
    entity["address"]["value"]["streetAddress"] = request.form.get("streetAddress", type=str)
    entity["location"]["value"]["coordinates"] = ast.literal_eval(request.form.get("coordinate", type=str))
    entity["category"] = request.form.get("category", type = str)
    headers = ngsi_ld.set_headers(context_link=ngsi_ld.LINK, content_type="application/json")
    code = ngsi_ld.update_attr(building_id, attr_vals=entity, headers=headers)
    if code == 207:
        print("Building succesfully updated!")
    return redirect(url_for("buildings")) 

@app.route('/Buildings/delete_building/<building_id>', methods = ["POST"])
def delete_building(building_id):
    headers = ngsi_ld.set_headers(context_link=ngsi_ld.LINK, content_type=None)
    building_id = "urn:ngsi-ld:Building:" + building_id
    code = ngsi_ld.delete_entity(building_id,
                                 headers=headers)
    if code == 204: 
        headers = ngsi_ld.set_headers(context_link=ngsi_ld.LINK,content_type=None)
        code, stockorders = ngsi_ld.list_entities(type="StockOrder",options="keyValues",
                                                  q=f'requestedFor=="{building_id}"',
                                                  headers=headers)
        code, shelfs = ngsi_ld.list_entities(type="Shelf",options="keyValues",
                                             q=f'locatedIn=="{building_id}"', headers=headers)
        stock_order_ids = [stockorder["id"] for stockorder in stockorders]
        headers = ngsi_ld.set_headers(content_type="application/json")
        #Se eliminan todas las stock orders relacionadas al building que ha sido eliminado
        #esto se hace en batch, en lugar de hacer una petición por cada stockorder a borrar
        code = ngsi_ld.batch_delete(entity_id_list=stock_order_ids,headers=headers)
        shelf_ids = [shelf["id"] for shelf in shelfs]
        #Misma idea que con las stock orders, en lugar de hacer el borrado de las shelfs,
        #una por una se hace en batch
        code = ngsi_ld.batch_delete(entity_id_list=shelf_ids, headers=headers)
    return redirect(url_for("buildings"))

@app.route('/Products/update_product/<product_id>', methods = ["GET", "POST"])
def update_product(product_id):
    headers = ngsi_ld.set_headers(context_link=ngsi_ld.LINK, content_type=None)
    product_id = "urn:ngsi-ld:Product:" + product_id
    code, entity = ngsi_ld.read_entity(product_id, headers=headers)
    del entity["id"]
    entity["name"] = request.form.get("name",type=str)
    entity["price"] = request.form.get("price",type=float)
    entity["size"] = request.form.get("size",type=str)
    headers = ngsi_ld.set_headers(context_link=ngsi_ld.LINK,
                                  content_type="application/json")
    code = ngsi_ld.update_attr(product_id,attr_vals=entity,headers=headers)
    if code == 207:
        print("Product succesfully updated!")
    return redirect(url_for("products"))

@app.route('/Products/delete_product/<product_id>')
def delete_product(product_id):
    headers = ngsi_ld.set_headers(context_link=ngsi_ld.LINK, content_type=None)
    product_id = "urn:ngsi-ld:Product:" + product_id
    code = ngsi_ld.delete_entity(product_id,
                                 headers=headers)
    if code == 204:
        headers = ngsi_ld.set_headers(context_link=ngsi_ld.LINK,content_type=None)
        code, stockorders = ngsi_ld.list_entities(type="StockOrder", options="keyValues",
                                                  q = f'orderedProduct=="{product_id}"',
                                                  headers=headers)
        code, shelfs = ngsi_ld.list_entities(type="Shelf", options="keyValues",
                                             q=f'stocks=="{product_id}"',headers=headers)
        stock_order_ids = [stockorder["id"] for stockorder in stockorders]
        if len(stock_order_ids) > 0:
            # Borrado de las stock orders relacionadas con el product eliminado. En  batch
            # en lugar de hacerlo por cada stock order
            headers = ngsi_ld.set_headers(content_type="application/json")
            code = ngsi_ld.batch_delete(entity_id_list=stock_order_ids,headers=headers)
        if len(shelfs) > 0:
            for shelf in shelfs: 
                shelf["numberOfItems"] = 0
                shelf["stocks"] = ":".join(product_id.split(":")[0:3]) + ":null"
            # Para cada una de las shelfs que tenían ese producto es neceario modificar 
            # el campo que tenía la relación con ese product y poner Product:null pero 
            # esto no se hace de forma que se tenga que hacer una petición por cada shelf
            # se hace en batch con ngsi_ld.batch_update
            headers = ngsi_ld.set_headers(context_link=ngsi_ld.LINK, content_type="application/json")
            code = ngsi_ld.batch_update(entity_attr_list=shelfs,headers=headers)
    return redirect(url_for("products"))

def map_tile_url(zoom, location):
    print(location)
    tiles_per_row = math.pow(2,zoom)
    longitude = location[0]
    latitude = location[1]
    longitude /= 360
    longitude += 0.5
    latitude =  0.5 - math.log(math.tan(math.pi / 4 + (latitude * math.pi) / 360)) / math.pi / 2.0
    return f"https://a.tile.openstreetmap.org/{zoom}/{math.floor(longitude * tiles_per_row)}/{math.floor(latitude * tiles_per_row)}.png"

@app.route('/Building/<building_id>')
def building(building_id):
    headers = ngsi_ld.set_headers(context_link=ngsi_ld.LINK,
                                  content_type=None)
    building_id = "urn:ngsi-ld:Building:" + building_id
    code, building = ngsi_ld.read_entity(building_id,
                                       headers=headers)
    mapurl = map_tile_url(15,building["location"]["value"]["coordinates"])
    building["mapurl"] = mapurl
    shelf_data = list()
    product_data = list()
    # Este apartado se ha hecho de forma que un building pueda tener varios shelfs
    # y que cada shelf tenga un único product. No se puede que un shelf tenga más,
    # de un product
    if "furniture" in building:
        if isinstance(building["furniture"],list):
            for s in building["furniture"]:
                shelf_d = dict()
                code, shelf = ngsi_ld.read_entity(s["object"],headers=headers)
                if "stocks" in shelf:
                    if "object" in shelf["stocks"]:
                        product_id = shelf["stocks"]["object"]
                    elif "value" in shelf["stocks"]:
                        product_id = shelf["stocks"]["value"]

                code,prod = ngsi_ld.read_entity(product_id,headers=headers)
                if "id" in prod:
                    product_data.append(prod)
                    shelf_d["id"] = shelf["id"]
                    shelf_d["name"] = shelf["name"]["value"]
                    shelf_d["maxcapacity"] = shelf["maxCapacity"]["value"]
                    shelf_d["numberofitems"] = shelf["numberOfItems"]["value"]
                    shelf_data.append(shelf_d)
                else: 
                    continue
        else: 
            shelf_d = dict()
            code,shelf = ngsi_ld.read_entity(building["furniture"]["object"],headers=headers)
            if "stocks" in shelf:    
                if "object" in shelf["stocks"]:
                    product_id = shelf["stocks"]["object"]
                elif "value" in shelf["stocks"]:
                    product_id = shelf["stocks"]["value"]          
            code,prod = ngsi_ld.read_entity(product_id,headers=headers)
            if "id" in prod:
                product_data.append(prod)
                shelf_d["id"] = shelf["id"]
                shelf_d["name"] = shelf["name"]["value"]
                shelf_d["maxcapacity"] = shelf["maxCapacity"]["value"]
                shelf_d["numberofitems"] = shelf["numberOfItems"]["value"]
                shelf_data.append(shelf_d)
        data = [(prod,shelf) for prod,shelf in zip(product_data,shelf_data)]
    return render_template("building.html",
                           building = building,
                           data = data)

@app.route('/Product/<product_id>')
def product(product_id):
    headers = ngsi_ld.set_headers(context_link=ngsi_ld.LINK,content_type=None)
    product_id = "urn:ngsi-ld:Product:" + product_id
    code, product = ngsi_ld.read_entity(product_id,headers=headers)
    # Se hacen las peticiones correspondientes a las shelfs y stock orders en las que está 
    # incluido este product.
    code, shelfs = ngsi_ld.list_entities(type="Shelf",options="keyValues",
                                         q=f'stocks=="{product_id}"',headers=headers)
    code, stockorders = ngsi_ld.list_entities(type="StockOrder",options="keyValues",
                                              q=f'orderedProduct=="{product_id}"',headers=headers)
    for shelf in shelfs: 
        code, shelf_building = ngsi_ld.read_entity(shelf["locatedIn"],headers=headers)
        code, shelf_person = ngsi_ld.read_entity(shelf["id"],headers=headers)
        shelf["installedBy"] = shelf_person["locatedIn"]["installedBy"]["object"]
        code, person_name = ngsi_ld.read_entity(shelf["installedBy"],headers=headers)
        shelf["building"] = shelf_building["name"]["value"]
        shelf["person"] = person_name["name"]["value"]
    for stockorder in stockorders:
        code, stock_building = ngsi_ld.read_entity(stockorder["requestedFor"],headers=headers)
        code, stock_person = ngsi_ld.read_entity(stockorder["requestedBy"],headers=headers)
        stockorder["orderDate"] = stockorder["orderDate"]["@value"]
        stockorder["building"] = stock_building["name"]["value"]
        stockorder["person"] = stock_person["name"]["value"]
    return render_template("product.html",
                           product = product, shelfs = shelfs, stockorders = stockorders)

@app.route('/Product/<product_id>/buy_product', methods = ["GET", "POST"])
def buy_product_page(product_id):
    headers = ngsi_ld.set_headers(context_link=ngsi_ld.LINK,
                                  content_type=None)
    shelf_id = "urn:ngsi-ld:Shelf:" + request.form.get("shelf_id")
    code, shelf = ngsi_ld.read_entity(shelf_id,headers=headers)
    if shelf["numberOfItems"]["value"] == 0:
        return redirect(url_for("product",product_id=product_id))
    payload = {
        "numberOfItems":{
            "type":"Property",
            "value": shelf["numberOfItems"]["value"] - 1
        }
    }
    headers = ngsi_ld.set_headers(context_link=ngsi_ld.LINK,content_type="application/json")
    code = ngsi_ld.update_attr(shelf_id,payload,headers=headers)
    return redirect(url_for("product",product_id=product_id))


@app.route('/Building/<building_id>/buy_product/<product_id>', methods = ["GET", "POST"])
def buy_product(building_id,product_id):
    headers = ngsi_ld.set_headers(context_link=ngsi_ld.LINK,
                                  content_type=None)
    shelf_id = "urn:ngsi-ld:Shelf:" + request.form.get("shelf_id")
    code, shelf = ngsi_ld.read_entity(shelf_id,headers=headers)
    if shelf["numberOfItems"]["value"] == 0:
        return redirect(url_for("building",building_id=building_id))
    payload = {
        "numberOfItems":{
            "type":"Property",
            "value": shelf["numberOfItems"]["value"] - 1
        }
    }
    headers = ngsi_ld.set_headers(context_link=ngsi_ld.LINK,content_type="application/json")
    code = ngsi_ld.update_attr(shelf_id,payload,headers=headers)
    return redirect(url_for("building",building_id = building_id))