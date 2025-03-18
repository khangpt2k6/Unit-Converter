import tkinter as tk
from tkinter import ttk
import math

class UnitConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Unit Converter")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # Configure styles for a modern look
        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure("TFrame", background="#f5f5f5")
        style.configure("TButton", font=("Arial", 10, "bold"), background="#007bff", foreground="white")
        style.map("TButton", background=[("active", "#0069d9")])
        style.configure("TLabel", font=("Arial", 10), background="#f5f5f5")
        style.configure("Header.TLabel", font=("Arial", 16, "bold"), background="#f5f5f5")
        style.configure("Result.TLabel", font=("Arial", 12), background="#e9ecef", padding=10)
        
        # Main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Unit Converter", style="Header.TLabel")
        title_label.pack(pady=(0, 20))
        
        # Category selection frame
        category_frame = ttk.Frame(main_frame)
        category_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(category_frame, text="Category:").pack(anchor=tk.W)
        
        # Categories and their units
        self.categories = {
            "Base": ["Binary", "Octal", "Decimal", "Hexadecimal"],
            "Time": ["Milliseconds", "Seconds", "Minutes", "Hours", "Days", "Weeks", "Months", "Years"],
            "Temperature": ["Celsius", "Fahrenheit", "Kelvin"],
            "Mass": ["Milligrams", "Grams", "Kilograms", "Ounces", "Pounds", "Tons"],
            "Length": ["Millimeters", "Centimeters", "Meters", "Kilometers", "Inches", "Feet", "Yards", "Miles"],
            "Volume": ["Milliliters", "Liters", "Cubic Meters", "Fluid Ounces", "Cups", "Pints", "Quarts", "Gallons"]
        }
        
        # Create category radio buttons
        self.category_var = tk.StringVar(value="Length")
        category_buttons_frame = ttk.Frame(category_frame)
        category_buttons_frame.pack(fill=tk.X, pady=5)
        
        col = 0
        for category in self.categories:
            rb = ttk.Radiobutton(
                category_buttons_frame, 
                text=category, 
                value=category, 
                variable=self.category_var,
                command=self.update_units
            )
            rb.grid(row=0, column=col, padx=5)
            col += 1
        
        # Conversion frame
        conversion_frame = ttk.Frame(main_frame)
        conversion_frame.pack(fill=tk.X, pady=10)
        
        # Input value
        input_frame = ttk.Frame(conversion_frame)
        input_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(input_frame, text="Value:").grid(row=0, column=0, padx=(0, 10), sticky=tk.W)
        self.input_value = ttk.Entry(input_frame, width=30)
        self.input_value.grid(row=0, column=1, sticky=tk.W)
        
        # From and To units frame
        units_frame = ttk.Frame(conversion_frame)
        units_frame.pack(fill=tk.X, pady=10)
        
        # From unit - FIXED: separate frames for each dropdown
        from_frame = ttk.Frame(units_frame)
        from_frame.grid(row=0, column=0, padx=(0, 20), sticky=tk.W)
        
        ttk.Label(from_frame, text="From:").pack(anchor=tk.W)
        self.from_unit = ttk.Combobox(from_frame, width=15, state="readonly")
        self.from_unit.pack(pady=5)
        
        # To unit - FIXED: dropdown added to to_frame instead of from_frame
        to_frame = ttk.Frame(units_frame)
        to_frame.grid(row=0, column=1, sticky=tk.W)
        
        ttk.Label(to_frame, text="To:").pack(anchor=tk.W)
        self.to_unit = ttk.Combobox(to_frame, width=15, state="readonly")  # FIXED HERE
        self.to_unit.pack(pady=5)
        
        # Convert button
        convert_button = ttk.Button(main_frame, text="Convert", command=self.convert)
        convert_button.pack(fill=tk.X, pady=15)
        
        # Result frame
        result_frame = ttk.Frame(main_frame, padding=10)
        result_frame.pack(fill=tk.X)
        
        self.result_var = tk.StringVar(value="")
        result_label = ttk.Label(
            result_frame, 
            textvariable=self.result_var, 
            style="Result.TLabel",
            anchor=tk.CENTER
        )
        result_label.pack(fill=tk.X)
        
        # Initialize units
        self.update_units()
    
    def update_units(self):
        """Update unit dropdown options based on selected category"""
        category = self.category_var.get()
        units = self.categories[category]
        
        self.from_unit['values'] = units
        self.to_unit['values'] = units
        
        # Set default selections
        self.from_unit.current(0)
        self.to_unit.current(1 if len(units) > 1 else 0)
        
        # Clear result
        self.result_var.set("")
    
    def convert(self):
        """Perform the unit conversion"""
        try:
            value = self.input_value.get().strip()
            if not value:
                self.result_var.set("Please enter a value")
                return
                
            category = self.category_var.get()
            from_unit = self.from_unit.get()
            to_unit = self.to_unit.get()
            
            # Perform conversion based on category
            if category == "Base":
                result = self.convert_base(value, from_unit, to_unit)
            elif category == "Temperature":
                result = self.convert_temperature(value, from_unit, to_unit)
            else:
                result = self.convert_standard(value, category, from_unit, to_unit)
                
            self.result_var.set(f"Result: {result}")
            
        except ValueError:
            self.result_var.set("Error: Invalid input value")
        except Exception as e:
            self.result_var.set(f"Error: {str(e)}")
    
    def convert_base(self, value, from_unit, to_unit):
        """Convert between different number bases"""
        bases = {"Binary": 2, "Octal": 8, "Decimal": 10, "Hexadecimal": 16}
        
        # Handle input based on base type
        try:
            if from_unit == "Hexadecimal":
                decimal = int(value, 16)
            elif from_unit == "Binary":
                value = value.replace(" ", "")  # Allow spaces in binary
                decimal = int(value, 2)
            elif from_unit == "Octal":
                decimal = int(value, 8)
            else:  # Decimal
                decimal = int(value)
        except ValueError:
            raise ValueError(f"Invalid {from_unit} value")
        
        # Convert to target base
        if to_unit == "Decimal":
            return str(decimal)
        elif to_unit == "Binary":
            return bin(decimal)[2:]  # Remove '0b' prefix
        elif to_unit == "Octal":
            return oct(decimal)[2:]  # Remove '0o' prefix
        elif to_unit == "Hexadecimal":
            return hex(decimal)[2:].upper()  # Remove '0x' prefix and convert to uppercase
    
    def convert_temperature(self, value, from_unit, to_unit):
        """Convert between temperature units"""
        try:
            value = float(value)
        except ValueError:
            raise ValueError("Temperature must be a number")
        
        # Convert to Celsius first
        if from_unit == "Celsius":
            celsius = value
        elif from_unit == "Fahrenheit":
            celsius = (value - 32) * 5/9
        elif from_unit == "Kelvin":
            celsius = value - 273.15
        
        # Convert from Celsius to target unit
        if to_unit == "Celsius":
            result = celsius
        elif to_unit == "Fahrenheit":
            result = (celsius * 9/5) + 32
        elif to_unit == "Kelvin":
            result = celsius + 273.15
        
        return self.format_number(result)
    
    def convert_standard(self, value, category, from_unit, to_unit):
        """Standard conversion using conversion factors"""
        try:
            value = float(value)
        except ValueError:
            raise ValueError("Value must be a number")
        
        # Conversion factors to base unit for each category
        conversion_factors = {
            "Time": {
                "Milliseconds": 0.001,
                "Seconds": 1,
                "Minutes": 60,
                "Hours": 3600,
                "Days": 86400,
                "Weeks": 604800,
                "Months": 2592000,  # 30-day month
                "Years": 31536000,  # 365-day year
            },
            "Mass": {
                "Milligrams": 0.001,
                "Grams": 1,
                "Kilograms": 1000,
                "Ounces": 28.3495,
                "Pounds": 453.592,
                "Tons": 907185,
            },
            "Length": {
                "Millimeters": 0.001,
                "Centimeters": 0.01,
                "Meters": 1,
                "Kilometers": 1000,
                "Inches": 0.0254,
                "Feet": 0.3048,
                "Yards": 0.9144,
                "Miles": 1609.34,
            },
            "Volume": {
                "Milliliters": 0.001,
                "Liters": 1,
                "Cubic Meters": 1000,
                "Fluid Ounces": 0.0295735,
                "Cups": 0.236588,
                "Pints": 0.473176,
                "Quarts": 0.946353,
                "Gallons": 3.78541,
            }
        }
        
        # Convert to base unit then to target unit
        base_value = value * conversion_factors[category][from_unit]
        result = base_value / conversion_factors[category][to_unit]
        
        return self.format_number(result)
    
    def format_number(self, num):
        """Format number to be more readable"""
        if num == int(num):
            return str(int(num))
        else:
            # Display up to 6 decimal places, removing trailing zeros
            return f"{num:.6f}".rstrip('0').rstrip('.') if '.' in f"{num:.6f}" else f"{num:.6f}"

if __name__ == "__main__":
    root = tk.Tk()
    app = UnitConverter(root)
    root.mainloop()
