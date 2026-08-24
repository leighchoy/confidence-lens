import traceback

import pandas as pd

from config import processed_path


"""
WACC = ((Debt/(Total Value))* Cost of Debt) + ((Equity/(Total Value)) x Cost of Equity)
Total value = debt + equity
Cost of debt = interest rate x (1-corporate tax rate)
Cost of Equity = risk-free rate + (beta x market risk premium)
"""
def calculate_wacc(settings:dict) -> float:



    try:



        #equity calculations
        market_value_equity = settings["outstanding_shares"] * settings["current_price"]

        #debt calculation
        total_value = market_value_equity + settings["total_debt"]

        # Weights
        weight_equity = market_value_equity / total_value
        weight_debt = settings["total_debt"] / total_value

        """
        Cost of equity 
        Using fixed values to simplify
        """
        beta = float(settings["Beta"].iloc[0])
        risk_free_rate = 0.05
        market_risk_premium = 0.06
        cost_of_equity = risk_free_rate + (market_risk_premium * beta)

        #Cost of Debt
        cost_of_debt = settings["interest_expense"] / settings["total_debt"] if settings["total_debt"] > 0 else 0.05

        #Tax rate
        tax_rate = settings["income_tax_expense"] / settings["ebit"] if settings["ebit"] > 0 else 0.25
        tax_rate = max(0, min(tax_rate, 0.25))
        #WACC
        wacc = (weight_debt * cost_of_debt * (1 - tax_rate)) + (weight_equity * cost_of_equity)

        return wacc
    except Exception as e:
        print(e)
        print(traceback.format_exc())




def calculate_dcf(settings : dict,forecast_years = 5,terminal_growth: float = 0.025):

    try:

        # Instead of pulling just row 0, average out the last 3 rows to smooth out anomalies





        fcf_growth = ((settings["market_fcf"] - settings["prior_fcf"]) / settings["prior_fcf"])

        # Get WACC
        wacc = calculate_wacc(settings)



        # Project FCFs and Present Values FCF's
        projected_fcfs = []
        pv_fcfs = []


        for year in range(1, forecast_years + 1):
            future_fcf = settings["market_fcf"] * ((1 + fcf_growth)**year)
            projected_fcfs.append(future_fcf)

            discounted_fcf = future_fcf / ((1 + wacc)**year)
            pv_fcfs.append(discounted_fcf)

        total_pv_fcfs = sum(pv_fcfs)

        #Terminal value
        terminal_fcf = projected_fcfs[-1] * (1 + terminal_growth)
        terminal_value = terminal_fcf / (wacc - terminal_growth)


        pv_terminal = terminal_value / ((1 + wacc) ** forecast_years)

        #Enterprise value
        enterprise_value = total_pv_fcfs + pv_terminal

        #Equity value (enterprise value - net debt)
        net_debt = settings["total_debt"] - settings["current_assets"]
        equity_value = enterprise_value - net_debt

        #DCF per share value
        if settings["market_fcf"] > 0:
            dcf_price_per_share = equity_value / settings["outstanding_shares"] if settings["outstanding_shares"] > 0 else 0
            upside_downside = ((dcf_price_per_share / settings["current_price"]) - 1) * 100 if settings["current_price"] > 0 else 0

        else:
            dcf_price_per_share = ("DCF not meaningful; company has negative free cash flow, likely due to heavy capital expenditure. "
                            "Consider using revenue multiples or comparable company analysis instead.")
            upside_downside = ("Upside downside not meaningful; company has negative free cash flow, likely due to heavy capital expenditure. "
                            "Consider using revenue multiples or comparable company analysis instead.")
        dcf_values = {
            "enterprise_value": enterprise_value,
            "equity_value": equity_value,
            "dcf_price_per_share": dcf_price_per_share,
            "upside_downside_pct": upside_downside,
            "total_pv_fcfs": [total_pv_fcfs],
            "pv_terminal": pv_terminal,
            "current_price": settings["current_price"],
            "fcf_growth": fcf_growth
        }
        return dcf_values

    except Exception as e:
        return {"error": str(e),
                "dcf_price_per_share": 0}

