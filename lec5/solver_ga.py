import csv
import math
import random
import numpy as np

def read_input(file_path):
    """
    CSVファイルから都市の座標データを読み込む関数。
    
    Args:
    - file_path (str): ファイルのパス
    
    Returns:
    - data (list): 読み込んだ都市の座標データのリスト
    """
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # ヘッダー行をスキップ
        data = []
        for row in reader:
            try:
                # 各行の値を浮動小数点数に変換してリストに追加
                data.append([float(val) for val in row])
            except ValueError as e:
                # 変換に失敗した場合、エラーメッセージを表示
                print(f"Error converting row to floats: {row}. Error: {e}")
                raise
    return data

def write_output(file_path, output_data):
    """
    出力データをCSVファイルに書き込む関数。
    
    Args:
    - file_path (str): 出力ファイルのパス
    - output_data (list): 出力するデータのリスト
    """
    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['index'])  # ヘッダー行を追加
        writer.writerows([[i] for i in output_data])

def calculate_distance(city1, city2):
    """
    2つの都市の座標間の距離を計算する関数。
    
    Args:
    - city1 (list): 都市1の座標 [x, y]
    - city2 (list): 都市2の座標 [x, y]
    
    Returns:
    - float: 2つの都市間の距離
    """
    return math.sqrt((city1[0] - city2[0])**2 + (city1[1] - city2[1])**2)

def total_distance(tour, cities):
    """
    巡回路の総距離を計算する関数。
    
    Args:
    - tour (list): 巡回路（都市インデックスのリスト）
    - cities (list): 都市の座標のリスト
    
    Returns:
    - float: 巡回路の総距離
    """
    total_dist = 0
    num_cities = len(tour)
    for i in range(num_cities):
        total_dist += calculate_distance(cities[tour[i]], cities[tour[(i + 1) % num_cities]])
    return total_dist

def initial_population(num_individuals, num_cities):
    """
    初期集団を生成する関数。
    
    Args:
    - num_individuals (int): 個体数
    - num_cities (int): 都市の数
    
    Returns:
    - list: 初期集団（個体のリスト）
    """
    population = []
    for _ in range(num_individuals):
        individual = list(range(num_cities))
        random.shuffle(individual)
        population.append(individual)
    return population

def tournament_selection(population, fitnesses, tournament_size):
    """
    トーナメント選択を行う関数。
    
    Args:
    - population (list): 個体群（個体のリスト）
    - fitnesses (list): 個体の適応度のリスト
    - tournament_size (int): トーナメントのサイズ
    
    Returns:
    - list: 選ばれた個体のインデックスのリスト
    """
    selected_indices = []
    for _ in range(len(population)):
        tournament_indices = random.sample(range(len(population)), tournament_size)
        tournament_fitnesses = [fitnesses[i] for i in tournament_indices]
        selected_indices.append(tournament_indices[np.argmax(tournament_fitnesses)])
    return selected_indices

def order_crossover(parent1, parent2):
    """
    順序交叉（Order Crossover）を行う関数。
    
    Args:
    - parent1 (list): 親個体1（都市インデックスのリスト）
    - parent2 (list): 親個体2（都市インデックスのリスト）
    
    Returns:
    - list: 子個体（都市インデックスのリスト）
    """
    n = len(parent1)
    child = [-1] * n
    start, end = sorted(random.sample(range(n), 2))
    for i in range(start, end + 1):
        child[i] = parent1[i]
    p2_index = 0
    for i in range(n):
        if child[i] == -1:
            while parent2[p2_index] in child:
                p2_index += 1
            child[i] = parent2[p2_index]
    return child

def mutate(individual, mutation_rate):
    """
    突然変異を行う関数。
    
    Args:
    - individual (list): 個体（都市インデックスのリスト）
    - mutation_rate (float): 突然変異率
    
    Returns:
    - list: 変異後の個体（都市インデックスのリスト）
    """
    if random.random() < mutation_rate:
        i, j = sorted(random.sample(range(len(individual)), 2))
        individual[i:j+1] = reversed(individual[i:j+1])
    return individual

def evaluate_population(population, cities):
    """
    個体群の適応度を評価する関数。
    
    Args:
    - population (list): 個体群（個体のリスト）
    - cities (list): 都市の座標のリスト
    
    Returns:
    - list: 各個体の適応度のリスト
    """
    fitnesses = []
    for individual in population:
        fitness = 1 / total_distance(individual, cities)  # 適応度（距離の逆数）
        fitnesses.append(fitness)
    return fitnesses

def select_best_individual(population, fitnesses):
    """
    最も適応度の高い個体を選択する関数。
    
    Args:
    - population (list): 個体群（個体のリスト）
    - fitnesses (list): 個体の適応度のリスト
    
    Returns:
    - list: 最も適応度の高い個体
    """
    return population[np.argmax(fitnesses)]

def genetic_algorithm(cities, population_size=100, num_generations=1000, mutation_rate=0.01, tournament_size=5):
    """
    遺伝的アルゴリズムで巡回セールスマン問題を解く関数。
    
    Args:
    - cities (list): 都市の座標のリスト
    - population_size (int): 個体群のサイズ
    - num_generations (int): 世代数
    - mutation_rate (float): 突然変異率
    - tournament_size (int): トーナメントのサイズ
    
    Returns:
    - list: 最適な巡回路（都市インデックスのリスト）
    """
    num_cities = len(cities)
    population = initial_population(population_size, num_cities)
    
    for generation in range(num_generations):
        fitnesses = evaluate_population(population, cities)
        new_population = [select_best_individual(population, fitnesses)]

        while len(new_population) < population_size:
            parent_indices = tournament_selection(population, fitnesses, tournament_size)
            parent1 = population[parent_indices[0]]
            parent2 = population[parent_indices[1]]
            child = order_crossover(parent1, parent2)
            child = mutate(child, mutation_rate)
            new_population.append(child)
        
        population = new_population
    
    best_individual = select_best_individual(population, evaluate_population(population, cities))
    return best_individual

def main():
    """
    メイン関数。複数の入力ファイルに対して遺伝的アルゴリズムを実行し、出力ファイルに結果を書き込む。
    """
    for i in range(7):
        input_file = f'input_{i}.csv'
        output_file = f'output_{i}.csv'

        cities = read_input(input_file)
        best_tour = genetic_algorithm(cities)

        write_output(output_file, best_tour)

if __name__ == "__main__":
    main()
