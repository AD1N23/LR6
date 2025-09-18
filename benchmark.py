import time
import matplotlib.pyplot as plt

from ferma_fact import fermat_factorization as py_fermat
from fermat_cython import fermat_factorization as c_fermat

TEST_LST = sorted([101, 9973, 104729, 101909, 609133, 1300039, 9999991, 99999959, 99999971, 3000009, 700000133, 61335395416403926747])

def measure_time(func, numbers):
    times = []
    for num in numbers:
        start_time = time.time()
        func(num)
        end_time = time.time()
        times.append(end_time - start_time)
    return times

if __name__ == '__main__':
    print("Замеряем производительность Python-версии...")
    python_times = measure_time(py_fermat, TEST_LST)

    print("Замеряем производительность Cython-версии...")
    cython_times = measure_time(c_fermat, TEST_LST)

    print("Построение графика...")

    # Создаем график
    plt.figure(figsize=(10, 6))
    plt.plot(TEST_LST, python_times, 'o-', label='Python')
    plt.plot(TEST_LST, cython_times, 'o-', label='Cython')

    # Настраиваем оси и заголовок
    plt.xscale('log') 
    plt.xlabel('Число для факторизации (логарифмическая шкала)')
    plt.ylabel('Время выполнения (секунды)')
    plt.title('Сравнение производительности: Python vs. Cython (Метод Ферма)')
    plt.legend()
    plt.grid(True)


    plt.show()

    input("Нажмите Enter для выхода...")