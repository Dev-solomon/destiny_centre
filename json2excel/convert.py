from json2excel import Json2Excel
import requests 

def extract_last_value(input_str):
    # Split the string by ' -- ' and take the last part
    parts = input_str.split(' -- ') 
    if parts:
        last_value = parts[-1]
        return last_value
    return input_str

def get_product_weight(input_str):
    # Split the string by ' -- ' and take the last part
    parts = input_str.split('-') 
    if parts:
        last_value = parts[-1]
        return last_value
    return input_str

def get_shipping_codes(shipping_country_codes:list):
    string_result = ','.join(shipping_country_codes)
    # print(string_result)  # Output: US
    return string_result



def get_products_in_usa():
    try:
        headers = {'CJ-Access-Token': "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIxNzA4NiIsInR5cGUiOiJBQ0NFU1NfVE9LRU4iLCJzdWIiOiJicUxvYnFRMGxtTm55UXB4UFdMWnlyK2FrM2QxTU9HTURrWlU4RHF2bU5vWGtFZWlyenRIc29Na3pkamVSQUwzN1pQUEJ6Y1RYWFhEZzNyOHdqYWxvL1MvalNJZGJ5UHBmbEwwbCs5YVlwSnU4VTU4Tkw4dXRCaEZSd25iM1pqRmJLM2l5QkxaamoxeGg1Zkh1MmNNbDdKdEwxMkVjYkNRdnM3cnJsWWhueDIxdWMvMUpPV2pPK0V3ZHk5Tm1QRGF3M0VWMHJ6ZUJhVnpNY2lTWnYySTE0L2JOd2lnMTFXVi9DaVdGVllkWUQ3Q0lXZi8xQjVDRVI2UGh2MnZ6UDR5R3lpRjFXS28yZWpNOUpCRVBEODZsa1ZvaTN6OC91M3M1Y1pjOXZjY0MxMD0ifQ.JRu2WSDd9GiHql3savT4bBOFY2RhfoBkG9uEumaLCTk"}
        params = {
            'pageNum': 4,
            'pageSize': 100,
            'categoryId': '2837816E-2FEA-4455-845C-6F40C6D70D1E',
            # category based on which ?
            # all women clothing => 2FE8A083-5E7B-4179-896D-561EA116F730
            # all men clothing => B8302697-CF47-4211-9BD0-DFE8995AEB30
            # all bags and shoes => 2415A90C-5D7B-4CC7-BA8C-C0949F9FF5D8
            # all toys, kids and babies => A50A92FA-BCB3-4716-9BD9-BEC629BEE735
            # all jewelry and watches => 2837816E-2FEA-4455-845C-6F40C6D70D1E
            # 'minPrice': 1.0,
            'countryCode': 'US',
            'productType': 'ORDINARY_PRODUCT'
        }
        response = requests.get(
            'https://developers.cjdropshipping.com/api2.0/v1/product/list',
            headers=headers,
            params=params
        )
        
        data = response.json()["data"]
        
        json2excel = Json2Excel()
         # print(json2excel.run('./test.json'))
        
        productsList = []
        for product in data['list']:
            productsList.append({
                'id': product['pid'],
                # 'cat_id': product['categoryId'],
                'name': product['productNameEn'],
                'category': product['categoryName'],
                'cost': float(extract_last_value(product['sellPrice'])),
                'price': (float(extract_last_value(product['sellPrice'])) * 3) + 1,
                'productType': 'Goods' if product['productType'] == 'ORDINARY_PRODUCT' else 'Services',
                'images': product['productImage'],
                'stock': float(product['listedNum']),
                'productWeight': float(get_product_weight(product['productWeight'])),
                # 'shippingCountry': 1 if get_shipping_codes(product['shippingCountryCodes']) == 'US' else 2
            })
            
        print(f"Total:: {data['total']}")
        print(f"productList Length:: {len(productsList)}")
        print(json2excel.run(productsList))
        
    except requests.exceptions.RequestException as e:
        print("something went wrong")
        
get_products_in_usa()



    
    

    
   


    