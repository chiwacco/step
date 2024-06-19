#焼きなまし方：局所解に陥らず広い解空間を探索する能力がある

import csv
import math
import random
import numpy as np

# 距離の計算　city1とcity2のユークリッド距離
def calculate_distance(city1, city2):
    return math.sqrt((city1[0] - city2[0])**2 + (city1[1] - city2[1])**2)

# 全経路の距離の計算
# tour:都市のindexList　cities:各都市の座標List
def total_distance(tour, cities):
    total_dist = 0
    for i in range(len(tour)):
        total_dist += calculate_distance(cities[tour[i]], cities[tour[(i + 1) % len(tour)]])
    return total_dist

# 焼きなまし法
# initial_temperatureからcooling_rateで温度を徐々に下げながら最適解を探索
def simulated_annealing(cities, initial_temperature=1000, cooling_rate=0.99, stopping_temperature=0.1):
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

        #ランダムに選んだ2つを交換して新しい解neighbor_solutionを生成
        if delta_distance < 0 or random.random() < np.exp(-delta_distance / temperature):
            current_solution = neighbor_solution
            current_distance = neighbor_distance

            if current_distance < best_distance:
                best_solution = current_solution
                best_distance = current_distance

        temperature *= cooling_rate

    return best_solution

# データの読み込み
def read_input(file_path):
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # ヘッダー行をスキップ
        cities = []
        for row in reader:
            cities.append([float(val) for val in row])
    return cities

# 出力の書き込み
def write_output(file_path, tour):
    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['index'])  # ヘッダー行を追加
        writer.writerows([[i] for i in tour])

# メイン関数
def main():
    for i in range(7):
        input_file = f'input_{i}.csv'
        output_file = f'output_{i}.csv'

        cities = read_input(input_file)
        best_tour = simulated_annealing(cities)

        write_output(output_file, best_tour)

if __name__ == "__main__":
    main()
