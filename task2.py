import json
import time
from hyperloglog import HyperLogLog


LOG_FILE = "lms-stage-access.log"


def load_ips(filename):
    """Зчитування IP-адрес із лог-файлу."""
    ips = []

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            try:
                record = json.loads(line)
                ip = record.get("remote_addr")

                if ip:
                    ips.append(ip)

            except json.JSONDecodeError:
                continue

    return ips


def exact_count(ips):
    """Точний підрахунок."""
    return len(set(ips))


def hyperloglog_count(ips):
    """Наближений підрахунок."""
    hll = HyperLogLog(0.01)

    for ip in ips:
        hll.add(ip)

    return len(hll)


if __name__ == "__main__":

    ips = load_ips(LOG_FILE)

    start = time.perf_counter()
    exact = exact_count(ips)
    exact_time = time.perf_counter() - start

    start = time.perf_counter()
    approx = hyperloglog_count(ips)
    approx_time = time.perf_counter() - start

    print("=" * 65)
    print("Порівняння продуктивності")
    print("=" * 65)

    print(f"{'Метод':25}{'Унікальні':15}{'Час (сек.)'}")
    print("-" * 65)

    print(f"{'Точний (set)':25}{exact:<15}{exact_time:.6f}")
    print(f"{'HyperLogLog':25}{approx:<15}{approx_time:.6f}")
    