class PLI:

    def __init__(self, column_name):
        self.column_name = column_name  # attention
        self.position_list = []
        self.subset = []
        self.superset = []
        self.uniqueness = None

    def build(self, column):
        dic = {}
        for i in range(len(column)):
            if column[i] not in dic.keys():
                dic[column[i]] = set()
            dic[column[i]].add(i)
        for key, value in dic.items():
            if len(value) > 1:
                self.position_list.append(value)

    def isUniqueness(self):
        return len(self.position_list) == 0

    def merge(self, B_pli):
        merge_dic = {}  # (A1B1) -> (r1,r3)
        b_dic = {}
        B_index = 1
        for entry_set in B_pli.position_list:
            for item in entry_set:
                b_dic[item] = "B{0}".format(B_index)
            B_index += 1

        A_index = 1
        for pli_set in self.position_list:
            for tpl in pli_set:
                if tpl in b_dic:
                    # key = "A" + str(A_index) + b_dic[tpl]  # A1B1
                    key = "A{0}{1}".format(A_index, b_dic[tpl])
                    if key not in merge_dic:
                        merge_dic[key] = set()
                    merge_dic[key].add(tpl)
            A_index += 1

        # combine_name = self.column_name + B_pli.column_name
        combine_name = tuple(sorted(list(set(self.column_name) | set(B_pli.column_name))))
        combine_PLI = PLI(combine_name)
        for key, value in merge_dic.items():
            if len(value) > 1:
                combine_PLI.position_list.append(value)
        # self.superset.append(combine_PLI)
        # combine_PLI.subset.append(combine_PLI)
        return combine_PLI