def format_amount(amount):


    minus = "-" if amount < 0 else ""
    absolute_amount = abs(amount)

    if absolute_amount >= 1_000_000_000_000:
        return f"{minus}${absolute_amount / 1_000_000_000_000:.1f} trillion"
    if absolute_amount >= 1_000_000_000:
        return f"{minus}${absolute_amount / 1_000_000_000:.1f} billion"
    if absolute_amount >= 1_000_000:
        return f"{minus}${absolute_amount / 1_000_000:.1f} million"
    if absolute_amount >= 1_000:
        return f"{minus}${absolute_amount / 1_000:.1f} thousand"
    return f"{minus}${absolute_amount}"

def calculate_all(balance_df : pd.DataFrame, price_df: pd.DataFrame, income_df : pd.DataFrame, cash_df : pd.DataFrame,company_overview : pd.DataFrame):

    try:
        settings = {
            "total_debt" : balance_df["total_debt"].iloc[0],
            "current_price" : price_df["Close"].iloc[-1],
            "income_tax_expense" : income_df["income_tax_expense"].iloc[0],
            "revenue" :income_df["revenue"].iloc[0],
            "interest_expense" : income_df["interest_expense"].iloc[0],
            "ebit" : income_df["operating_income"].iloc[0],
            "current_assets" : balance_df["current_assets"].iloc[0],
            "outstanding_shares" : balance_df["outstanding_shares"].iloc[0],
            "market_fcf" : cash_df["free_cash_flow"].iloc[0],
            "prior_fcf" : cash_df["free_cash_flow"].iloc[1],
            "operating_income" : income_df["operating_income"].iloc[0],
            "operating_outcome" : income_df["operating_outcome"].iloc[0],
            "operating_cash_flow" : cash_df["operating_cash_flow"].iloc[0],
            "Beta": company_overview["Beta"]
        }

        wacc = calculate_wacc(settings)

        dcf = calculate_dcf(settings,forecast_years = 5,terminal_growth= 0.025)

        market_cap = settings["outstanding_shares"] * settings["current_price"]
        if settings["market_fcf"] > 0:
            price_to_fcf = round((market_cap / settings["market_fcf"]),2)
        else :
            price_to_fcf = "Calculation for price/free cash flow not meaningful; company has negative free cash flow"
        if settings["operating_cash_flow"] > 0:
            price_to_ocf = round((market_cap / settings["operating_cash_flow"]),2)
        else :
            price_to_ocf = "Calculation for Price/Operating Cash Flow not meaningful; company has negative operating cash flow"

        operating_margin = settings["operating_income"] / settings["revenue"]
        revenue_cagr = ((income_df["revenue"].iloc[0] / income_df["revenue"].iloc[3]) ** (1/3)-1)
        equity = settings["outstanding_shares"] * settings["current_price"]
        debt_to_equity = settings["total_debt"] / equity
        fcf_growth = dcf["fcf_growth"]

        financials_display = {
            "Operating Margin": f"{operating_margin:.1%}",
            "Revenue CAGR": f"{revenue_cagr:.1%}",
            "Equity": format_amount(equity),
            "Debt/Equity": f"{debt_to_equity:.2f}x",
            "WACC": f"{wacc:.2%}",
            "Price/Free Cash Flow": f"{price_to_fcf}",
            "Price/Operating Cash Flow": f"{price_to_ocf}",
            "Free Cash Flow Growth": f"{fcf_growth:.1%}",
            "Year Prior Free Cash Flow": format_amount(settings["prior_fcf"]),
            "Current Free Cash Flow": format_amount(settings["market_fcf"]),
            "Market Cap": format_amount(market_cap),
            "Beta": f"{company_overview["Beta"].iloc[0]}",
            "P/E": f"{company_overview["P/E"].iloc[0]}x",
            "EPS": f"{company_overview["EPS"].iloc[0]}"
        }

        return financials_display,dcf

    except Exception as e:
        print(f"Error calculating fundamental ratios: {e}")



