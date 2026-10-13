import argparse
import time

import requests


def measure_speed(url: str) -> None:
    total_bytes = 0
    total_time = 0

    for number in range(1, 11):
        downloaded_bytes = 0
        start = time.perf_counter()

        try:
            with requests.get(url, stream=True, timeout=30) as response:
                response.raise_for_status()

                for chunk in response.iter_content(chunk_size=8192):
                    downloaded_bytes += len(chunk)

        except requests.RequestException as error:
            print(f"Ошибка запроса {number}: {error}")
            return

        elapsed = time.perf_counter() - start
        total_bytes += downloaded_bytes
        total_time += elapsed

        print(f"Запрос {number}: {elapsed:.2f} с")

        if number < 10:
            time.sleep(1)

    average_time = total_time / 10
    total_mb = total_bytes / (1024 * 1024)
    speed = total_mb / total_time if total_time else 0

    print(f"\nСреднее время запроса: {average_time:.2f} с")
    print(f"Общий объем скачанных данных: {total_mb:.2f} МБ")
    print(f"Средняя скорость: {speed:.2f} МБ/с")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Замер скорости интернета")
    parser.add_argument("url", help="Ссылка на файл")

    args = parser.parse_args()
    measure_speed(args.url)
