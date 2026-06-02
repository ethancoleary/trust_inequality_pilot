import random
import string

def generate_decryption_tasks(n=100, key_size=20, code_length=5, seed=42):
    """
    Generate a fixed list of decryption tasks.
    Each task has:
      - 'key': dict mapping 20 encrypted letters -> plaintext letters
      - 'code': 5 encrypted letters (the puzzle)
      - 'answer': the correct plaintext decryption
    """
    rng = random.Random(seed)
    tasks = []
    alphabet = list(string.ascii_uppercase)

    for _ in range(n):
        shuffled = alphabet.copy()
        rng.shuffle(shuffled)
        # Pick key_size letters as the cipher alphabet subset shown to the user
        key_letters = rng.sample(alphabet, key_size)
        key = {enc: shuffled[alphabet.index(enc)] for enc in key_letters}

        # The code uses only letters present in the key
        code = [rng.choice(key_letters) for _ in range(code_length)]
        answer = ''.join(key[c] for c in code)

        tasks.append({
            'key': key,
            'code': ''.join(code),
            'answer': answer,
        })

    return tasks
