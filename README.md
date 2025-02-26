# 热力学计算系统

这是一个基于 Thermo-Calc Python API (tc-python) 的热力学计算系统，用于进行材料的平衡态计算。

## 功能特点

- 支持批量和单点平衡态计算
- 灵活的成分范围生成
- 模块化的计算器设计
- 异常处理和自动降级机制
- 相变温度计算（液相线、固相线和γ'相溶解温度）
- 稳定相分析和相分数计算

## 系统架构

系统主要包含以下组件：

1. **SystemManager**: 负责管理 Thermo-Calc 系统的创建和配置
2. **BaseCalculator**: 所有计算器的抽象基类
3. **EquilibriumCalculator**: 实现平衡态计算的具体计算器
4. **PhaseTransitionCalculator**: 相变温度计算器（使用固定相分数方法）
5. **PropertyManager**: 属性管理器（待实现）

## 使用方法

### 系统初始化

```python
from system_manager import SystemManager

# 初始化系统管理器
system_manager = SystemManager(database="TCNI8", elements=["Ni", "Al", "Cr"])
system = system_manager.create_system()
```

### 成分范围生成

```python
# 定义成分范围
composition_ranges = {
    "Al": [0.1, 0.2, 0.01],  # [min, max, step]
    "Cr": [0.15, 0.25, 0.01]
}

# 生成所有可能的成分组合
compositions = generate_compositions(composition_ranges)
```

### 平衡态计算

```python
from calculations.equilibrium import EquilibriumCalculator

# 创建计算器实例
calculator = EquilibriumCalculator(system)

# 执行计算
results = calculator.calculate(
    temperature=1273.15,
    compositions=compositions,
    mode="batch"  # 或 "single"
)
```

### 相变温度计算

```python
from calculations.phase_transition_calculator import PhaseTransitionCalculator

# 创建计算器实例
calculator = PhaseTransitionCalculator(
    database="TCNI",
    elements=["Ni", "Cr", "Co", "Al", "Mo"]
)

# 设置成分
calculator.set_composition({
    "Cr": 0.20,    # 20 wt% Cr
    "Co": 0.10,    # 10 wt% Co
    "Al": 0.05,    # 5 wt% Al
    "Mo": 0.03     # 3 wt% Mo
})

# 计算相变温度
liquidus_temp, solidus_temp, gamma_prime_solvus, phase_info = (
    calculator.calculate_transition_temperatures(
        initial_temperature=1700.0,
        gamma_prime_phase_name="FCC_L12#2"
    )
)
```

## 依赖要求

- tc-python
- Python 3.6+

## 注意事项

1. 批量计算模式会自动降级到单点计算模式（如果发生错误）
2. 确保系统中基体元素（如 Fe、Ni）作为平衡元素使用
3. 所有成分输入应为重量分数（wt%）
4. 相变温度计算需要合适的初始温度以确保计算收敛
5. γ'相溶解温度计算依赖于数据库中相的命名，默认使用"FCC_L12#2"
6. 每次相变温度计算都会创建新的 Thermo-Calc 会话，确保资源正确释放

## 贡献指南

1. Fork 该项目
2. 创建特性分支
3. 提交更改
4. 发起 Pull Request

## 许可证

待定