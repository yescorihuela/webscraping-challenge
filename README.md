Instrucciones
---

1. Buscar todos los libros (recorrer la paginación) de este link: http://books.toscrape.com/
2. De cada libro se debe obtener la siguiente información:
    * Title
    * Price
    * Stock
    * Category (Travel, Mystery, Historical Fiction, etc)
    * Cover (url de la carátula del libro)
    * Product Description
        * UPC
        * Product Type
        * Price (excl. tax)
        * Price (incl. tax)
        * Tax
        * Availability
        * Number of reviews
3. Se recomienda usar las librerías [Requests](http://docs.python-requests.org/en/master/) y [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
4. Los resultados se deben exportar en un archivo CSV con las siguientes cabeceras:
    * Title
    * Price
    * Stock
    * Category
    * Cover
    * UPC
    * Product Type
    * Price (excl. tax)
    * Price (incl. tax)
    * Tax
    * Availability
    * Number of reviews
5. Se debe incluir un archivo requeriments.txt con las dependencias que requiera el script.
6. Se debe entregar un pull-request con la solución y una breve descripción/explicación.

En qué nos fijaremos
---
* Correcto uso de GIT
* Patrones de diseño
* Orden del código
