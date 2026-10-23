from collections import defaultdict
from math import isfinite


POSITIONS = [
 {"id": "R1", "desk": "Repo", "side": "OUT",
 "amount_m": 70.0},
 {"id": "P1", "desk": "Prime", "side": "OUT",
 "amount_m": 20.0},
 {"id": "C1", "desk": "Collateral", "side": "IN",
 "amount_m": 45.0},
]

SCENARIOS = {
 "base": {"Repo": 1.00, "Prime": 1.00, "Collateral" : 1.00},
 "funding_stress": {"Repo": 1.40, "Prime": 1.20, "Collateral" : 1.30},
 "severe": {"Repo": 1.80, "Prime": 1.65 , "Collateral" : 1.50},
}

required_fields = {"id", "desk" , "side", "amount_m"}

def calculate(positions, scenario, hqla_m):
    if not isinstance(positions, list):
        raise ValueError("Postions must be a list!")

    if not isinstance(scenario, dict):
        raise ValueError("Scenario is not a dictionary!")

    for desk,factor in scenario.items():

        if not isinstance(desk,str):
            raise ValueError("Desk is not a string!")
        if desk.strip() == "":
            raise ValueError("Desk is an empty string!")    

        if not isinstance(factor,(int,float)) or isinstance(factor,bool):
            raise ValueError("Stress factor is not a number!")
        if not isfinite(factor):
            raise ValueError("Stress factor is not finite!")
        if factor< 0:
            raise ValueError("Stress factor is negative!")

    if not isinstance(hqla_m,(int,float)) or isinstance(hqla_m,bool):
        raise ValueError("HQLA is not a number!")
    if not isfinite(hqla_m):
        raise ValueError("HQLA is not a finite number")
    if hqla_m<0:
        raise ValueError("HQLA must be non-negative")
    ids = set()
    by_desk = defaultdict(float)
    outflows = inflows = 0.0

    for p in positions:

        if not isinstance(p,dict):
            raise ValueError("Each position must be a dictionary!")
        
        for field in required_fields:
           if field not in p:
               raise ValueError(f"Missing required field: {field}")

         
        if not isinstance(p["desk"],str):
            raise ValueError("Desk is not a string!")
        if p["desk"].strip() == "":
            raise ValueError("Desk is an empty string!")
        desk = p["desk"].strip()
        if desk not in scenario:
            raise ValueError("There isn't a risk factor for this desk!")

        if not isinstance(p["id"],str):
            raise ValueError("Id is not a string!")
        transaction_id = p["id"].strip()
        if transaction_id == "":
            raise ValueError("Empty ID string!")
        if transaction_id in ids:
            raise ValueError("Duplicate Transaction ID")
        ids.add(transaction_id)
        
        if not isinstance(p["side"], str):
             raise ValueError("Transaction side must be a string!")
        side = p["side"].strip().upper()
        if side not in ("IN", "OUT"):
            raise ValueError("Invalid transaction side")

        if not isinstance(p["amount_m"],(int,float)) or isinstance(p["amount_m"],bool):
            raise ValueError("Amount is not a number!")
        if not isfinite(p["amount_m"]):
            raise ValueError("Amount is not a finite number!")
        if p["amount_m"]<0 :
            raise ValueError("Negative Input")

        stress = scenario[desk]
        amount = p["amount_m"]*stress

        if side == "OUT":
            outflows += amount
            by_desk[desk] += amount
        else:
            inflows += amount

    if outflows <= 0 :
        raise ValueError("Outflows are non-positive")

    recognized = min(inflows, 0.75*outflows)

    net = outflows - recognized

    return {
    "lcr_pct": 100 * hqla_m / net,
    "total_outflows_m": outflows,
    "total_inflows_m": inflows,
    "net_outflows_m": net,
    "outflows_by_desk_m": dict(by_desk),
}

if __name__ == "__main__":

    def test_base_scenario():
        result = calculate(POSITIONS, SCENARIOS["base"], 135.0)
    
        assert result["total_outflows_m"] == 90.0
        assert result["total_inflows_m"] == 45.0
        assert result["net_outflows_m"] == 45.0
        assert result["lcr_pct"] == 300.0

    print("Base scenario test passed!")

    for name,factors in SCENARIOS.items():
        print(name, calculate(POSITIONS, factors, 135.0))


