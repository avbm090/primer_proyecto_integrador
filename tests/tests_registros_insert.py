import os
import logging
from sqlalchemy import create_engine, text, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pytest

logging.basicConfig(level=logging.INFO)

DATABASE_URL = "sqlite:///:memory:"  # base de datos sqlite en memoria para simular

Base = declarative_base()

# se definen y crean las tablas en entorno simulado

from sqlalchemy import Column, Integer, String, DECIMAL, DATETIME, CHAR, TIME, ForeignKey
from sqlalchemy.orm import relationship

class Category(Base):
    __tablename__ = 'categories'
    CategoryID = Column(Integer, primary_key=True, autoincrement=True)
    CategoryName = Column(String(100))

class Country(Base):
    __tablename__ = 'countries'
    CountryID = Column(Integer, primary_key=True, autoincrement=True)
    CountryName = Column(String(100))
    CountryCode = Column(String(10))

class City(Base):
    __tablename__ = 'cities'
    CityID = Column(Integer, primary_key=True, autoincrement=True)
    CityName = Column(String(100))
    Zipcode = Column(String(10))
    CountryID = Column(Integer, ForeignKey('countries.CountryID'))
    country = relationship("Country")

class Customer(Base):
    __tablename__ = 'customers'
    CustomerID = Column(Integer, primary_key=True, autoincrement=True)
    FirstName = Column(String(50))
    MiddleInitial = Column(CHAR(1))
    LastName = Column(String(50))
    CityID = Column(Integer, ForeignKey('cities.CityID'))
    Address = Column(String(150))
    city = relationship("City")

class Employee(Base):
    __tablename__ = 'employees'
    EmployeeID = Column(Integer, primary_key=True, autoincrement=True)
    FirstName = Column(String(50))
    MiddleInitial = Column(CHAR(1))
    LastName = Column(String(50))
    BirthDate = Column(DATETIME)
    Gender = Column(CHAR(1))
    CityID = Column(Integer, ForeignKey('cities.CityID'))
    HireDate = Column(DATETIME)
    city = relationship("City")

class Product(Base):
    __tablename__ = 'products'
    ProductID = Column(Integer, primary_key=True, autoincrement=True)
    ProductName = Column(String(150))
    Price = Column(DECIMAL(10, 4))
    CategoryID = Column(Integer, ForeignKey('categories.CategoryID'))
    Class = Column(String(20))
    ModifyDate = Column(TIME)
    Resistant = Column(String(20))
    IsAllergic = Column(String(10))
    VitalityDays = Column(Integer)

class Sale(Base):
    __tablename__ = 'sales'
    SalesID = Column(Integer, primary_key=True, autoincrement=True)
    SalesPersonID = Column(Integer, ForeignKey('employees.EmployeeID'))
    CustomerID = Column(Integer, ForeignKey('customers.CustomerID'))
    ProductID = Column(Integer, ForeignKey('products.ProductID'))
    Quantity = Column(Integer)
    Discount = Column(DECIMAL(5, 2))
    TotalPrice = Column(DECIMAL(10, 2))
    SalesDate = Column(TIME)
    TransactionNumber = Column(String(50))


####################################################################################


# función para insertar lso datos:

def insertar_datos(session, tabla, **datos):
    try:
        columns = ', '.join(datos.keys())
        values = ', '.join([f"'{v}'" for v in datos.values()])
        query = f"INSERT INTO {tabla} ({columns}) VALUES ({values})"
        
        session.execute(text(query))
        session.commit()
        logging.info(f"datos insertados en la tabla {tabla}")
    except Exception as e:
        session.rollback()
        logging.error(f"error al insertar datos en {tabla}: {e}", exc_info=True)
    finally:
        pass


#####################################################################################

# la base de datos sólo se crea y se conecta una vez al inicio del módulo, 
# y después se reutiliza para todas las pruebas dentro de ese módulo.

