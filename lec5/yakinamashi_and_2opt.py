import csv
import math
import random
import numpy as np

def calculate_distance(city1, city2):
    """
    2つの都市間のユークリッド距離を計算する関数。
    """
    return math.sqrt((city1[0] - city2[0])**2 + (city1[1] - city2[1])**2)

def total_distance(tour, cities):
    """
    巡回路の総距離を計算する関数。
    """
    total_dist = 0
    num_cities = len(tour)
    for i in range(num_cities):
        total_dist += calculate_distance(cities[tour[i]], cities[tour[(i + 1) % num_cities]])
    return total_dist

def simulated_annealing(cities, initial_temperature=1000, cooling_rate=0.99, stopping_temperature=0.1):
    """
    焼きなまし法による巡回セールスマン問題の解法。
    """
    num_cities = len(cities)
    current_solution = list(range(num_cities))
    current_distance = total_distance(current_solution, cities)

    best_solution = current_solution
    best_distance = current_distance

    temperature = initial_temperature

    while temperature > stopping_temperature:
        neighbor_solution = current_solution[:]
        i, j = sorted(random.sample(range(num_cities), 2))
        neighbor_solution[i:j+1] = reversed(neighbor_solution[i:j+1])

        neighbor_distance = total_distance(neighbor_solution, cities)
        delta_distance = neighbor_distance - current_distance

        if delta_distance < 0 or random.random() < np.exp(-delta_distance / temperature):
            current_solution = neighbor_solution
            current_distance = neighbor_distance

            if current_distance < best_distance:
                best_solution = current_solution
                best_distance = current_distance

        temperature *= cooling_rate

    return best_solution

def apply_2_opt(tour, cities):
    """
    2-opt法による局所探索。
    """
    improved = True
    while improved:
        improved = False
        for i in range(1, len(tour) - 2):
            for j in range(i + 1, len(tour)):
                if j - i == 1:
                    continue  # 隣接する辺は交換しない
                new_tour = tour[:]
                new_tour[i:j] = tour[j - 1:i - 1:-1]  # 2-opt操作
                new_distance = total_distance(new_tour, cities)
                if new_distance < total_distance(tour, cities):
                    tour = new_tour
                    improved = True
                    break
            if improved:
                break
    return tour

def read_input(filename):
    """
    CSVファイルから都市の座標を読み込む関数。
    """
    cities = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            try:
                x, y = float(row[0]), float(row[1])
                cities.append((x, y))
            except ValueError:
                continue  # 非数値データが含まれている行をスキップ
    return cities

def write_output(filename, tour):
    """
    最適な巡回路をCSVファイルに書き込む関数。
    """
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for city in tour:
            writer.writerow([city])

def main():
    for i in range(7):
        input_file = f'input_{i}.csv'
        output_file = f'output_{i}.csv'

        cities = read_input(input_file)
        initial_tour = simulated_annealing(cities)
        best_tour = apply_2_opt(initial_tour, cities)

        write_output(output_file, best_tour)

if __name__ == "__main__":
    main()
