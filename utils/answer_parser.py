import re
import json

def extract_invest_ratio_seq(text, key="Investment Proportion"):

    json_substrings = []
    stack = []
    start_idx = None

    for i, char in enumerate(text):
        if char == '{':
            if not stack:
                start_idx = i
            stack.append(char)
        elif char == '}':
            if stack:
                stack.pop()
                if not stack:
                    json_str = text[start_idx:i+1]
                    json_substrings.append(json_str)

    for candidate in json_substrings:
        try:
            candidate_cleaned = re.sub(r'\$\$(.*?)\$\$', '', candidate, flags=re.DOTALL).replace("\n", " ").replace("”", "\"").replace("“", "\"")
            json_obj = json.loads(candidate_cleaned)
            ans = json_obj[key]
            if isinstance(ans, list):
                seq = ans
            elif isinstance(ans, str):
                try:
                    seq = json.loads(ans)
                except Exception as e:
                    print(e)
                    try:
                        seq = ans.strip("[]").split(", ")
                    except Exception as e:
                        print(e)
                        continue
            try:
                ratios = []
                for r in seq:
                    if isinstance(r, float):
                        r /= 100
                    elif isinstance(r, str):
                        r = float(r.strip().replace("\n", "").strip("\"").strip("'").strip("%"))
                        r /= 100
                    ratios.append(r)
                return ratios
            except Exception as e:
                print(e)
                continue
        except Exception as e:
            print(e)
            continue
    return None