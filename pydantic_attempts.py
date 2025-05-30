# YT link: https://www.youtube.com/watch?v=XIdQ6gO3Anc
# find there also Validator decorator to apply a customed validation on eny argument on your class (e.g. for initiation, for value toi be within range TBD)

# install the following packagess via 'uv add requirements.txt':
# "matplotlib>=3.10.3",
# "pandas>=2.2.3",
# "pydantic[email]>=2.11.5",


from pydantic import BaseModel, EmailStr, StrictStr, StrictInt, Field, field_validator



# basic
class User(BaseModel):
    name: StrictStr
    # name: str
    email: EmailStr
    account_id: StrictInt
    # account_id: int


try:
    user = {"name": "Shai", "email": "userphilips.com", "account_id": 12345}
    new_user = User(**user)
except Exception as e:
    print(e)
finally:
    user = {"name": "Shai", "email": "user@philips.com", "account_id": 12345}
    new_user = User(**user)
# 1 validation error for User email:
# value is not a valid email address: An email address must have an @-sign. [type=value_error, input_value='userphilips.com', input_type=str]



print()


# note that it can also catch multiple validation errors (if such introduced)
try:
    user = {"name": "Shai", "email": "user@philips.com", "account_id": "12345"}
    new_user = User(**user)
except Exception as e:
    print(e)
finally:
    user = {"name": "Shai", "email": "user@philips.com", "account_id": 12345}
    new_user = User(**user)
# 1 validation error for User account_id:
# Input should be a valid integer [type=int_type, input_value='12345', input_type=str]



print()




print(new_user) # auto repl that youdon't get with the basic class
# name='Shai' email='user@philips.com' account_id=12345


print()

class MyClass(BaseModel):
    install_component_version: str = Field(pattern=r"^[0-9]{2}\.[0-9]+\.[0-9]+$")

# my_class = MyClass(install_component_version="20.1984.70")

try:
    my_class = MyClass(install_component_version="2025/1984/70")
except Exception as e:
    print(e)
finally:
    my_class = MyClass(install_component_version="20.1984.70")
    # install_component_version = "20.1984.70"


print("\n", my_class.install_component_version)
# 2025.1984.70


# ==================================
# using customed validation (validator decorator)
# ==================================

print()

class Values(BaseModel):
    temperature: int
    humidity: int
    device: str

    @field_validator("temperature")
    def validate_temperature(cls, value):
        if not (-10 <= value <= 60):
            raise ValueError("Temperature must be between 0 and 100.")
        return value


    @field_validator("humidity")
    def validate_humidity(cls, value):
        if not (0 <= value <= 100):
            raise ValueError("Humidity must be between 0 and 100.")
        return value

reader1 = Values(temperature=25, humidity=50, device="sensor1")
# temperature=25 humidity=50 device='sensor1'

try:
    reader2 = Values(temperature=70, humidity=50, device="sensor2")
except Exception as e:
    print(e)
# Value error, Temperature must be between -10 and 70. [type=value_error, input_value=70, input_type=int]
# note that there's a bug in the debug printout


# =============================
# dataclass build-in alternative
# =============================


print()

from dataclasses import dataclass # not much data validation here!
# from dataclasses import dataclass, field

@dataclass
class DataClassUser:
    name: str
    email: str
    account_id: int


shai = DataClassUser(name='Shai', email="user@philips.com", account_id=12345)
print(shai)
# DataClassUser(name='Shai', email='user@philips.com', account_id=12345)

