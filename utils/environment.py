
import numpy as np
from scipy.optimize import fsolve, approx_fprime
from scipy.integrate import quad, solve_bvp
from scipy.interpolate import interp1d

mu = 0.07  # 风险资产的收益率
r = 0.04  # 无风险资产的收益率
v = mu - r  # 风险资产的超额收益率
sigma = 0.17  # 风险资产的波动率
baralpha = 0.2  # “小秘”的风险厌恶系数（固定为0.2）
delta_eta = 1e6

def calculate_bar_P(T):
    global mu, r, v, sigma, baralpha
    t_list = np.arange(1, T + 1)
    bar_P = (mu - r) / (baralpha * sigma ** 2) * np.exp(r * (t_list - T))
    return bar_P

def update_budget(budget, invest, dW):
    return budget * (1 + r) + invest * (v + sigma * dW)

# 计算alpha的选项映射
def cal_alpha(x):
    if x == 18: return 0.499  # alpha=0.95
    elif x == 17: return 0.314  # alpha=0.85
    elif x == 16: return 0.225  # alpha=0.75
    elif x == 15: return 0.163  # alpha=0.65
    elif x == 14: return 0.113  # alpha=0.55
    elif x == 13: return 0.676  # alpha=0.45
    elif x == 12: return 0.023  # alpha=0.35

# 计算theta的选项映射（可调整）
def rank2theta(x):
    return x * 1e-8

# 计算theta的选项映射（可调整）
def theta2rank(x):
    return int(x / 1e-8)

# 计算rho的选项映射（可调整）
def rank2rho(x):
    return x * 0.5

# 计算rho的选项映射（可调整）
def rho2rank(x):
    return int(x / 0.5)

def get_optimal_decision(
        x: float, # initial budget
        T: int, # investment span
        alpha: float,
        theta: float,
        rho: float,
):
    global mu, r, v, sigma, baralpha, barP
    vartheta = theta / (alpha * sigma ** 2)  # 计算用辅助变量
    varrho = 2 - rho  # 计算用辅助变量

    # "小秘"的决策函数
    barP = lambda t: v / (baralpha * sigma ** 2) * np.exp(r * (t - T))  # “小秘”的决策函数
    # 下面是计算用户最优决策函数的过程
    eta_0 = np.exp(-alpha * x * np.exp(r * T) - v ** 2 * T / (2 * sigma ** 2))
    eta = eta_0
    delta_eta = 1e6
    while delta_eta > 1e-10:
        int_func = lambda t: vartheta ** 2 * v ** 2 * (alpha / baralpha - 1) ** 2 / 2 * sigma ** 2 * (eta * np.exp(varrho * r * (T - t)) + vartheta) ** 2
        eta_ = eta_0 * np.exp(quad(int_func, 0, T)[0])
        delta_eta = np.abs(eta_ - eta)
        eta = eta_
    P = lambda t: (eta * baralpha * sigma ** 2 * np.exp(varrho * r * (T - t)) + theta) / (eta * alpha * sigma ** 2 * np.exp(varrho * r * (T - t)) + theta) * barP(t)
    t_list = np.arange(0, T)
    barP_value = barP(t_list)  # “小秘”的最优决策序列
    P_value = P(t_list)  # 用户的最优决策序列

    return barP_value, P_value

def alpha2P(alpha, 
            *,
            win = 10, 
            lose = 0, 
            timid = 3):
    
    P = (np.exp(-alpha * timid) - np.exp(-alpha * lose)) / (np.exp(-alpha * win) - np.exp(-alpha * lose))
    return P

def P2alpha(P, win=10, lose=0, timid=3):
    # 定义一个方程，左边是函数 alpha2P，右边是已知的 P
    equation = lambda alpha: alpha2P(alpha, win=win, lose=lose, timid=timid) - P
    # 使用 fsolve 来求解 alpha
    alpha_initial_guess = 0.1  # 初始猜测值，可以根据实际情况调整
    alpha_solution, = fsolve(equation, alpha_initial_guess)
    return alpha_solution

def object_func(x_T, P, hatP, alpha, theta, rho, r=0.04, T=10):
    func = -1 / alpha * np.exp(-alpha * x_T) \
         - theta / 2 * np.sum([np.exp(rho * r * (T - u)) * (P[u] - hatP[u]) ** 2 for u in range(10)]) * T / 10
    return func

def obj_func_absolute(P_list, alpha, theta, alpha2=baralpha, r=r, v=v, sigma=sigma, x0=10, T=10):
    assert len(P_list) == 10, "invalid length P_list"
    P_list = np.array(P_list)
    Q = lambda t: v / (alpha2 * sigma ** 2) * np.exp(r * (t - T))
    Ephi = -1 / alpha * np.exp(-alpha * x0 * np.exp(r * T) - alpha * v * np.sum(r * (T - 1 - np.arange(T)) * P_list) \
         + alpha ** 2 * sigma ** 2 / 2 * np.sum(2 * r * (T - 1 - np.arange(T)) * P_list ** 2))
    AD = theta / 2 * np.sum((P_list - Q(np.arange(T))) ** 2)
    return Ephi - AD

