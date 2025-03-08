import os
import sys
import random
import time
import matplotlib.pyplot as plt

def log_message(message):
    with open("log.txt", "a") as log_file:
        log_file.write(message)

def simulate_experiment(num_prisoners):
    # Generate random permutation
    permutation = list(range(num_prisoners))
    random.shuffle(permutation)
    
    boxes_per_prisoner = max(1, num_prisoners / 2)
    
    # Determine the outcome by checking the lengths of cycles in the permutation.
    visited = [False] * num_prisoners
    for i in range(num_prisoners):
        if not visited[i]:
            cycle_length = 0
            j = i
            while not visited[j]:
                visited[j] = True
                j = permutation[j]
                cycle_length += 1
            if cycle_length > boxes_per_prisoner:
                return permutation, False
    return permutation, True

def run_experiments(num_prisoners, num_experiments):
    start_time = time.time()
    success_count = 0

    for i in range(num_experiments):
        permutation, success = simulate_experiment(num_prisoners)
        if success:
            success_count += 1
        result_str = "success" if success else "fail"
        log_message(f"Experiment {i+1}: Permutation: {permutation} | Result: {result_str}\n")

    avg_success_rate = success_count / num_experiments
    print(f"After {num_experiments} experiments with {num_prisoners} prisoners:")
    print(f"Average success rate: {avg_success_rate:.4f}")
    elapsed_time = time.time() - start_time
    print(f"Execution time: {elapsed_time:.6f} seconds. ")

def test_experiments():
    print("Use Ctrl+C to stop the execution time test. ")
    num_prisoners = 10
    while True:
        start_time = time.time()
        _, _ = simulate_experiment(num_prisoners)
        elapsed_time = time.time() - start_time
        print(f"Number of prisoners: {num_prisoners} -> Experiment execution time: {elapsed_time:.6f} seconds. ")
        num_prisoners *= 10

def plot_experiments(start_num, end_num, experiment_times):
    start_time = time.time()
    prisoner_counts = []
    success_rates = []
    
    for num in range(start_num, end_num + 1, 2):
        success_count = 0
        for _ in range(experiment_times):
            _, success = simulate_experiment(num)
            if success:
                success_count += 1
        rate = success_count / experiment_times
        prisoner_counts.append(num)
        success_rates.append(rate)
        print(f"Prisoners: {num}, Success Rate: {rate:.4f}")
        log_message(f"Plot: Prisoners: {num} -> Success Rate: {rate:.4f}\n")

    plt.figure(figsize=(10, 6))
    plt.plot(prisoner_counts, success_rates, marker='o', linestyle='-', color='b')
    plt.title("100 Prisoner Problem: Success Rate vs Number of Prisoners")
    plt.xlabel("Number of Prisoners")
    plt.ylabel("Success Rate")
    plt.grid(True)
    plt.xlim(start_num, end_num)
    
    plt.savefig("plot.png")
    print("Plot saved as plot.png.")
    elapsed_time = time.time() - start_time
    print(f"Execution time: {elapsed_time:.6f} seconds. ")

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py [test|run|plot] [arguments]")
        return

    command = sys.argv[1].lower()

    if command == "test":
        try:
            test_experiments()
        except KeyboardInterrupt:
            print("\nTest stopped.")

    elif command == "run":
        try:
            if len(sys.argv) == 4:
                num_prisoners = int(sys.argv[2])
                num_experiments = int(sys.argv[3])
            else:
                print("Usage: python main.py run <prisoner number> <experiment times>")
        except ValueError:
            print("Invalid input for number of prisoners or experiments.")
            return

        # Check if number of prisoners is even and at least 2
        if num_prisoners < 2 or num_prisoners % 2 != 0:
            print("Error: Only even numbers (>=2) are accepted for the number of prisoners in run command.")
            return
        
        try:
            os.remove("log.txt")
        except FileNotFoundError:
            pass

        run_experiments(num_prisoners, num_experiments)

    elif command == "plot":
        if len(sys.argv) < 5:
            print("Usage: python main.py plot <start number> <end number> <experiment times>")
            return
        try:
            start_num = int(sys.argv[2])
            end_num = int(sys.argv[3])
            experiment_times = int(sys.argv[4])
        except ValueError:
            print("Invalid input for plot parameters. Usage: python main.py plot <start number> <end number> <experiment times>")
            return
        
        # Validate start and end number
        if start_num < 2 or start_num % 2 != 0 or end_num < 2 or end_num % 2 != 0:
            print("Error: Only even numbers (>=2) are accepted for the number of prisoners in plot command.")
            return

        if start_num > end_num:
            print("Error: The start number must be less than or equal to the end number.")
            return
        
        try:
            os.remove("log.txt")
        except FileNotFoundError:
            pass

        plot_experiments(start_num, end_num, experiment_times)

    else:
        print("Unknown command. Usage: python main.py [test|run|plot] [arguments]")

if __name__ == "__main__":
    main()
