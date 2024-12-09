from transformers import AutoTokenizer
import json
import os
from vllm import LLM, SamplingParams
from openai import OpenAI

class OpenSourceLLM:
    def __init__(self, model_path="", system_prompt = "", tp_size=1):
        self.model = LLM(model_path, trust_remote_code=True, tensor_parallel_size=tp_size)
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        self.n_max_token = json.load(open(f"{model_path}/config.json", "r"))["max_position_embeddings" if "glm-4" not in os.path.basename(model_path) else "seq_length"]
        self.system_prompt = system_prompt

    def __call__(self, 
        prompt: str, 
        n_max_new_token: int=1024, 
        seed: int=42, 
        temperature: int=0.9,
        top_p: int=1.0,
    ) -> str:
        sampling_params = SamplingParams(temperature=temperature, top_p=top_p, max_tokens=n_max_new_token, seed=seed)
        prompt = "\n\n".join([self.system_prompt, prompt])
        outputs = self.model.generate(prompt, sampling_params)
        return outputs[0].outputs[0].text

class OpenAILLM:
    def __init__(self, model_name="gpt-35-turbo"):

        self.model_name = model_name
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_BASE"),
        )

    def __call__(self, 
        prompt: str, 
        n_max_new_token: int=1024, 
        seed: int=42, 
        temperature: int=0.9,
        top_p: int=1.0,
    ) -> str:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "user", "content": prompt},
            ],
            seed=seed,
            max_tokens=n_max_new_token,
            temperature=temperature,
            top_p=top_p,
        )
        return response.choices[0].message.content
