import json
import itertools
from system_manager import SystemManager
from property_manager import PropertyManager

def generate_compositions(composition_ranges):
    """
    Generate all possible compositions from the given ranges.
    """
    elements = list(composition_ranges.keys())
    ranges = [composition_ranges[el] for el in elements]
    
    compositions = []
    for values in itertools.product(
        *[list(range(r[0]*100, int(r[1]*100) + 1, int(r[2]*100))) for r in ranges]
    ):
        comp = {elements[i]: values[i] / 100 for i in range(len(elements))}
        comp["Ni"] = round(1 - sum(comp.values()), 4)
        compositions.append(comp)
    
    return compositions

def main():
    with open("configs/systems.json", "r") as f:
        config_data = json.load(f)
        
    for system_config in config_data["systems"]:
        system_manager = SystemManager(system_config["database"], system_config["elements"])
        system = system_manager.create_system()
        property_manager = PropertyManager(system)
        
        compositions = generate_compositions(system_config["composition_ranges"])
        
        for prop in system_config["properties"]:
            mode = prop.get("mode", "batch")
            parameters = prop["parameters"]
            parameters["compositions"] = compositions
            
            print(f"Calculating property: {prop["type"]}, mode: {mode}, parameters: {parameters}")
            result = property_manager.calculate(prop["type"], mode, **parameters)
            
            for i, comp in enumerate(compositions):
                print(f"Composition {i+1}: {comp}, Property: {result[i]:.4f}")
                
if __name__ == "__main__":
    main()