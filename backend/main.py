from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

class ConversionRequest(BaseModel):
    unit_from: str
    unit_to: str
    value: float

# Conversion rates (forward and reverse)
conversion_rates = {
    # Length
    ("meters", "feet"): 3.28084,
    ("feet", "meters"): 1 / 3.28084,
    
    ("kilometers", "miles"): 0.621371,
    ("miles", "kilometers"): 1 / 0.621371,
    
    ("centimeters", "inches"): 0.393701,
    ("inches", "centimeters"): 1 / 0.393701,
    
    ("millimeters", "inches"): 0.0393701,
    ("inches", "millimeters"): 1 / 0.0393701,

    # Weight
    ("kilograms", "pounds"): 2.20462,
    ("pounds", "kilograms"): 1 / 2.20462,

    ("grams", "ounces"): 0.035274,
    ("ounces", "grams"): 1 / 0.035274,

    # Temperature (special case)
    ("celsius", "fahrenheit"): lambda x: (x * 9/5) + 32,
    ("fahrenheit", "celsius"): lambda x: (x - 32) * 5/9,
    
    ("celsius", "kelvin"): lambda x: x + 273.15,
    ("kelvin", "celsius"): lambda x: x - 273.15,

    ("fahrenheit", "kelvin"): lambda x: (x - 32) * 5/9 + 273.15,
    ("kelvin", "fahrenheit"): lambda x: (x - 273.15) * 9/5 + 32,
}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Unit Converter API!"}

@app.post("/convert")
def convert_units(request: ConversionRequest):
    key = (request.unit_from, request.unit_to)
    if key in conversion_rates:
        conversion = conversion_rates[key]
        converted_value = conversion(request.value) if callable(conversion) else request.value * conversion
        return {"converted_value": converted_value}
    return {"error": "Conversion not supported"}
