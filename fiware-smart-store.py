from flask import Flask, render_template, redirect,url_for,request
import ast
import ngsi_ld

app = Flask(__name__)
"""
Valores a null: Tenemos que poner null en el caso de por ejemplo una shelf el atributo stocks 
Esto realmente es de tipo Relationship y apunta a un objeto de tipo product. Cuando haga un update 
para poner el valor del atributo objet a null le tengo que decir de que tipo es el null Product:null

Otra cosa en Step by Step NGSI-LD: Normalized Operations y Consise Crud operations y las peticiones postman que hay ahi. 
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
        print(product_id)
        code, shelfs = ngsi_ld.list_entities(type="Shelf",options="keyValues",
                                             q=f'stocks=="{product_id}"',headers=headers)
        print(code)
        total_stock, total_capacity = 0,0
        for shelf in shelfs: 
            print(shelf)
            print(shelfs)
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
    print(building_id[3])
    print(building_id)
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
        print(stock_order_ids)
        headers = ngsi_ld.set_headers(content_type="application/json")
        code = ngsi_ld.batch_delete(entity_id_list=stock_order_ids,headers=headers)
        shelf_ids = [shelf["id"] for shelf in shelfs]
        print(shelf_ids)
        code = ngsi_ld.batch_delete(entity_id_list=shelf_ids, headers=headers)
        print(code)
    return redirect(url_for("buildings"))

@app.route('/Products/update_product/<product_id>')
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
        print("Product succesfully updated")
    return redirect(url_for("products"))




@app.route('/Products/delete_product')
def delete_product():
    pass 

"""
@app.route('/Building/<store_id>')
def display_store(store_id):
    (status, data) = ngsiv2.read_entity(store_id)
    if status == 200:
        return render_template('store.html', store = data) +\
        list_inventory_items_for_store(store_id)
    else:
        return render_template('error.html',
        error = f"Error reading product {store_id}.\
                Orion response: {data}") 

@app.route("/Products")
def products():
    _, products = ngsiv2.list_entities(type="Product")
    return render_template("products.html",
                           products = products,
                           product_base_url = '/Product/')

@app.route('/Product/<product_id>')
def display_product(product_id):
    (status, data) = ngsiv2.read_entity(product_id)
    if status == 200:
        return render_template('product.html', product = data) +\
        list_inventory_items_for_product(product_id)
    else:
        return render_template('error.html',
        error = f"Error reading product {product_id}.\
                Orion response: {data}") 
"""