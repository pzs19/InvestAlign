#!/bin/bash

python infer_seq_relative.py \
    --model-path meta-llama/Meta-Llama-3.1-8B-Instruct \
    --tp-size 4 \
    --save-dir results/Meta-Llama-3.1-8B-Instruct/exp_relative
python infer_seq_relative.py \
    --model-path Qwen/Qwen2-7B-Instruct \
    --tp-size 4 \
    --save-dir results/Qwen2-7B-Instruct/exp_relative
python infer_seq_relative.py \
    --model-path THUDM/glm-4-9b-chat \
    --tp-size 4 \
    --save-dir results/glm-4-9b-chat/exp_relative

export OPENAI_API_BASE=""
export OPENAI_API_KEY=""
python infer_seq_relative.py \
    --model-path openai/gpt-3.5-turbo-0125 \
    --save-dir results/gpt-3.5-turbo-0125/exp_relative