class UniqueGraph:

    def __init__(self, PLI_names):  # [A,B,C,D]
        unique_graph = {}
        none_unique_graph = {}
        for item in PLI_names:
            unique_graph[item] = {}
            none_unique_graph[item] = {}

    def insert_unique(self, combined_keys):
        combined_keys = tuple(sorted(list(combined_keys)))  # smallest key as the index key
        self.unique_graph[combined_keys[0]].add(combined_keys[0])

    def insert_none_unique(self, combined_keys):
        combined_keys = tuple(sorted(list(combined_keys)))
        self.none_unique_graph[combined_keys[0]].add(combined_keys[0])

    def is_unique(self, keys):
        # key = tuple(sorted(list(key)))
        for key in keys:
            for unique_key in self.unique_graph[key]:
                if keys in unique_key:
                    return True
        return False

    def is_none_unique(self, key):
        key = tuple(sorted(list(key)))
        return key in self.none_unique_graph[key[0]]
