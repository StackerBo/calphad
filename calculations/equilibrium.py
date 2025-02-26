from calculations.base_calculator import BaseCalculator
from tc_python import *

class EquilibriumCalculator(BaseCalculator):
    """
    This class is used to calculate the equilibrium of a system. Support for single and batch mode.
    """
    
    def calculate(self, temperature, compositions, mode = "batch"):
        """
        - mode = "batch", batch_equilibrium
        - mode = "single", single_equilibrium
        """
        if mode == "batch":
            try:
                return self._batch_equilibrium(temperature, compositions)
            except Exception as e:
                print(f"Error in batch equilibrium: {e}, return to single mode")
                return self._single_equilibrium(temperature, compositions)
        elif mode == "single":
            try:
                return self._single_equilibrium(temperature, compositions)
            except Exception as e:
                print(f"Error in single equilibrium: {e}")
                return None
        else:
            raise ValueError(f"Invalid mode: {mode}")
        
    def _batch_equilibrium(self, temperature, compositions):
        """
        Calculate the equilibrium of a system in batch mode.
        """
        with self.system.with_batch_equilibrium_calculation() as calc:
            calc.set_condition(ThermodynamicQuantity.temperature(), temperature)
            calc.set_conditions_for_equilibria([
                [(f"X({el})", comp[el]) for el in comp]
                for comp in compositions
            ])
            return calc.calculate(["G"]).get_values_of("G")
        
    def _single_equilibrium(self, temperature, compositions):
        """
        Calculate the equilibrium of a system in single mode.
        """
        results = []
        for comp in compositions:
            with self.system.with_single_equilibrium_calculation() as calc:
                calc.set_condition(ThermodynamicQuantity.temperature(), temperature)
                for el, val in comp.items():
                    calc.set_condition(ThermodynamicQuantity.mole_fraction_of_a_component(el), val)
                results.append(calc.calculate(["G"]).get_values_of("G"))
        return results
            