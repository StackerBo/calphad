from calculations.phase_transition_calculator import PhaseTransitionCalculator

def print_phase_info(phase_dict: dict) -> None:
    """打印相信息。"""
    for phase, amount in phase_dict.items():
        print(f"    {phase}: {amount:.3f}")

def main():
    """示例：使用相变温度计算器计算Ni基高温合金的相变温度。"""
    
    # 创建计算器实例
    calculator = PhaseTransitionCalculator(
        database="TCNI10",  # 使用镍基合金数据库
        elements=["Ni", "Co", "Cr", "Mo", "Al", "Ti", "Hf", "B", "C", "Zr"]
    )
    
    # 设置成分
    calculator.set_composition({
        "Co": 15.6,
        "Cr": 11.2,
        "Mo": 6.5,
        "Al": 4.37,
        "Ti": 4.36,
        "Hf": 0.5,
        "B": 0.015,
        "C": 0.018,
        "Zr": 0.03
    })
    
    # 计算相变温度
    liquidus_temp, solidus_temp, gamma_prime_solvus, phase_info = (
        calculator.calculate_transition_temperatures(
            initial_temperature=1700.0,
            gamma_prime_phase_name="FCC_L12#2"
        )
    )
    
    # 打印结果
    print("\n计算结果：")
    print("\n1. 初始平衡状态：")
    print(f"温度: {phase_info['initial_equilibrium']['temperature']:.2f} K")
    print("稳定相:")
    print_phase_info(phase_info['initial_equilibrium']['phases'])
    
    if all([liquidus_temp, solidus_temp, gamma_prime_solvus]):
        print(f"\n2. 液相线温度: {liquidus_temp:.2f} K")
        print("稳定相:")
        print_phase_info(phase_info['liquidus']['phases'])
        
        print(f"\n3. 固相线温度: {solidus_temp:.2f} K")
        print("稳定相:")
        print_phase_info(phase_info['solidus']['phases'])
        
        print(f"\n4. γ'相溶解温度: {gamma_prime_solvus:.2f} K")
        print("稳定相:")
        print_phase_info(phase_info['gamma_prime_solvus']['phases'])
        
        print(f"\n5. 温度区间:")
        print(f"    凝固区间: {liquidus_temp - solidus_temp:.2f} K")
        print(f"    γ'相稳定区间: {gamma_prime_solvus - solidus_temp:.2f} K")
    else:
        print("\n计算失败，请检查计算条件。")

if __name__ == "__main__":
    main() 