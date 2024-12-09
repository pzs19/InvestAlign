import json
from utils.environment import P2alpha, rank2rho, rank2theta

def format_prompt_infer_seq(prompt_path, budget, refer_ratios, alpha_raw, rho_raw, theta_raw, T=10):
    refer_ratios_str = json.dumps([f"{r*100:.2f}%" for r in refer_ratios])
    alpha = P2alpha(alpha_raw)
    rho = rank2rho(rho_raw)
    theta = rank2theta(theta_raw)
    with open(prompt_path, 'r', encoding='utf-8') as f:
        prompt_template = f.read()
    prompt = prompt_template.replace("{T}", str(T))
    prompt = prompt.replace("{budget}", json.dumps(round(budget, 2)))
    prompt = prompt.replace("{refer_ratios}", json.dumps(refer_ratios_str))
    prompt = prompt.replace("{alpha_raw}", f"{alpha_raw*100:.2f}")
    prompt = prompt.replace("{rho_raw}", f"{rho_raw:d}")
    prompt = prompt.replace("{theta_raw}", f"{theta_raw:d}")
    prompt = prompt.replace("{alpha}", f"{alpha:.6f}")
    prompt = prompt.replace("{rho}", f"{rho:.6f}")
    prompt = prompt.replace("{theta}", f"{theta:.6f}")
    return prompt

def format_prompt_infer_delta_seq(prompt_path, budget, refer_ratios, invest_ratio_t0, alpha_raw, rho_raw, theta_raw, T=10):
    
    refer_ratios_str = json.dumps([f"{r*100:.2f}%" for r in refer_ratios])
    delta_refer_ratios = [refer_ratios[i+1] - refer_ratios[i] for i in range(len(refer_ratios)-1)]
    delta_refer_ratios_str = json.dumps([f"{r*100:.2f}%" for r in delta_refer_ratios])

    alpha = P2alpha(alpha_raw)
    rho = rank2rho(rho_raw)
    theta = rank2theta(theta_raw)
    with open(prompt_path, 'r', encoding='utf-8') as f:
        prompt_template = f.read()
    prompt = prompt_template.replace("{T}", str(T))
    prompt = prompt.replace("{budget}", json.dumps(round(budget, 2)))
    prompt = prompt.replace("{refer_ratios}", json.dumps(refer_ratios_str))
    prompt = prompt.replace("{delta_refer_ratios}", json.dumps(delta_refer_ratios_str))
    prompt = prompt.replace("{invest_ratio_t0}", f"{invest_ratio_t0*100:.2f}%")
    prompt = prompt.replace("{alpha_raw}", f"{alpha_raw*100:.2f}")
    prompt = prompt.replace("{rho_raw}", f"{rho_raw:d}")
    prompt = prompt.replace("{theta_raw}", f"{theta_raw:d}")
    prompt = prompt.replace("{alpha}", f"{alpha:.6f}")
    prompt = prompt.replace("{rho}", f"{rho:.6f}")
    prompt = prompt.replace("{theta}", f"{theta:.6f}")
    return prompt
