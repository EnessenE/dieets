import json
from math import prod
from urllib import request
from supermarktconnector.jumbo import JumboConnector
from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
app = Flask(__name__)
api = Api(app)


class DataProduct:
    name = ""
    ean = 1
    ingredients = [""]

def GetProductFromEan(ean: int) -> DataProduct:
    dataProduct = DataProduct()
    connector = JumboConnector()
    data = connector.get_product_by_barcode(ean)
    productJson = connector.get_product_details(data)
    print(productJson)

    product = productJson["product"]["data"]

    notAllowedList = ['sucralose']
    dataProduct.ean = ean;
    dataProduct.name = product["title"]
    print("name: "+product["title"])
    print("id: "+product["id"])
    print("ingredienten: "+json.dumps(product["ingredientInfo"]))

    itemPassed = True
    dataProduct.ingredients = []
    for ing in product["ingredientInfo"][0]["ingredients"]:
        ing_name = ing["name"].lower()
        dataProduct.ingredients.append(ing_name)
        #print("checking: "+ ing_name)
        for notAllowed in notAllowedList:
            if ing_name.__contains__(notAllowed.lower()):
                print(ing_name + " NOT ALLOWED!")
                itemPassed = False
            else:
                print(ing_name+" is fine")

    print("HAS ITEM PASSED: "+str(itemPassed))
    return product


class Products(Resource):
    def get(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('ean', type=int, required=True,help="ean cant be empty")
        args = parser.parse_args()  # parse arguments to dictionary
        
        dataProduct = GetProductFromEan(args['ean'])
        return {'product', dataProduct}, 200
    pass


api.add_resource(Products, '/products')



if __name__ == '__main__':
    app.run()
