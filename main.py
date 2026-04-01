import requests
import pandas as pd
import sqlite3

# API'den veri çek
url = "https://dummyjson.com/products"
response = requests.get(url)
data = response.json()

# API verisi
df_api = pd.DataFrame(data["products"])

# Sadece ihtiyacımız olan kolonları al
df_api = df_api[["id", "title", "price", "category"]]

# CSV verisi
df_stock = pd.read_csv("data/products.csv")
df_stock.columns = df_stock.columns.str.strip()

# Birleştir
df = df_api.merge(df_stock, on="id", how="left")

# Eksik stokları 0 yap
df["stock"] = df["stock"].fillna(0).astype(int)

# SQLite bağlantısı
conn = sqlite3.connect("db/products.db")

# DataFrame'i SQL tablosuna yaz
df.to_sql("products", conn, if_exists="replace", index=False)

print("Veriler veritabanına kaydedildi.")

# SQL sorgusu 1: ilk 5 ürün
query1 = "SELECT * FROM products LIMIT 5"
result1 = pd.read_sql(query1, conn)

print("\nİlk 5 ürün:")
print(result1)

# SQL sorgusu 2: stoku 0 olan ürünler
query2 = "SELECT id, title, stock FROM products WHERE stock = 0"
result2 = pd.read_sql(query2, conn)

print("\nStoku 0 olan ürünler:")
print(result2)

conn.close()

# Excel'e aktar
df.to_excel("stok_raporu.xlsx", index=False)

print("\nExcel dosyası oluşturuldu: stok_raporu.xlsx")