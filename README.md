# 🛒 Sistema simple de gestión de ventas 

**Proyecto Integrador**  
Fecha: Junio 2025

---

## 📌 Descripción

Este proyecto es un sistema básico de gestión de ventas desarrollado en Python. Aplica principios de Programación Orientada a Objetos (POO), patrones de diseño (Factory, Singleton, Strategy), acceso a bases de datos relacionales con SQLAlchemy, con creación de triggers y procedures, y queries con CTE's, funciones de agregación y funciones ventana.

**Características principales:**

- Carga masiva de datos desde archivos JSON.  
- Registro de ventas y actualización automática de stock.  
- Generación de informes con distintas estrategias.  
- Conexión segura y única a MySQL usando variables de entorno.  
- Pruebas automatizadas con `pytest`.  

---

## 📁 Estructura del Proyecto


- pycache/ # archivos compilados de Python
-  cache/ #archivos temporales de caché
-  data/ # datos de entrada
-  informes_resultado/ # resultados generados de los informes como json
- logs/ # archivos de registro (logs)
-  sql/ # patron strategy para el tipo de consulta
-  src/ # código fuente principal del sistema
-  tests/ # Pruebas unitarias con pytest
   - test_modelos.py # Ejemplo de pruebas unitarias
-  venv/ # entorno virtual
-  .env # variables de entorno
-  .gitignore # archivos y carpetas a ignorar por Git
-  main.py # punto de entrada principal
-  queries.ipynb # notebook de queries con cte's
-  README.md 
-  requirements.txt # dependencias

---

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
