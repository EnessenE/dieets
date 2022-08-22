from supermarktconnector.jumbo import JumboConnector
import json

connector = JumboConnector()
data = connector.get_product_by_barcode(8712800535621)
productJson = connector.get_product_details(data)
print(productJson)

product = productJson["product"]["data"]

notAllowedList = ['sucralose']

print("name: "+product["title"])
print("id: "+product["id"])
print("ingredienten: "+json.dumps(product["ingredientInfo"]))

itemPassed = True
for ing in product["ingredientInfo"][0]["ingredients"]:
    ing_name = ing["name"].lower()
    #print("checking: "+ ing_name)
    for notAllowed in notAllowedList:
        if ing_name.__contains__(notAllowed.lower()):
            print(ing_name + " NOT ALLOWED!")
            itemPassed = False
        else:
            print(ing_name+" is fine")


print("HAS ITEM PASSED: "+str(itemPassed))