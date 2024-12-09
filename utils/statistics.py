import os
import numpy as np
import pandas as pd

def get_refers(T, save_dir="results/statistics"):
    def calculate_bar_P(mu, r, sigma, T):
        t_list = np.arange(1, T + 1)
        bar_P = (mu - r) / (0.2 * sigma ** 2) * np.exp(r * (t_list - T))
        return bar_P

    mu = 0.00292
    r = 0.00125
    sigma = 0.00708
    bar_P_values = calculate_bar_P(mu, r, sigma, T)
    np.savetxt(os.path.join(save_dir, 'file_1_barP.csv'), np.column_stack((np.arange(1, T + 1), bar_P_values)), header=r't, barP(t)', delimiter=',', comments='')
    return bar_P_values

def get_budgets(T_int, num_simulation=1000, save_dir="results/statistics"):
    def generate_gbm(mu, sigma, T, S0):
        T = np.array(T)
        dt = 1
        n = len(T)
        Z = np.random.standard_normal(n)
        W = np.cumsum(np.sqrt(dt) * Z)
        S = S0 * np.exp((mu - 0.5 * sigma**2) * T + sigma * W)
        return S

    mu = 0.00292
    sigma = 0.00708
    S0 = 1
    T = np.arange(T_int)

    gbm_matrix = np.zeros((len(T), num_simulation))
    for i in range(num_simulation):
        gbm_matrix[:, i] = generate_gbm(mu, sigma, T, S0)
    
    time_index = np.arange(len(T)).reshape(-1, 1)
    gbm_matrix_with_time = np.hstack((time_index, gbm_matrix))
    column_names = ['t'] + [f'S_{i}(t)' for i in range(num_simulation)]
    df = pd.DataFrame(gbm_matrix_with_time, columns=column_names)
    df.to_csv(os.path.join(save_dir, 'file_2_price.csv'), index=False)

    return gbm_matrix

def get_budgets_static():
    budgets = [10.00, 10.59, 11.22, 11.89, 12.60, 13.35, 14.15, 15.01, 15.91, 16.88]
    return budgets

def get_refers_static():
    refers = [36.21, 35.59, 34.96, 34.35, 33.73, 33.13, 32.53, 31.93, 31.34, 30.75]
    return refers