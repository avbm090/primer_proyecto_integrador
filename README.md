# 🛒 Sistema simple de gestión de ventas 

**Proyecto Integrador**  
Fecha: Junio 2025


## 📌 Descripción

Este proyecto es un sistema básico de gestión de ventas desarrollado en Python. Aplica principios de Programación Orientada a Objetos (POO), patrones de diseño (Factory, Singleton, Strategy), acceso a bases de datos relacionales con SQLAlchemy, con creación de triggers y procedures, y queries con CTE's, funciones de agregación y funciones ventana.

**Características principales:**

- Carga masiva de datos desde archivos JSON.  
- Registro de ventas y actualización automática de stock.  
- Generación de informes con distintas estrategias.  
- Conexión segura y única a MySQL usando variables de entorno.  
- Pruebas automatizadas con `pytest`.  


## 📁 Estructura del Proyecto



-  cache/ #archivos temporales de caché
-  data/ # datos de entrada
-  informes_resultado/ # resultados generados de los informes como json
- logs/ # archivos de registro (logs)
-  sql/ # patron strategy para el tipo de consulta
-  src/ # código fuente principal del sistema
-  tests/ # Pruebas unitarias con pytest
-  venv/ # entorno virtual
-  .env # variables de entorno
-  .gitignore # archivos y carpetas a ignorar por Git
-  main.py # archivo donde se inicializa el menú por consola
-  queries.ipynb # notebook de queries con cte's
-  README.md 
-  requirements.txt # dependencias

## :eyeglasses: Detelles:

- `cache.py:`
    Posee una función de caché básica (con decorador @lru_cache) para cuando se selecciona la opción de visualizar todas las ventas hechas. Como sólo hay 600 registros aproximadamente el tamaño de la ventana es de 1, es decir guarda todos los datos de las ventas en memoria.
- `data:`
  - Crear Tablas: En el archivo crear_tablas.py, se establece la conexión mediante el patrón Singleton. Luego, se importan los modelos ORM generados a partir de los archivos CSV, y se realiza el mapeo entre las clases de Python y las tablas en la base de datos, las cuales se crean automáticamente.
  - data_sin_procesar: Contiene los archivos Excel originales proporcionados, que se utilizan para realizar el mapeo hacia la base de datos.
  - primera_carga_masiva_de:datos: Utiliza la conexión singleton, utiliza loggin y el path de los csv guardados como variable de entorno. Los nombres de las tablas se guardan como un diccionario donde las claves son las tablas y los valores son las columnas de ids, esto es porque: ##Importante:## No se sobreescribieron los id's existentes, dado que esto podría generar un problema de consistencia en los registros de las ventas. Más bien, se tomaron los id's existentes de cada tabla y se corrobora si éstos efectivamente están en cada una, a modo de control. Después, se pasan los archivos a dataframe (es es sólamente en caso de que más adelante se necesite realizar alguna limpieza de datos o lo que fuere necesario para trabajar como paso intermedio) y se pasan a tipo sql. Después se busca el valor del último ID  se ajustan las tablas para que lo tomen, a fin de que, cuando se realicen nuevos inserts, sea a partir de estos valores buscados y no se comprometa la integridad de los datos. Este archio se ejecuta por única vez.

- `informes_resultado:` Contiene los archivos JSON generados de los distintos informes solicitados desde consola. Estos archivos se generan desde el método "ejectuar" de la clase "Informe" que heredan las clases que representan cada tipo de informe. Todo esto está organizado con patrón fatcory en el archivo factory.py de la carpeta "informes".
- `sql:` Contiene el archivo "consultas_sql" con las clases diseñadas utilizando patrón strategy (una clase de consultas select, otra para tipo call y otra para identificar el tipo de consultas que no se pueden realizar,  como update por ejemplo) para una mejor organización. La clase padre llamada "ConsultaStrategy" es la clase abstracta, y sus clases derivadas o hijas "ConsultaSelect", "ConsultaCallProcedure" y "ConsultaDefault" que heredan el método "ejecutar" por polimorfismo. Para determinar la estrategia se utiliza la función "elegir_strategy" que corre dentro de la función "ejecutar_consulta" que se ejecuta en el main.
- `src:` Contiene la estructura principal del programa:
    - #conexion:# El archivo conexion_singleton.py contiene la lógica de la conexión a la base de datos. Se almacena una única instancia permitida, a través de una variable privada, llamada __instance que la almacena. El método __new__ detecta si __instance es o no None (como cls._instance), en caso de que así sea, crea una nueva conexión seteando a cls._instance como super().__new__(cls) y se organiza la conexión a la base de datos. 

## ⚙️ Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/tu_usuario/nombre_proyecto.git
cd nombre_proyecto
Crea y activa un entorno virtual:

bash
Copiar
Editar
python -m venv venv
source venv/bin/activate      # En Windows: venv\Scripts\activate
Instala las dependencias:

bash
Copiar
Editar
pip install -r requirements.txt
Configura las variables de entorno:

Crea un archivo .env con el siguiente contenido:

ini
Copiar
Editar
DB_HOST=localhost
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_NAME=nombre_de_tu_base
▶️ Ejecución
Ejecuta el programa principal:

bash
Copiar
Editar
python main.py
Desde aquí podrás registrar ventas, cargar datos y generar informes.
