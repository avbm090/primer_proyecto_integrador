from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, DECIMAL, Time, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

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
    CountryID = Column(Integer, ForeignKey('countries.CountryID', ondelete='CASCADE', onupdate='CASCADE'))

    country = relationship("Country")

class Customer(Base):
    __tablename__ = 'customers'
    CustomerID = Column(Integer, primary_key=True, autoincrement=True)
    FirstName = Column(String(50))
    MiddleInitial = Column(CHAR(1))
    LastName = Column(String(50))
    CityID = Column(Integer, ForeignKey('cities.CityID', ondelete='SET NULL', onupdate='CASCADE'))
    Address = Column(String(150))

    city = relationship("City")

class Employee(Base):
    __tablename__ = 'employees'
    EmployeeID = Column(Integer, primary_key=True, autoincrement=True)
    FirstName = Column(String(50))
    MiddleInitial = Column(CHAR(1))
    LastName = Column(String(50))
    BirthDate = Column(DateTime)
    Gender = Column(CHAR(1))
    CityID = Column(Integer, ForeignKey('cities.CityID', ondelete='SET NULL', onupdate='CASCADE'))
    HireDate = Column(DateTime)

    city = relationship("City")

class Product(Base):
    __tablename__ = 'products'
    ProductID = Column(Integer, primary_key=True, autoincrement=True)
    ProductName = Column(String(150))
    Price = Column(DECIMAL(10, 4))
    CategoryID = Column(Integer, ForeignKey('categories.CategoryID', ondelete='SET NULL', onupdate='CASCADE'))
    Class = Column(String(20))
    ModifyDate = Column(Time)
    Resistant = Column(String(20))
    IsAllergic = Column(String(10))
    VitalityDays = Column(Integer)

    category = relationship("Category")

class Sale(Base):
    __tablename__ = 'sales'
    SalesID = Column(Integer, primary_key=True, autoincrement=True)
    SalesPersonID = Column(Integer, ForeignKey('employees.EmployeeID'))
    CustomerID = Column(Integer, ForeignKey('customers.CustomerID'))
    ProductID = Column(Integer, ForeignKey('products.ProductID'))
    Quantity = Column(Integer)
    Discount = Column(DECIMAL(5, 2))
    TotalPrice = Column(DECIMAL(10, 2))
    SalesDate = Column(Time)
    TransactionNumber = Column(String(50))

    salesperson = relationship("Employee")
    customer = relationship("Customer")
    product = relationship("Product")
