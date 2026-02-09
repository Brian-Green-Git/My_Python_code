# -*- coding: utf-8 -*-
"""
Created on Wed Jan 28 17:09:55 2026

@author: brian green
"""

#%%
class Person:
    name = "Brian"
    surname = "Green"
    title = ""
    
    def update(self, update_title):
        self.title = update_title
           
create_object = Person()

get_title = input("Please enter the title: ")

create_object.update(get_title)

print(f"{create_object.title} {create_object.name} {create_object.surname}")

#%%
class Person1:
    name = "Brian"
    def __init__(self, uptitle, sur):
        self.title = uptitle
        self.surname = sur     
       
        
obj = Person1("Mr", "green.")

print(f"{obj.title}, {obj.name}, {obj.surname}")
            
#%%
class car: 
    brand = ""
    model = ""
    mileage = 0
    type 
    
    def update1(self, new_brand, new_model, new_mileage):
        self.brand = new_brand
        self.model = new_model
        self.mileage = new_mileage
        
    def __init__(self, edit):
        
        if edit == True:
            self.brand = ""
            self.model = ""
            self.mileage = 0
                    
#%%
import numpy as np
# import pandas as pd

class Numbers:    
    def __init__(self, inpt):
        
        self.initial_value = inpt
        self.changed_value = self.initial_value * 100
              
    def create(self):
        self.arr = np.linspace(1, 10, 3)
        self.null = np.zeros(20, int)
        return(self.arr, self.null)
               
obj = Numbers(52)

a,b = obj.create()

print(b, "\n", a)

#%%

class Sports:
    type = "Outdoor"
    distance = "short"
    use_hands = False
    
    def __init__(self, team):
        self.team = team

class Football(Sports):
    name = "Football"

    def __init__(self, team):
        self.team = "Chelsea" 

#%%
class Plant:
    def __init__(self, scientific_name, climate):
        self.scientific_name = scientific_name
        self.climate = climate

class Lotus(Plant):
    pass

#%%
class Animal:
    def __init__(self, name, sound):
        self.name = name
        self.sound= sound

class Dog(Animal):
    def make_sound(self):
        print(self.sound)
        
#%%

# Private Variables can be defined as class variables that cannot be accessed or 
# changed outside the class. Thus, encapsulated within one single class only.

# Private Variables can help in order to prevent any accidental changes that 
# might occur during the development process.

# In order for us to create a private variable, 
# we must add two underscores (__) before the variable's name.

class Capsule:
    test = True

    def __init__(self, value1):
        self.__value1 = value1
    
    def get_value(self):
        return self.__value1

    def set_value(self, new_val):
        self.__value1 = new_val

def test_answer(value1, new_val):
    obj = Capsule(value1)
    obj.set_value(new_val)
    return obj.get_value()

print(test_answer(10, 15))

#%%

class Login:
    def __init__(self, username, password):
        self.__username = username
        self.__password = password
    
    def see_credentials(self):
        return (self.__username, self.__password)

    def set_new_pass(self, new_pass):
        self.__password = new_pass

    def set_new_user(self, new_user):
        self.__username = new_user

def test_answer(username, password, new_user, new_pass):
    obj = Login(username, password) # sets initial info to username and password
    obj.set_new_pass(new_pass)      # changes intial password to new password
    obj.set_new_user(new_user)      # changes intial username to new username
    return obj.see_credentials()    # returns a tuple containing the private username and password info

username, password = test_answer("Brian", 0000, "Brian_new", 123456)

print(username)
print(password)

#%%
class Vehicle:
    def __init__(self, company, fuel_amt, milage_per_litre):
        self.company = company
        self.fuel_amt = fuel_amt
        self.milage_per_litre = milage_per_litre

class Car(Vehicle):

    def run(self, distance_km):
        total_distance_to_travel = distance_km
        total_amt_fuel = self.fuel_amt
        distance_per_liter = self.milage_per_litre

        total_distance_can_travel = total_amt_fuel * distance_per_liter

        total_fuel_used = total_distance_to_travel / distance_per_liter

        if total_distance_to_travel < total_distance_can_travel:
            self.fuel_amt = self.fuel_amt - total_fuel_used
            print("Ran Successfully")

        else:
            print("Not Enough Fuel")


obj = Car("Mercedes Benz", 10, 20)
obj.run(10)
          
obj2 = Car("Hyundai", 10, 1)
obj2.run(11)

#%%
class System:
    def __init__(self, username, password):
        self.__username = username
        self.__password = password
    
    def login(self, user, passw):

        if (self.__username == user and self.__password == passw) == True:
            print("Login Successful")

        else:
            print("Invalid Credentials") 

def test_answer(username, password, user, passw):
        obj = System(username, password)
        obj.login(user, passw)
        
test_answer("username", "password", "user", "passw")

#%%
class Numbers:
    def __init__(self, values1, values2):
        self.values1 = values1
        self.values2 = values2

class Calculator(Numbers):

    def add(self):
        return(self.values1 + self.values2)

    def multiply(self):
        return(self.values1 * self.values2)

    def subtract(self):
        return(self.values1 - self.values2)

def test_answer(num1, num2):
    obj = Calculator(num1, num2)
    return obj.add(), obj.multiply(), obj.subtract()

test_answer(15, 26)
