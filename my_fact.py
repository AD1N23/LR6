import os
import time
import threading
import queue
import multiprocessing

from ferma_fact import fermat_factorization as py_fermat
from fermat_cython import fermat_factorization as c_fermat


class FactorizationManager:
    """
    Класс для управления многопоточной и многопроцессорной факторизацией.
    """
    def __init__(self, test_list, num_workers):
        self.test_list = test_list
        self.num_workers = num_workers
        self.tasks = None
        self.results = None

    def _worker(self, factorization_function):
        """Универсальная функция-воркер, которая будет запускаться в потоках/процессах."""
        while True:
            try:
                item = self.tasks.get(timeout=1)
                if item is None:
                    break
                factors = factorization_function(item)
                self.results.put((item, factors))
            except queue.Empty:
                continue

    def run_with_threads(self, factorization_function):
        """Запускает многопоточную факторизацию."""
        print(f"Запуск многопоточной факторизации с {factorization_function.__name__} на {self.num_workers} потоках...")
        self.tasks = queue.Queue()
        self.results = queue.Queue()

        start_time = time.time()
        
        threads = []
        for _ in range(self.num_workers):
            t = threading.Thread(target=self._worker, args=(factorization_function,))
            threads.append(t)
            t.start()
        
        for item in self.test_list:
            self.tasks.put(item)
        
        for _ in range(self.num_workers):
            self.tasks.put(None)
        
        for t in threads:
            t.join()
        
        return self._get_results(start_time)

    def run_with_processes(self, factorization_function):
        """Запускает многопроцессорную факторизацию."""
        print(f"Запуск многопроцессорной факторизации с {factorization_function.__name__} на {self.num_workers} процессах...")
        self.tasks = multiprocessing.Queue()
        self.results = multiprocessing.Queue()

        start_time = time.time()
        
        processes = []
        for _ in range(self.num_workers):
            p = multiprocessing.Process(target=self._worker, args=(factorization_function,))
            processes.append(p)
            p.start()
        
        for item in self.test_list:
            self.tasks.put(item)
        
        for _ in range(self.num_workers):
            self.tasks.put(None)
        
        for p in processes:
            p.join()
        
        return self._get_results(start_time)

    def _get_results(self, start_time):
        """Вспомогательный метод для сбора результатов и замера времени."""
        final_results = []
        while not self.results.empty():
            final_results.append(self.results.get())
        
        end_time = time.time()
        total_time = end_time - start_time
        
        self.print_summary(final_results, total_time)
        return total_time

    def print_summary(self, results, total_time):
        """Выводит результаты и время выполнения."""
        print("\nФакторизация завершена.")
        print("Результаты:")
        for res in results:
            original_number, factors = res
            print(f"Число: {original_number}, Множители: {factors}")
        print(f"\nОбщее время выполнения: {total_time:.4f} секунд.")
        


if __name__ == "__main__":
    TEST_LST = sorted([101, 9973, 104729, 101909, 609133, 1300039, 9999991, 99999959, 99999971, 3000009, 700000133, 61335395416403926747])
    NUM_WORKERS = os.cpu_count()

    manager = FactorizationManager(TEST_LST, NUM_WORKERS)

    # # Запуск с потоками и обычной Python-реализацией
    time_py_thr = manager.run_with_threads(py_fermat)
    
    # # Запуск с потоками и Cython-реализацией
    time_c_thr = manager.run_with_threads(c_fermat)

    # # Запуск с процессами и обычной Python-реализацией
    time_py_proc = manager.run_with_processes(py_fermat)
    # # Запуск с процессами и Cython-реализацией
    time_c_proc =  manager.run_with_processes(c_fermat)

    import matplotlib.pyplot as plt

    # Визуализация результатов
    plt.bar(
        ['Python + Threads', 'Python + Processes', 'Cython + Threads', 'Cython + Processes'],
        [time_py_thr, time_py_proc, time_c_thr, time_c_proc],
        color=['blue', 'orange', 'green', 'red'])
    plt.axhline(time_py_thr, color='black', linestyle='--')
    plt.axhline(time_py_proc, color='black', linestyle='--')
    plt.axhline()
    plt.title('Время выполнения факторизации')
    plt.xlabel("Сценарий")
    plt.ylabel("Время (секунды)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()
    input("Press Enter to exit...")