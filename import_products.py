import json
import mysql.connector

# Veritabanına bağlantı kurma
config = {
    'user': 'kullanici',
    'password': 'şifre', #kullanıcı şifresi girilmeli
    'host': 'localhost',
    'database': 'sys'
}

# MySQL sunucusuna bağlanın
try:
    connection = mysql.connector.connect(**config)
    print("Bağlantı başarılı!")

    # JSON dosyasını okuma
    with open('petlebi_products.json', 'r') as file:
        data = json.load(file)

    # Verileri MySQL veritabanına aktarma
    for product in data:
        product_URL = product['product_URL']
        product_name = product['product_name']
        barcode = product['barcode']
        price = product['price']
        #product_stock = product['product_stock']
        #product_images = prodcut['product_images']
        description = product['description']
        #sku = product['sku']
        category = product['category']
        #product_ID = product['product_ID'] mysql'e atarken kendisi atıyor
        brand = product['brand']

        cursor = connection.cursor()

        # Verileri tabloya ekleme
        # %s lerin sayısı ve başlıklar kontrol edilmeli
        sql = "INSERT INTO petlebi (product_URL, product_name, barcode, price, description, category, brand) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (product_URL, product_name, barcode, price, description, category, brand)

        cursor.execute(sql, values)
        connection.commit()

    print(cursor.rowcount, "rows inserted.")

    # Bağlantıyı kapatma
    connection.close()
except mysql.connector.Error as error:
    print("Bağlantı hatası:", error)
