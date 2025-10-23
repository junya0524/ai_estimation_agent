def estimate_fp(ei, eo, eq, ilf, eif):
    """簡易FP法による見積もり"""
    weights = {"EI": 4, "EO": 5, "EQ": 4, "ILF": 7, "EIF": 5}
    ufp = ei*weights["EI"] + eo*weights["EO"] + eq*weights["EQ"] + ilf*weights["ILF"] + eif*weights["EIF"]
    afp = ufp * 0.65
    effort_pm = afp * 0.05
    cost = afp * 10000
    return {"UFP": ufp, "AFP": afp, "Effort_PM": effort_pm, "Cost_JPY": cost}
