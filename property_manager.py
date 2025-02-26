from calculations.equilibrium import EquilibriumCalculator

class PropertyManager:
    """
    Manager for calculating thermodynamic properties.
    """
    def __init__(self, system):
        self.system = system
        self.calculators = {
            "equilibrium": EquilibriumCalculator(system)
        }
        
    def calculate(self, property_name, mode="batch", **kwargs):
        if property_name not in self.calculators:
            raise ValueError(f"Unsupported property: {property_name}")
        
        calculator = self.calculators[property_name]
        return calculator.calculate(mode = mode, **kwargs)
    
    def register_calculator(self, property_name, calculator):
        """
        Register a new calculator for a property.
        """
        self.calculators[property_name] = calculator