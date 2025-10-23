def estimate_cocomo(size_kloc, mode="organic"):
    """COCOMO基本モデル"""
    params = {
        "organic": (2.4, 1.05),
        "semi_detached": (3.0, 1.12),
        "embedded": (3.6, 1.20)
    }
    a, b = params.get(mode, params["organic"])
    effort = a * (size_kloc ** b)
    duration = 2.5 * (effort ** 0.38)
    cost = effort * 200000  # 1人月=20万円で試算
    return {"Effort_PM": effort, "Duration_Months": duration, "Cost_JPY": cost}
