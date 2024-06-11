import csv
import math

def read_input(file_path):
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
    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['index'])  # ヘッダー行を追加
        writer.writerows(output_data)

def calculate_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def solve(input_data):
    n = len(input_data)
    visited = [False] * n
    path = [0]
    visited[0] = True

    for _ in range(n - 1):
        last = path[-1]
        next_city = None
        min_distance = float('inf')
        for i in range(n):
            if not visited[i]:
                distance = calculate_distance(input_data[last], input_data[i])
                if distance < min_distance:
                    min_distance = distance
                    next_city = i
        path.append(next_city)
        visited[next_city] = True

    path.append(0)  # 戻ってくる
    return [[city] for city in path]

def main():
    for i in range(7):
        input_file = f'input_{i}.csv'
        output_file = f'output_{i}.csv'
        input_data = read_input(input_file)
        output_data = solve(input_data)
        write_output(output_file, output_data)

if __name__ == "__main__":
    main()
