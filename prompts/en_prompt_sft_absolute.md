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

- Your risk aversion coefficient (alpha) is: {alpha}, which means you consider the following two choices to be indifferent when the probability (i.e., P) is {alpha_raw}: A. With probability P, you can obtain $20, and with probability 1 - P, you can obtain $0; B. With 100% probability, you obtain $6. Note that as an investor, you have a certain level of optimism about "winning" and are willing to take on some risk, so you consider the two options equivalent at probability P={alpha_raw}, which is higher than the 30.00% in a completely rational scenario.

- Your convergence coefficient (theta) is: {theta}, which means "in decision-making, your level of dependence on the smart investment advisor is: {theta_raw} points. A score of 10 indicates a high level of dependence on the advisor, while a score of 0 indicates a low level of dependence.

## Output Format Requirements

Please output your decision in JSON format, including two parts: (1) Decision Explanation: Explain the reasons behind your investment proportion decisions. (2) Investment Proportion Sequence: The percentage sequence of funds allocated to the stock each year over the {T} years. You need to output a list containing {T} percentages, with each percentage ranging from 0% to 100% and precise to two decimal places, representing the investment proportion for each year t. For example:

{"Decision Explanation": "Briefly explain the reasons behind your investment proportion decisions.", "Investment Proportion Sequence": ["34.79%", "38.58%", "35.75%", "32.17%", "31.61%", "30.52%", "34.01%", "32.48%", "34.20%", "31.70%"]}

Here, ["34.79%", "38.58%", "35.75%", "32.17%", "31.61%", "30.52%", "34.01%", "32.48%", "34.20%", "31.70%"] is just an example. You need to replace this percentage list with your actual investment proportion sequence. Providing the investment proportion sequence is the most important; do not just focus on the explanation and forget to provide the investment proportion sequence!!!

## Question

Now, you have {budget} million dollars for investment and savings, and the smart investment advisor recommends the following investment proportions for the stock over the {T} years: {refer_ratios}. Considering historical investment situations and the advisor's recommendations, based on your own investment insights, what is your decided investment proportion sequence for the stock over these {T} years? (Please follow the previously provided JSON format requirements, and provide a list of {T} specific percentages indicating your investment proportion sequence for these {T} years, rather than giving investment recommendations or writing code.)

Answer:

# Output

According to optimal investment theory, in the above scenario, the optimal amount for investing in the stock, $P^*(t)$, equals the product of the smart investment advisor's investment amount (i.e., the advisor's decision proportion multiplied by the current budget) and a hyperbolic tangent function. The specific calculation is as follows:

$$
    P^*(t)=\frac{\eta\alpha_2\sigma^2\mathrm{e}^{2r(T-t)}+\theta}{\eta\alpha_1\sigma^2\mathrm{e}^{2r(T-t)}+\theta}\cdot \frac{v}{\alpha_2\sigma^2}\mathrm{e}^{r(t-T)},t\in\{1,2,...,10\},
$$
where:
- $r$ is the interest rate, which is 4%
- $\sigma$ is the volatility of the stock, which is 17%
- $v$ is the excess return of the stock, which is 3%
- $\alpha_1$ is my risk aversion coefficient: $\alpha_1={alpha}$
- $\alpha_2$ represents the risk aversion coefficient of the smart investment advisor: $\alpha_2=0.2$
- $\theta$ is my convergence coefficient: $\theta={theta}$
- The integral constant $\eta$ depends on $\theta$. In the current settings, $\eta={eta}$

Substituting the specific numbers, the proportion sequence of funds allocated to the stock is: {optimal_ratios}.

Note that I also need to output the investment proportion sequence in JSON format:

{"Decision Explanation": "Based on the optimal investment theory and substituting specific numbers, the investment proportion sequence for the stock is calculated.", "Investment Proportion Sequence": "{optimal_ratios}"}