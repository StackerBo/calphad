from tc_python import *
from typing import Dict, List, Tuple, Optional
import os

class PhaseTransitionCalculator:
    """使用固定相分数方法计算相变温度的计算器。"""
    
    def __init__(self, database: str, elements: List[str]):
        """
        初始化计算器。
        
        Args:
            database: 数据库名称（如 'TCNI'）
            elements: 要考虑的元素列表
        """
        self.database = database
        self.elements = elements
        self.composition = {}
        self.cache_folder = "phase_transition_cache"
        
    def set_composition(self, composition: Dict[str, float]) -> None:
        """
        设置合金成分。
        
        Args:
            composition: 元素成分字典 {element: weight_fraction}
        """
        self.composition = composition
        
    def get_stable_phases(self, calc_result) -> Dict[str, float]:
        """
        获取稳定相及其数量。
        
        Args:
            calc_result: 平衡计算结果
            
        Returns:
            稳定相及其数量的字典
        """
        stable_phases = {}
        for phase in calc_result.get_stable_phases():
            amount = calc_result.get_value_of(f'NP({phase})')
            stable_phases[phase] = amount
        return stable_phases
        
    def calculate_transition_temperatures(self, 
                                       initial_temperature: float = 1700.0,
                                       gamma_prime_phase_name: str = "FCC_L12#2") -> Tuple[Optional[float], Optional[float], Optional[float], Dict]:
        """
        计算液相线、固相线和gamma prime相溶解温度。
        
        Args:
            initial_temperature: 初始平衡计算温度（K）
            gamma_prime_phase_name: gamma prime相在数据库中的名称
            
        Returns:
            Tuple[float, float, float, Dict]: (液相线温度, 固相线温度, gamma prime溶解温度, 相信息字典)
        """
        phase_info = {}
        
        with TCPython() as session:
            # 设置系统
            calculation = (
                session
                .set_cache_folder(self.cache_folder)
                .select_database_and_elements(self.database, self.elements)
                .get_system()
                .with_single_equilibrium_calculation()
                .set_condition(ThermodynamicQuantity.temperature(), initial_temperature)
            )
            
            # 设置成分
            for element, weight_fraction in self.composition.items():
                calculation.set_condition(
                    ThermodynamicQuantity.mass_fraction_of_a_component(element),
                    weight_fraction
                )
            
            try:
                # 初始平衡计算
                initial_result = calculation.calculate()
                phase_info['initial_equilibrium'] = {
                    'temperature': initial_result.get_value_of(ThermodynamicQuantity.temperature()),
                    'phases': self.get_stable_phases(initial_result)
                }
                
                print("Finished initial equilibrium calculation")
                
                # 计算液相线温度（液相分数为1）
                liquidus_result = (
                    calculation
                    .remove_condition(ThermodynamicQuantity.temperature())
                    .set_phase_to_fixed("LIQUID", 1.0)
                    .calculate()
                )
                liquidus_temp = liquidus_result.get_value_of(ThermodynamicQuantity.temperature())
                phase_info['liquidus'] = {
                    'temperature': liquidus_temp,
                    'phases': self.get_stable_phases(liquidus_result)
                }
                
                print("Finished liquidus calculation")
                # 计算固相线温度（液相分数为0）
                solidus_result = (
                    calculation
                    .set_phase_to_fixed("LIQUID", 0.0)
                    .calculate()
                )
                solidus_temp = solidus_result.get_value_of(ThermodynamicQuantity.temperature())
                phase_info['solidus'] = {
                    'temperature': solidus_temp,
                    'phases': self.get_stable_phases(solidus_result)
                }
                
                print("Finished solidus calculation")
                # 计算gamma prime相溶解温度
                # 首先重置条件
                calculation.remove_condition("NP(LIQUID)")
                
                # 设置gamma prime相分数为0来找到溶解温度
                gamma_prime_result = (
                    calculation
                    .set_phase_to_fixed(gamma_prime_phase_name, 0.0)
                    .calculate()
                )
                gamma_prime_solvus = gamma_prime_result.get_value_of(ThermodynamicQuantity.temperature())
                phase_info['gamma_prime_solvus'] = {
                    'temperature': gamma_prime_solvus,
                    'phases': self.get_stable_phases(gamma_prime_result)
                }
                
                print("Finished gamma prime solvus calculation")
                return liquidus_temp, solidus_temp, gamma_prime_solvus, phase_info
                
            except Exception as e:
                print(f"计算过程中发生错误: {str(e)}")
                return None, None, None, phase_info 