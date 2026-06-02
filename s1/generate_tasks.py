# generate_tasks.py  (run once from terminal: python generate_tasks.py)
import random, string, json

def generate_decryption_tasks(n=100, key_size=20, code_length=5, seed=42):
    rng = random.Random(seed)
    tasks = []
    alphabet = list(string.ascii_uppercase)
    for _ in range(n):
        shuffled = alphabet.copy()
        rng.shuffle(shuffled)
        key_letters = rng.sample(alphabet, key_size)
        key = {enc: shuffled[alphabet.index(enc)] for enc in key_letters}
        code = [rng.choice(key_letters) for _ in range(code_length)]
        answer = ''.join(key[c] for c in code)
        tasks.append({'key': key, 'code': ''.join(code), 'answer': answer})
    return tasks

tasks = generate_decryption_tasks()

with open('tasks.json', 'w') as f:
    json.dump(tasks, f, indent=2)

print(f"Saved {len(tasks)} tasks to tasks.json")