def obj_func_relative(P_list, alpha, theta, alpha2=baralpha, r=r, v=v, sigma=sigma, x0=10, T=10):
    assert len(P_list) == 10, "invalid length P_list"
    P_list = np.array(P_list)
    Q = lambda t: v / (alpha2 * sigma ** 2) * np.exp(r * (t - T))
    Ephi = -1 / alpha * np.exp(-alpha * x0 * np.exp(r * T) - alpha * v * np.sum(r * (T - 1 - np.arange(T)) * P_list) \
         + alpha ** 2 * sigma ** 2 / 2 * np.sum(2 * r * (T - 1 - np.arange(T)) * P_list ** 2))
    AD = theta / 2 * np.sum((np.diff(P_list) - np.diff(Q(np.arange(T)))) ** 2)
    return Ephi - AD

def optimal_obj_func_absolute(alpha, theta, alpha2=baralpha, r=r, v=v, sigma=sigma, x0=10, T=10):
    vartheta = theta / (alpha * sigma ** 2)
    varrho = 2
    barP = lambda t: v / (alpha2 * sigma ** 2) * np.exp(r * (t - T))
    eta_0 = np.exp(-alpha * x0 * np.exp(r * T) - v ** 2 * T / (2 * sigma ** 2))
    eta = eta_0
    delta_eta = 1e6
    while delta_eta > 1e-10:
        int_func = lambda t: vartheta ** 2 * v ** 2 * (alpha / alpha2 - 1) ** 2 / 2 * sigma ** 2 * (eta * np.exp(varrho * r * (T - t)) + vartheta) ** 2
        eta_ = eta_0 * np.exp(quad(int_func, 0, T)[0])
        delta_eta = np.abs(eta_ - eta)
        eta = eta_
    P = lambda t: (eta * alpha2 * sigma ** 2 * np.exp(varrho * r * (T - t)) + theta) / (eta * alpha * sigma ** 2 * np.exp(varrho * r * (T - t)) + theta) * barP(t)
    int_func1 = lambda t: np.exp(r * (T - t)) * P(t)
    int_func2 = lambda t: int_func1(t) ** 2
    int_func3 = lambda t: (P(t) - barP(t)) ** 2
    int1 = quad(int_func1, 0, T)[0]
    int2 = quad(int_func2, 0, T)[0]
    int3 = quad(int_func3, 0, T)[0]
    return -1 / alpha * np.exp(-alpha * x0 * np.exp(r * T) - alpha * v * int1 + alpha ** 2 * sigma ** 2 / 2 * int2) - theta / 2 * int3

def optimal_obj_func_relative(alpha, theta, alpha2=baralpha, r=r, v=v, sigma=sigma, x0=10, T=10):
    barP = lambda t: v / (alpha2 * sigma ** 2) * np.exp(r * (t - T))
    num_point = 1000
    eta = 1
    zeta = sigma * np.exp(r * T) / r * np.sqrt(eta * alpha / theta)
    c1 = r ** 2 * v * np.exp(-r * T) / (alpha2 * sigma ** 2)
    for _ in range(1000):
        c2 = -eta * v * np.exp(r * T) / theta
        def fun(t, y):
            return np.vstack((y[1], y[0] * r ** 2 * zeta ** 2 * np.exp(-2 * r * t) + c1 * np.exp(r * t) + c2 * np.exp(-r * t)))
        def bc(ya, yb):
            return np.array([ya[0] - v / (alpha * sigma ** 2) * np.exp(-r * T), yb[0] - v / (alpha * sigma ** 2)])
        x = np.linspace(0, T, num_point)
        y = np.zeros((2, x.size))
        res = solve_bvp(fun, bc, x, y)
        eta_ = np.exp(-alpha * x0 * np.exp(r * T) \
                     - alpha * v * np.sum(res.y[0] * np.exp(r * (T - x))) * T / num_point \
                     + alpha ** 2 * sigma ** 2 / 2 * np.sum(res.y[0] ** 2 * np.exp(2 * r * (T - x))) * T / num_point)
        zeta_ = sigma * np.exp(r * T) / r * np.sqrt(eta_ * alpha / theta)
        delta_eta, delta_zeta = np.abs(eta_ - eta), np.abs(zeta_ - zeta)
        eta, zeta = eta_, zeta_
        if max(delta_eta, delta_zeta) < 1e-10:
            break
    P = interp1d(np.linspace(0, 10, num_point), res.y[0], kind='linear')
    int_func1 = lambda t: np.exp(r * (T - t)) * P(t)
    int_func2 = lambda t: int_func1(t) ** 2
    int_func3 = lambda t: (approx_fprime(t, P, 1e-4) - approx_fprime(t, barP, 1e-4)) ** 2
    int1 = quad(int_func1, 0, T)[0]
    int2 = quad(int_func2, 0, T)[0]
    int3 = quad(int_func3, 0, T)[0]
    return -1 / alpha * np.exp(-alpha * x0 * np.exp(r * T) - alpha * v * int1 + alpha ** 2 * sigma ** 2 / 2 * int2) - theta / 2 * int3
