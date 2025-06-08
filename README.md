# 🛒 Sistema simple de gestión de ventas 

**Proyecto Integrador**  


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
- `informes_resultados:` contiene lso archivos jsons que se obtienen como resutlados de los informes.
- `src:` Contiene la estructura principal del programa:
    - **conexion:** El archivo conexion_singleton.py contiene la lógica de la conexión a la base de datos. Se almacena una única instancia permitida, a través de una variable privada, llamada __instance que la almacena. El método __new__ detecta si __instance es o no None (como cls._instance), en caso de que así sea, crea una nueva conexión seteando a cls._instance como super().__new__(cls) y se organiza la conexión a la base de datos.
    - **informes:** Esta carpeta contiene la lógica para generar los informes predeterminados.
        - procedures: Para realizar los informes se crearon los procedures llamados "informe_producto_ciudad_resumen", "informe_top_clientes", "informe_ventas_categoria" e "informe_ventas". Estas queries son simples, las más complejas se crearon en el archivo "queries.ipynb" en el directorio principal. 
        - triggers: contiene el trigger llamado "venta_insert", éste se activa cuando se carga una venta, los datos ingresados por el usuario se guardan en una tabla llamada "log_ventas" y posteriormente se puede acceder a estos datos a modo de adutoría.
        - factory.py: es la fábrica de los informes, contiene la clase abstracta llamada "Informe" con dos métodos: "guardar_json" y "ejecutar" (que usa "guardar_json". Las clases "InformeProductoCiudad", "InformeTopClientes", "InformeVentasCategoria", "InformeVentasHistorico", e "InformeVentas" heredan estos métodos y generan los archivos json. en la carpeta "informes_resultado".
        - **loggin:** contiene los archivos "loggin_config.py" que contiene la función "configurar_logging" donde se genera la configuración que toma el resto de los arhivos del programa, todos los logs se guardan en "loggin_config.log".
        - **modelos:** Contiene las clases que se mapean los archivos csv con las tablas de la base de datos mediante la libreria sqlalchemy. En el directrio data - crear_tablas - crear_tablas.py se llama a "Base" que es la base declarativa de los modelos, estos modelos son: Category, Country, City, Customer, Employee, Product, Sale. Cada uno está configurado para que tome la estructura de primary keys, foreign keys y las relaciones que corresponde.
        - **registros_insert:** contiene los archivos con clases que llaman a los procedimientos almacenados para realizar inserts. Es decir, se tienen los siguientes archivos:   insert_category.py, insert_cities.py, insert_countries.py, insert_customers.py, insert_employee.py, insert_product.py, insert_sales.py. Cada uno de estos contiene una clase con una lógica que permite al usuario ingresar los datos de ventas en cada tabla, y llama a un procedure específico dependiendo la tabla donde se estén insertando los datos (ver **procedures**). Un archivo "factory.py" que es la fábrica y maneja la lógica para realizar las inserciones.
            - **procedures:** contiene lso procedimientos mencionados en **registros_insert**. Estos son: "InsertCustomer()", "InsertEmployee()", "InsertProduct()", e "InsertSale()". Cada uno contiene el tipo de variable que se espera y una salida, dependiendo de si el dato ya estaba cargado en la tabla o no. Cabe aclarar que esto último no se controla en la tabal ventas, dado que se asume que todas las ventas insertadas son distintas.

- `tests:` contiene los tests unitarios.
- **test_caché.py:** este test corrobora si los datos se consultan pro primera vez al caché o a la base de datos. La primera vez consultará a la bbdd y la segunda llamada deberá ser consultada al caché.
- mock_session(): El fixture mock_session ( con decorador @pytest.fixture ) crea un mock de la sesión. En este caso, es una instancia de MagicMock() que simula el comportamiento de la sesión que se usaría en una base de datos en SQLAlchemy. Se configura para que mock_session.query.return_value.all.return_value devuelva una lista de tuplas que simulan registros de ventas.
- test_cache_ventas() (1): En este test, se utiliza un mock de la función get_session() de la clase ConexionSingleton, usando @patch.object(ConexionSingleton, 'get_session'). Esto reemplaza la función get_session() con un objeto simulado, mock_get_session. Este mock está configurado para devolver el objeto mock_session cuando se llama. El objeto mock_session proviene del fixture mock_session(), que simula el comportamiento de una sesión de base de datos. La función cache_ventas() utiliza este mock de la sesión, y se verifica que la consulta a la base de datos (simulada) devuelva los datos esperados, es decir, las dos ventas preconfiguradas. Además, se asegura que la consulta a la base de datos mockeada se haya realizado solo una vez, lo que implica que cache_ventas() solo consultó la base de datos una vez.
- test_cache_ventas() (2): test_cache_ventas() (2): Este test evalúa si la función cache_ventas() utiliza correctamente el caché después de realizar una consulta inicial a la base de datos. En la primera llamada a cache_ventas(), se espera que la función consulte a la base de datos simulada (a través de la sesión mockeada). En la segunda llamada, se espera que la función recupere los mismos datos, pero esta vez desde el caché, sin consultar nuevamente la base de datos.
Se verifica que los resultados de ambas llamadas sean iguales, lo que indica que el caché está funcionando correctamente. Además, se comprueba que la base de datos haya sido consultada solo una vez, lo que asegura que la segunda llamada a cache_ventas no realice una nueva consulta a la base de datos, sino que obtenga los datos desde el caché.
Al igual que en el primer test, se utiliza @patch.object para reemplazar el método get_session de ConexionSingleton y simular la sesión de base de datos. Los argumentos mock_get_session y mock_session permiten controlar el comportamiento de la sesión simulada para realizar las verificaciones necesarias en el test.
- **test_conexion.py:** Este test es el más simple de todos, solamente corrobora que, si se crean dos sesiones, estas utilizan el mismo engine.
- **test_crear_tablas.py:**
- test de creación OK:
      - Se usa @patch para reemplazar la función create_all de SQLAlchemy (que se usa para crear las tablas) por un mock.
      - mock_create_all.return_value = None: Simula que la función create_all no devuelve nada (como en una ejecución exitosa).
      - conexion = ConexionSingleton(): Se crea una instancia de la clase ConexionSingleton, que es la que maneja la conexión a la base de datos (en este caso mockeada).
       - Base.metadata.create_all(conexion.engine): Esta línea simula la creación de las tablas en la base de datos utilizando el engine de la conexión.                   - mock_create_all.assert_called_once_with(mock_conexion.engine): Verifica que la función create_all fue llamada una sola vez y con el engine correcto de la conexión mockeada.
- test de error en la creación de tablas: ene ste test se verifica que se maneje adecuadamente un error durante la creación de las tablas.
       - @patch con side_effect: En lugar de devolver None, se utiliza side_effect=SQLAlchemyError("Error en la base de datos") para simular que la función create_all genera un error de tipo SQLAlchemyError.
       - mock_create_all.assert_called_once_with(mock_conexion.engine): Como en el test anterior, acá se verifica que la función create_all haya sido llamada una sola vez con el engine correcto de la conexión mockeada. El test asegura que, a pesar de que ocurra un error en la creación de las tablas, la función create_all haya sido llamada una vez con el engine de la conexión mockeada.
- **test_registros_insert.py:** En términos generales, lo que se hace en este test es:
      - se crea una base de datos en memoria con sqlite.
      - se copian y pegan los modelos ya creados, que representan las tablas, para que ahora se creen en la base de datos simulada.
      - se define una función genérica para insertar los datos en las tablas.
      - se crea una función por cada tabla de tal manera que, si se ingresan datos, estos coincidan con los esperados.
- `main.py:` archivo donde se ejecuta el menú principal por consola.
- `queries:` archivo tipo ipynb que muestra algunas queries extras que podrían ser de utilidad. Se utilizan CTE's y funciones ventana.

  

## ⚙️ Instalación

1. clonar el repositorio:
- git clone https://github.com/avbm090/primer_proyecto_integrador.git
- cd primer_proyecto_integrador
2. crear entorno virtual: venv\Scripts\activate
3. configurar las variables de entorno.
4. Ejecutar: python main.py.
5. Ver archivo "queries" para ver uso de queries.