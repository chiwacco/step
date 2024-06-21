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

def apply_3_opt(tour, cities):
    """
    3-opt法による局所探索。
    """
    improved = True
    while improved:
        improved = False
        num_cities = len(tour)
        for i in range(1, num_cities - 4):
            for j in range(i + 2, num_cities - 2):
                for k in range(j + 2, num_cities):
                    # Generate new tour by applying 3-opt move
                    new_tour = three_opt_swap(tour, i, j, k, cities)
                    new_distance = total_distance(new_tour, cities)
                    if new_distance < total_distance(tour, cities):
                        tour = new_tour
                        improved = True
                        break
                if improved:
                    break
            if improved:
                break
    return tour

def three_opt_swap(tour, i, j, k, cities):
    """
    Perform 3-opt swap on tour.
    """
    part1 = tour[:i]
    part2 = tour[i:j]
    part3 = tour[j:k]
    part4 = tour[k:]

    # 3-opt move: Choose one of the possible tours
    option1 = part1 + part2 + part3 + part4
    option2 = part1 + part3 + part2 + part4
    option3 = part1 + part2[::-1] + part3 + part4
    option4 = part1 + part3[::-1] + part2 + part4
    option5 = part1 + part2 + part4[::-1] + part3
    option6 = part1 + part3 + part4[::-1] + part2
    option7 = part1 + part4[::-1] + part2[::-1] + part3
    option8 = part1 + part3[::-1] + part2[::-1] + part4

    options = [option1, option2, option3, option4, option5, option6, option7, option8]

    # Choose the best option based on total distance
    best_option = min(options, key=lambda x: total_distance(x, cities))

    return best_option




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
        input_file = f'input_3.csv'
        output_file = f'output_3opt_3.csv'

        cities = read_input(input_file)
        initial_tour = simulated_annealing(cities)
        best_tour = apply_3_opt(initial_tour, cities)

        write_output(output_file, best_tour)


if __name__ == "__main__":
    main()
