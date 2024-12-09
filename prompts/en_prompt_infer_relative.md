## Task Description

### Background

Assume you are an investment expert. Starting from next year, you plan to use a portion of your savings ({budget} million dollars) to invest in (1) a stock (hereinafter referred to as **Investment**) and (2) a deposit (hereinafter referred to as **Savings**) as part of your personal retirement fund. You will establish a dedicated account to manage this retirement fund. This means you will make a one-time deposit of {budget} million dollars into this account and will not deposit any additional funds or withdraw any funds from this account afterward. Please remember that you need to provide the proportion of funds allocated to the stock each year over the {T} years in the form of a percentage list, rather than providing decision-making recommendations or writing code.

### Your Investment Characteristics

1. **Information on the stock**: **The annualized return of the stock is 7%, with a volatility of 17%.**
An annualized return of 7% means that if you invest $100 in this stock, you can expect to have $107 after one year on average (the original $100 plus $7 in return).
A volatility of 17% indicates that:
- With a 68% probability: The asset price will be between $100 ± $17 (i.e., $83 to $117) after one year.
- With a 95% probability: The asset price will be between $100 ± 2 × $17 (i.e., $66 to $134) after one year.
- With a 99.7% probability: The asset price will be between $100 ± 3 × $17 (i.e., $49 to $151) after one year.

2. **Information on the deposit**: **The annualized return of the deposit is 4%.**
If you invest $100 in the deposit, you will receive $104 after one year (the original $100 plus $4 in return).

### Investment Period and Smart Investment Advisor

Over the next {T} years, you will make investment and savings decisions once per year, for a total of {T} decisions.
These {T} decision points are labeled 1, 2, ..., {T}.
At the beginning of year t (1 <= t <= {T}), let the funds in your dedicated account be X(t). Your decision is to allocate part of these funds to invest in the stock, denoted as P(t); the remaining funds will be allocated to savings, which will be X(t) - P(t). **You will determine the proportion of funds to allocate to the stock.**

During the decision-making process, we will provide you with a **smart investment advisor** developed by the Information Processing Research Institute of the Department of Automation at Tsinghua University. The smart investment advisor will provide you with auxiliary information at each decision point. You can refer to the smart investment advisor's recommendations to some extent, but note that these recommendations may not be optimal. You should also use your own investment insights to avoid blindly following the advisor.

### Task Objective

**Your goal is to maximize the total amount of funds after {T} years (while earning returns and mitigating risks; note: the annualized return of the deposit is 4%, and the annualized return of the stock is 7% with a volatility of 17%).**

## Your Investment Characteristics

As an investment expert, you have the following characteristics:

- Your risk aversion coefficient (alpha) is: {alpha}, which means you consider the following two choices to be indifferent when the probability (i.e., P) is {alpha_raw}: A. With probability P, you can obtain $20, and with probability 1 - P, you can obtain $0; B. With 100% probability, you obtain $6. Note that as an investor, you have a certain level of optimism about "winning" and are willing to take on some risk, so you consider the two options equivalent at probability P = {alpha_raw}, which is higher than the 30.00% in a completely rational scenario.

- Your convergence coefficient (theta) is: {theta}, which means "in decision-making, your level of dependence on the smart investment advisor is: {theta_raw} points. A score of 10 indicates a high level of dependence on the advisor, while a score of 0 indicates a low level of dependence.

## Output Format Requirements

Please output your decision in JSON format, including two parts: (1) Decision Explanation: Explain the reasoning behind your investment proportion decisions. (2) Investment Proportion Change Sequence: The sequence of **changes** in the percentage of funds allocated to the stock each year over the {T} years. You need to output a list containing {T-1} percentages, where each percentage represents the change in the investment proportion from year t-1 to year t, ranging from -100% to 100%. Positive values indicate an increase in investment, while negative values indicate a decrease. For example:

{"Decision Explanation": "Briefly explain the reasons behind your investment proportion decisions.", "Investment Proportion Change Sequence": ["3.88%", "0.01%", "-4.13%", "1.37%", "-1.37%", "-2.79%", "-2.56%", "2.02%", "-0.06%"]}

Here, ["3.88%", "0.01%", "-4.13%", "1.37%", "-1.37%", "-2.79%", "-2.56%", "2.02%", "-0.06%"] is just an example. You need to replace this percentage list with your actual investment proportion change sequence. Providing the investment proportion change sequence is crucial; do not just focus on the explanation and forget to include the investment proportion change sequence!!!

## Initial Investment Situation

In the first year, the proportion of funds allocated to the stock was: {invest_ratio_t0}.

## Question

You have {budget} million dollars for investment and savings, and the smart investment advisor recommends the following annual changes in the investment proportion for the stock over the {T} years: {refer_ratios}, the sequence of changes in investment proportion is {delta_refer_ratios}. Considering the initial investment situation and the advisor's recommendations, based on your own investment insights, what is your decided annual change sequence for the investment proportion in the stock over these {T} years? (Please follow the previously provided JSON format requirements, and provide a list of {T-1} specific percentages indicating the changes in your investment proportion over these {T} years, rather than giving investment recommendations or writing code.)

Answer: