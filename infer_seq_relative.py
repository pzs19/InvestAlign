import argparse
import os
import json
import numpy as np
from collections import defaultdict
from utils.llmwraper import OpenSourceLLM, OpenAILLM
from utils.prompt_formatter import format_prompt_infer_seq, format_prompt_infer_delta_seq
from utils.environment import update_budget, rank2rho, rank2theta, get_optimal_decision, P2alpha
from utils.answer_parser import extract_invest_ratio_seq

def main(args):
    save_dir = args.save_dir
    os.makedirs(args.save_dir, exist_ok=True)
    epoch_dir = os.path.join(save_dir, "epochs")
    os.makedirs(epoch_dir, exist_ok=True)

    if "openai" in args.model_path:
        llm = OpenAILLM(model_name=os.path.basename(args.model_path))
    else:
        llm = OpenSourceLLM(model_path=args.model_path, tp_size=args.tp_size)
    
    refer_ratios = [36.21, 35.59, 34.96, 34.35, 33.73, 33.13, 32.53, 31.93, 31.34, 30.75]
    refer_ratios = [r/100 for r in refer_ratios]
    delta_refer_ratios = [refer_ratios[i+1] - refer_ratios[i] for i in range(len(refer_ratios)-1)]
    alpha_list = [0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    rho = 0
    theta_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    seed_list = [37, 42, 71, 99, 100, 500, 1000, 1500, 2000, 2024]

    num_total_exp = len(alpha_list) * len(theta_list) * len(seed_list)
    results = []
    flags = []
    for alpha in alpha_list:
        for theta in theta_list:
            for seed in seed_list:
                save_fname = f"result_alpha{alpha}_theta{theta}_seed{seed}.json"
                if os.path.exists(os.path.join(epoch_dir, save_fname)):
                    res = json.load(open(os.path.join(epoch_dir, save_fname), "r", encoding="utf-8"))   
                    results.append(res)
                    flags.append(res['valid'])
                    print(f'load result from {os.path.join(epoch_dir, save_fname)}')
                    print(f"process: {len(flags)} / {num_total_exp}, valid: {sum(flags)} / {len(flags)}")
                    continue

                dW = np.random.normal(size=args.total_step)
                res = defaultdict(dict)
                res["alpha_raw"] = alpha
                res["rho_raw"] = rho
                res["theta_raw"] = theta
                res["alpha"] = P2alpha(alpha)
                res["rho"] = rank2rho(rho)
                res["theta"] = rank2theta(theta)
                res["valid"] = True
                invests = []
                budget = args.initial_budget
                budgets = [budget]

                prompt = format_prompt_infer_seq(args.prompt_path, budget, refer_ratios, alpha, rho, theta, T=args.total_step)
                output = llm(prompt, seed=seed, n_max_new_token=1024)
                pred_ratios = extract_invest_ratio_seq(output, key="Investment Proportion Sequence")
                if pred_ratios is None:
                    pred_ratios = refer_ratios[:]
                if len(pred_ratios) > args.total_step:
                    pred_ratios = pred_ratios[:args.total_step]
                elif len(pred_ratios) < args.total_step:
                    pred_ratios += refer_ratios[len(pred_ratios):]

                ratio_t0 = pred_ratios[0]
                invest_t0 = ratio_t0 * budget
                budget_t0 = update_budget(budget, invest_t0, dW[0])
                prompt = format_prompt_infer_delta_seq(args.delta_prompt_path, budget_t0, refer_ratios, ratio_t0, alpha, rho, theta, T=args.total_step)
                output = llm(prompt, seed=seed, n_max_new_token=1024)
                delta_pred_ratios = extract_invest_ratio_seq(output, key="Investment Proportion Change Sequence")
                res["output"] = output
                res["valid"] = (delta_pred_ratios is not None)
                if delta_pred_ratios is None:
                    delta_pred_ratios = delta_refer_ratios[:]
                if len(delta_pred_ratios) > args.total_step-1:
                    delta_pred_ratios = delta_pred_ratios[:args.total_step-1]
                elif len(delta_pred_ratios) < args.total_step-1:
                    delta_pred_ratios += delta_refer_ratios[len(delta_pred_ratios):]

                pred_ratios = [ratio_t0]
                for delta_ratio in delta_pred_ratios:
                    pred_ratios.append(pred_ratios[-1] + delta_ratio)

                for t, ratio in enumerate(pred_ratios):
                    invest = ratio * budget
                    invests.append(invest)

                    budget = update_budget(budget, invest, dW[t])
                    budgets.append(round(budget, 6))
                
                res["invests"] = invests
                res["ratios"] = pred_ratios
                res["delta_ratios"] = delta_pred_ratios
                res["budgets"] = budgets

                _, optimal_invests = get_optimal_decision(
                    args.initial_budget,
                    args.total_step,
                    alpha=res["alpha"], 
                    theta=res["theta"],
                    rho=res["rho"],
                )
                res["optimal_invests"] = optimal_invests.tolist()
                budget = args.initial_budget
                res["optimal_budgets"] = [budget]
                for t, invest in enumerate(optimal_invests):
                    budget = update_budget(budget, invest, dW[t])
                    res["optimal_budgets"].append(budget)

                flags.append(res['valid'])
                results.append(res)
                json.dump(res, open(os.path.join(epoch_dir, save_fname), "w", encoding="utf-8"), ensure_ascii=False, indent=4)
                
                print(f"process: {len(flags)} / {num_total_exp}, valid: {sum(flags)} / {len(flags)}")
                if args.verbose:
                    print(f"Answer: {res['output']}")
                    print(f"Invest Ratios: {res['ratios']}")

    with open(os.path.join(save_dir, "result_all.jsonl"), "w", encoding="utf-8") as f:
        f.writelines([json.dumps(_, ensure_ascii=False) + "\n" for _ in results])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--total-step', type=int, default=10,
    )
    parser.add_argument(
        '--num-simulation', type=int, default=200,
    )
    parser.add_argument(
        '--model-path', type=str, required=True,
    )
    parser.add_argument(
        '--prompt-path', type=str, default="prompts/en_prompt_infer_absolute.md",
    )
    parser.add_argument(
        '--delta-prompt-path', type=str, default="prompts/en_prompt_infer_relative.md",
    )
    parser.add_argument(
        '--save-dir', type=str, default="results/exp",
    )
    parser.add_argument(
        '--initial-budget', type=int, default=10,
    )
    parser.add_argument(
        '--tp-size', type=int, default=1,
    )
    parser.add_argument(
        '--verbose', action=argparse.BooleanOptionalAction, default=False
    )
    args = parser.parse_args()
    main(args)