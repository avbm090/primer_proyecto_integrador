# 🛒 Sistema de Gestión de Ventas

**Proyecto Integrador - SoyHenry**  
Autor: [Tu Nombre]  
Fecha: Junio 2025

---

## 📌 Descripción

Este proyecto es un sistema completo de gestión de ventas desarrollado en Python. Aplica principios de Programación Orientada a Objetos (POO), patrones de diseño (Factory, Singleton, Builder, Strategy), acceso a bases de datos relacionales con SQLAlchemy, y consultas avanzadas con Pandas.

**Características principales:**

- Carga masiva de datos desde archivos JSON.  
- Registro de ventas y actualización automática de stock.  
- Generación de informes con distintas estrategias.  
- Conexión segura y única a MySQL usando variables de entorno.  
- Pruebas automatizadas con `pytest`.  

---

## 📁 Estructura del Proyecto

.
├── cargar_datos.py # Carga de datos desde JSON con validación
├── conexion_singleton.py # Patrón Singleton para conexión a DB
├── modelos_factory.py # Clases ORM con Factory pattern
├── query.py # Consultas SQL con SQLAlchemy
├── informes/ # Reportes con patrón Strategy
│ ├── base.py
│ ├── informe_por_ciudad.py
│ ├── informe_ventas_totales.py
│ └── ...
├── main.py # Punto de entrada principal
├── tests/ # Pruebas unitarias con pytest
│ └── test_modelos.py
├── requirements.txt
└── README.md

yaml
Copiar
Editar

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