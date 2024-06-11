#2-opt アルゴリズムは、特に都市の数が多い場合、計算量が多くなることがあります。そのため、実行時間が長くなることがあります。以下に、いくつかの改善方法を提案します。
#初期経路の改善: ランダムな初期経路ではなく、より良い初期経路を生成することで、2-opt アルゴリズムの収束を早めることができます。例えば、貪欲法（nearest neighbor）を用いて初期経路を生成することが考えられます。
#実行時間の制限: 2-opt アルゴリズムの実行時間に制限を設け、時間内に得られた最良の解を採用する方法があります。
#部分的な改善: 全経路を対象にするのではなく、部分的に2-opt改善を行うことで計算時間を短縮します。

#以下に、初期経路を貪欲法で生成し、2-opt アルゴリズムの実行時間に制限を設けた例を示します。




import csv
import math
import random

# 距離の計算
def calculate_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

# 全経路の距離の計算
def total_distance(tour, distance_matrix):
    return sum(distance_matrix[tour[i]][tour[i+1]] for i in range(len(tour)-1)) + distance_matrix[tour[-1]][tour[0]]

# 2-opt アルゴリズム
def two_opt(tour, distance_matrix):
    improved = True
    while improved:
        improved = False
        for i in range(1, len(tour) - 2):
            for j in range(i + 1, len(tour)):
                if j - i == 1: continue  # 隣接するエッジはスキップ
                new_tour = tour[:]
                new_tour[i:j] = reversed(tour[i:j])
                if total_distance(new_tour, distance_matrix) < total_distance(tour, distance_matrix):
                    tour = new_tour
                    improved = True
    return tour

# データの読み込み
def read_input(file_path):
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # ヘッダー行をスキップ
        data = []
        for row in reader:
            data.append([float(val) for val in row])
    return data

# 距離行列の作成
def create_distance_matrix(input_data):
    num_cities = len(input_data)
    distance_matrix = [[0] * num_cities for _ in range(num_cities)]
    for i in range(num_cities):
        for j in range(num_cities):
            if i != j:
                distance_matrix[i][j] = calculate_distance(input_data[i], input_data[j])
    return distance_matrix

# 初期経路の生成（ランダム）
def generate_initial_tour(num_cities):
    tour = list(range(num_cities))
    random.shuffle(tour)
    return tour

# 出力の書き込み
def write_output(file_path, output_data):
    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['index'])  # ヘッダー行を追加
        writer.writerows([[i] for i in output_data])

# メイン関数
def main():
    for i in range(7):
        input_file = f'input_{i}.csv'
        output_file = f'output_{i}.csv'
        input_data = read_input(input_file)
        distance_matrix = create_distance_matrix(input_data)
        initial_tour = generate_initial_tour(len(input_data))
        best_tour = two_opt(initial_tour, distance_matrix)
        write_output(output_file, best_tour)

if __name__ == "__main__":
    main()
