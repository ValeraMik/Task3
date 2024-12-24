from concurrent.futures import ThreadPoolExecutor
import time
from threading import Lock

# Глобальні змінні для підрахунку
total_steps = 0
processed_numbers = 0
lock = Lock()  # Для безпечного оновлення глобальних змінних


def collatz_steps(n):
    """
    Обчислення кількості кроків для виродження числа n до 1 за гіпотезою Колаца.
    """
    steps = 0
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        steps += 1
    return steps


def process_number(n):
    """
    Обробляє одне число: обчислює кількість кроків і оновлює глобальні змінні.
    """
    global total_steps, processed_numbers
    steps = collatz_steps(n)
    
    # Оновлення глобальних змінних за допомогою Lock (atomic update)
    with lock:
        total_steps += steps
        processed_numbers += 1


def main():
    # Параметри
    total_numbers = 10_000_000  # Загальна кількість чисел
    num_threads = 8             # Кількість потоків (можна змінити)

    start_time = time.time()

    # Використання ThreadPoolExecutor для паралельного виконання
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Розподіл обробки чисел між потоками
        executor.map(process_number, range(1, total_numbers + 1))

    # Обчислення середньої кількості кроків
    average_steps = total_steps / processed_numbers
    print(f"Середня кількість кроків: {average_steps}")

    end_time = time.time()
    print(f"Час виконання: {end_time - start_time:.2f} секунд")


if __name__ == "__main__":
    main()