@pytest.fixture(scope='module')
def session():
    engine = create_engine(DATABASE_URL, echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

# test para insert categoría
def test_insertar_categoria(session):
    datos = {'CategoryName': 'Electronics'}
    tabla = 'categories'
    insertar_datos(session, tabla, **datos)
    
    resultado = session.execute(text("SELECT CategoryName FROM categories WHERE CategoryName = 'Electronics'"))
    row = resultado.fetchone()
    
    assert row is not None
    assert row[0] == 'Electronics'

# test para insert país
def test_insertar_pais(session):
    datos = {'CountryName': 'Mexico', 'CountryCode': 'MX'}
    tabla = 'countries'
    insertar_datos(session, tabla, **datos)
    
    resultado = session.execute(text("SELECT CountryName FROM countries WHERE CountryName = 'Mexico'"))
    row = resultado.fetchone()
    
    assert row is not None
    assert row[0] == 'Mexico'

# test para insert ciudad
def test_insertar_ciudad(session):
    session.execute(text("INSERT INTO countries (CountryName, CountryCode) VALUES ('USA', 'US')"))
    session.commit()
    
    datos = {'CityName': 'New York', 'Zipcode': '10001', 'CountryID': 1}
    tabla = 'cities'
    insertar_datos(session, tabla, **datos)
    
    resultado = session.execute(text("SELECT CityName FROM cities WHERE CityName = 'New York'"))
    row = resultado.fetchone()
    
    assert row is not None
    assert row[0] == 'New York'

# test para insert producto
def test_insertar_producto(session):
    session.execute(text("INSERT INTO categories (CategoryName) VALUES ('Electronics')"))
    session.commit()

    datos = {'ProductName': 'Laptop', 'Price': 1000.0, 'CategoryID': 1}
    tabla = 'products'
    insertar_datos(session, tabla, **datos)

    resultado = session.execute(text("SELECT ProductName, Price FROM products WHERE ProductName = 'Laptop'"))
    row = resultado.fetchone()

    assert row is not None
    assert row[0] == 'Laptop'
    assert row[1] == 1000.0

# test para insert empleado
def test_insertar_empleado(session):
    session.execute(text("INSERT INTO cities (CityName, Zipcode, CountryID) VALUES ('New York', '10001', 1)"))
    session.commit()

    datos = {
        'FirstName': 'juanito',
        'MiddleInitial': 'D',
        'LastName': 'juani',
        'BirthDate': '1990-01-01',
        'Gender': 'M',
        'CityID': 1,
        'HireDate': '2025-06-07'
    }
    tabla = 'employees'
    insertar_datos(session, tabla, **datos)

    resultado = session.execute(text("SELECT FirstName, LastName, Gender FROM employees WHERE FirstName = 'juanito' AND LastName = 'juani'"))
    row = resultado.fetchone()

    assert row is not None
    assert row[0] == 'juanito'
    assert row[1] == 'juani'
    assert row[2] == 'M'

# test para insert cliente
def test_insertar_cliente(session):
    session.execute(text("INSERT INTO cities (CityName, Zipcode, CountryID) VALUES ('Los Angeles', '90001', 1)"))
    session.commit()

    datos = {'FirstName': 'Alicia', 'MiddleInitial': 'S', 'LastName': 'Smith', 'CityID': 1, 'Address': '123 Main St'}
    tabla = 'customers'
    insertar_datos(session, tabla, **datos)

    resultado = session.execute(text("SELECT FirstName, LastName, Address FROM customers WHERE FirstName = 'Alicia' AND LastName = 'Smith'"))
    row = resultado.fetchone()

    assert row is not None
    assert row[0] == 'Alicia'
    assert row[1] == 'Smith'
    assert row[2] == '123 Main St'

# test para insertar venta
def test_insertar_venta(session):
    session.execute(text("INSERT INTO categories (CategoryName) VALUES ('Electronics')"))
    session.execute(text("INSERT INTO products (ProductName, Price, CategoryID) VALUES ('Laptop', 1000.0, 1)"))
    session.execute(text("INSERT INTO cities (CityName, Zipcode, CountryID) VALUES ('New York', '10001', 1)"))
    session.execute(text("INSERT INTO customers (FirstName, LastName, CityID, Address) VALUES ('John', 'Doe', 1, '123 Main St')"))
    session.execute(text("INSERT INTO employees (FirstName, LastName, BirthDate, Gender, CityID, HireDate) VALUES ('Jane', 'Smith', '1985-05-15', 'F', 1, '2022-01-01')"))
    session.commit()

    datos = {
        'SalesPersonID': 1,
        'CustomerID': 1,
        'ProductID': 1,
        'Quantity': 2,
        'Discount': 0.1,
        'TotalPrice': 1800.0,
        'SalesDate': '12:00:00',
        'TransactionNumber': 'TX123'
    }
    tabla = 'sales'
    insertar_datos(session, tabla, **datos)

    resultado = session.execute(text("SELECT SalesDate, TransactionNumber, TotalPrice FROM sales WHERE TransactionNumber = 'TX123'"))
    row = resultado.fetchone()

    assert row is not None
    assert row[0] == '12:00:00'
    assert row[1] == 'TX123'
    assert row[2] == 1800.0
