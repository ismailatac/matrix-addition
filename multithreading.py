import numpy as np
import multiprocessing as mp
import time
import matplotlib.pyplot as plt

def add_matrices(start, end, A, B, C,SIZE):
    for i in range(start, end):
        for j in range(SIZE):
            C[i][j] = A[i][j] + B[i][j]

if __name__ == '__main__':
    mp.freeze_support()

    sizes = [2000, 3000, 4000, 5000, 6000]

    
    num_processes_list = [1, 2, 3, 4]

    
    for SIZE in sizes:
        elapsed_times = []
        A = np.random.randint(0, 100, (SIZE, SIZE))
        B = np.random.randint(0, 100, (SIZE, SIZE))
        C = np.zeros((SIZE, SIZE))
        serial_start = time.time()
        add_matrices(0, SIZE, A, B, C,SIZE)
        serial_elapsed_time = time.time() - serial_start

        speedup_values = []
        efficiency_values = []
        for num_processes in num_processes_list:
            processes = []
            start_time = time.time()
            for i in range(num_processes):
                start = i * (SIZE // num_processes)
                end = (i+1) * (SIZE // num_processes)
                p = mp.Process(target=add_matrices, args=(start, end, A, B, C,SIZE))
                p.start()
                processes.append(p)

            for p in processes:
                p.join()

            elapsed_time = time.time() - start_time
            elapsed_times.append(elapsed_time)

            speedup = serial_elapsed_time / elapsed_time
            efficiency = speedup / num_processes

            speedup_values.append(speedup)
            efficiency_values.append(efficiency)

            print(f"Matris boyutu: {SIZE}, Çekirdek sayısı: {num_processes}, "
                f"Süre: {elapsed_time:.5f}, Speed-up: {speedup:.5f}, "
                f"Efficiency: {efficiency:.5f}")
            
      
        
        plt.plot(num_processes_list, efficiency_values, label=f'{SIZE}')
        print("---------------------------------------------------")

    plt.xlabel('Çekirdek Sayısı')
    plt.ylabel('Speedup')
    plt.legend()
    plt.show()
 
