def estimate_loc(loc_count):
    """LOC法による単純見積もり"""
    productivity = 500  # 1人月あたり500行と仮定
    effort_pm = loc_count / productivity
    cost = effort_pm * 200000  # 1人月=20万円で試算
    return {"Effort_PM": effort_pm, "Cost_JPY": cost}

