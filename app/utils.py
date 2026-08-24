import random
import string

#de mutat in utils.py *cand se atinge limita k2 trece la k3
def genereaza_cod_urmarire() -> str:

    part1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))

    part2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=2))

    return f"RPR-{part1}-{part2}"