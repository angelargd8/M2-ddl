# Web Scraping
# Autores: - Cesar Lopez #22535
#          - Francis Aguilar #22243
#          - Angela Garcia #22869

import re
import csv
from urllib.parse import urljoin


#abrir un archivo html de la pagina descargada
def cargar_html(nombre_archivo):
    with open(nombre_archivo, 'r', encoding='utf-8') as file:
        return file.read()

#implementar un buffer para procesar el contenido

#usar expresiones regulares para encontrar los nombres de productos y urls de imagenes
def extraer_productos(archivo_html, url_base):
    productos = []
    #re.dotall sirve para que el . en la re coincida con cualquier caracter y el finter sirve para devolver un iterador de las conincidencias
    for match in re.finditer(r'<li class="product.*?<a.*?<img.*?src="(.*?)"(?: alt=".*?")?.*?>.*?<h2 class="woocommerce-loop-product__title"\s*>(.*?)</h2>', archivo_html, re.DOTALL):
        imagen = match.group(1)
        nombre = match.group(2).strip()
        # print(nombre)
        # print(imagen)
        #caracteres de la ruta de imagen
        caracteres = './Trufas &amp; Bombones _ Zurich Guatemala_files/'
        imagen = imagen.replace(caracteres, "")
        #cambiar la url de la imagen para que apunte a la url base
        imagen = urljoin(url_base, imagen)
        # print(imagen)
        productos.append([nombre, imagen])

    return productos

# generar un archivo exportable, como un .csv con las columnas de "nombre del producto" y "url de la imagen"
# exportar los resultados
def exportar_csv(productos, archivo_salida):
    with open(archivo_salida, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Nombre del producto', 'Url de la imagen'])
        for producto in productos:
            writer.writerow(producto)

#cargar el archivo
nombre_archivo= 'Trufas & Bombones _ Zurich Guatemala.html'
archivo_html = cargar_html(nombre_archivo)

#extraer los productos y las urls de imagenes
url_base = "https://zurichgt.com/wp-content/uploads/2024/04/" #alli es donde estan las imagenes en la web
productos = extraer_productos(archivo_html, url_base)


#exportar los resultados en un csv
exportar_csv(productos, 'Trufas_bombones_Zurich_Guatemala.csv')