import sys
import collections
import queue

class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file):

        # A mapping from a page ID (integer) to the page title.
        # For example, self.titles[1234] returns the title of the page whose
        # ID is 1234.
        self.titles = {}

        # A set of page links.
        # For example, self.links[1234] returns an array of page IDs linked
        # from the page whose ID is 1234.
        self.links = {}

        # Read the pages file into self.titles.　分野とそのID
        with open(pages_file) as file:
            for line in file:
                (id, title) = line.rstrip().split(" ")
                id = int(id)
                assert not id in self.titles, id
                self.titles[id] = title
                self.links[id] = []
        print("Finished reading %s" % pages_file)

        # Read the links file into self.links.　分野のIDと記事のID
        with open(links_file) as file:
            for line in file:
                (src, dst) = line.rstrip().split(" ")
                (src, dst) = (int(src), int(dst))
                assert src in self.titles, src
                assert dst in self.titles, dst
                self.links[src].append(dst)
        print("Finished reading %s" % links_file)
        print()


    # Find the longest titles. This is not related to a graph algorithm at all
    # though :)
    def find_longest_titles(self):
        titles = sorted(self.titles.values(), key=len, reverse=True)
        print("The longest titles are:")
        count = 0
        index = 0
        while count < 15 and index < len(titles):
            if titles[index].find("_") == -1:
                print(titles[index])
                count += 1
            index += 1
        print()


    # Find the most linked pages.
    def find_most_linked_pages(self):
        link_count = {}
        for id in self.titles.keys():
            link_count[id] = 0

        for id in self.titles.keys():
            for dst in self.links[id]:
                link_count[dst] += 1

        print("The most linked pages are:")
        link_count_max = max(link_count.values())
        for dst in link_count.keys():
            if link_count[dst] == link_count_max:
                print(self.titles[dst], link_count_max)
        print()

    # HW1
    # Find the shortest path.
    # |start|: The title of the start page.
    # |goal|: The title of the goal page.
    def find_shortest_path(self, start, goal):
        
        start_id = None
        goal_id = None

        for id, title in self.titles.items():
            if title == start:
                start_id = id
            if title == goal:
                goal_id = id

        # If either start or goal is not found, retun None
        if start_id is None or goal_id is None:
            print("start or goal page is Not Found")
            return
        
        # Use BFS to find shortest path
        queue = collections.deque([(start_id, [start_id])])
        visited = set()

        while queue:
            current_id, path = queue.popleft()
            if current_id in visited:
                continue
            visited.add(current_id) #通過したらvisited

            if current_id == goal_id:
                # Convert path of IDs to path of titles
                path_titles = [self.titles[pid] for pid in path]
                print("Shortest path:" , "-> ".join(path_titles))
                return
            
            for child in self.links[current_id]:
                if child not in visited:
                    queue.append((child, path + [child]))

        print("No path found")
        pass

    # HW2
    # Calculate the page ranks and print the most popular pages.
    def find_most_popular_pages(self):
        num_pages = len(self.titles)
        ranks = {id: 1 /num_pages for id in self.titles}
        damping_factor = 0.85
        num_iteration = 100
        min_delta = 1e-6  # 収束しきい値

        for iteration in range(num_iteration):
            new_ranks = {id: 0 for id in self.titles}
            rank_sum = 0

            for page in self.titles:
                if len(self.links[page]) == 0:
                    rank_sum += ranks[page] / num_pages
                else:
                    for linked_page in self.links[page]:
                        new_ranks[linked_page] += damping_factor * ranks[page] / len(self.links[page])

            for page in new_ranks:
                new_ranks[page] += (1 - damping_factor) / num_pages + rank_sum * damping_factor

            # Calculate total change in PageRank value
            delta = sum(abs(new_ranks[page] - ranks[page]) for page in self.titles)
            ranks = new_ranks

            if delta < min_delta:
                break
                
        # Print: top 10 pages
        top_pages = sorted(ranks.items(), key=lambda item:item[1], reverse=True)[:10]
        print("Top 10 popular pages:")
        for page_id, rank in top_pages:
            print(f"{self.titles[page_id]}: {rank:.6f}")

        # Check: Total PageRank=1
        total_rank = sum(ranks.values())
        print(f"Total PageRank: {total_rank:.6f}")

        pass

    # HW3
    # Find the longest path in a DAG.
    # Do something more interesting!!
    def find_longest_path(self):
        def topological_sort():
            visited = set()
            stack = []
            def dfs(node):
                visited.add(node)
                for neighbor in self.links[node]:
                    if neighbor not in visited:
                        dfs(neighbor)
                stack.append(node)
            
            for node in self.titles.keys():
                if node not in visited:
                    dfs(node)
            return stack[::-1]
        
        def find_longest_path_from(start):
            distances = {node: float('-inf') for node in self.titles}
            distances[start] = 0
            path_from = {node: [] for node in self.titles}

            for node in topological_order:
                for neighbor in self.links[node]:
                    if distances[node] + 1 > distances[neighbor]:
                        distances[neighbor] = distances[node] + 1
                        path_from[neighbor] = path_from[node] + [neighbor]
            
            max_distance = max(distances.values())
            end_node = [node for node, distance in distances.items() if distance == max_distance][0]
            return (max_distance, [start] + path_from[end_node])

        
        topological_order = topological_sort()
        longest_path_length = 0
        longest_path = []

        for node in self.titles.keys():
            path_length, path = find_longest_path_from(node)
            if path_length > longest_path_length:
                longest_path_length = path_length
                longest_path = path
            
        if longest_path:
            print("The longest path is:")
            print(" -> ".join(self.titles[node] for node in longest_path))
            print(f"Length: {longest_path_length}")
        else:
            print("No path found")

        pass
        


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)

    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    #wikipedia.find_longest_titles()
    #wikipedia.find_most_linked_pages()
    #wikipedia.find_shortest_path("A", "D")
    #wikipedia.find_most_popular_pages()
    wikipedia.find_longest_path()
