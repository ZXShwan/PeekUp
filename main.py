from pli import PLI
import pandas as pd
import sys


def strategy_take(seeds):
    K = seeds.pop(0)
    return K


def check_subset_nonunique(combine_K):
    if exist_unchecked_subset(combine_K):
        return False
    for sub_pli in combine_K.subset:
        if sub_pli.uniqueness:
            return False
    return True


def check_superset_unique(combine_K):
    if exist_unchecked_superset(combine_K):
        return False
    for super_pli in combine_K.superset:
        if not super_pli.uniqueness:
            return False
    return True


def exist_unchecked_subset(combine_K):
    if len(combine_K.subset) < len(combine_K.column_name):
        return True
    else:
        return False


def exist_unchecked_superset(combine_K):
    if len(combine_K.superset) < (len(column_names) - len(combine_K.column_name)):
        return True
    else:
        return False


def pickone_unchecked_subset(combine_K):
    column_name = combine_K.column_name
    for i in range(len(column_name)):
        temp_tuple = column_name[:i] + column_name[i + 1:]
        temp_tuple = tuple(sorted(list(temp_tuple)))
        if temp_tuple not in PLIs.keys():
            # temp_pli = combine(temp_tuple)
            return temp_tuple
        else:
            temp_pli = PLIs[temp_tuple]
        if temp_pli not in combine_K.subset:
            combine_K.subset.append(temp_pli)
            # return temp_tuple


def pickone_unchecked_superset(combine_K):
    for i in range(len(column_names)):
        if column_names[i] not in combine_K.column_name:
            temp_tuple = combine_K.column_name + (column_names[i],)
            temp_tuple = tuple(sorted(list(temp_tuple)))
            if temp_tuple not in PLIs.keys():
                # temp_pli = combine(temp_tuple)
                return temp_tuple

            else:
                temp_pli = PLIs[temp_tuple]
            if temp_pli not in combine_K.superset:
                combine_K.superset.append(temp_pli)
                # return temp_tuple


def randomWalkStep(combine_K, pathTrace):
    pathTrace.append(combine_K)
    if combine_K.isUniqueness() and exist_unchecked_subset(combine_K):
        unchecked = pickone_unchecked_subset(combine_K)
        if unchecked:
            return unchecked
        else:
            return pathTrace.pop().column_name
    elif not combine_K.isUniqueness() and exist_unchecked_superset(combine_K):
        unchecked = pickone_unchecked_superset(combine_K)
        if unchecked is not None:
            return unchecked
        else:
            return pathTrace.pop().column_name
    else:
        if pathTrace[-1].column_name == combine_K.column_name:
            pathTrace.pop()
        if pathTrace:
            return pathTrace.pop().column_name
        else:
            return None


def build_plis(data):
    PLIs = {}
    column_names = []
    for column_name in data.columns:
        column = data[column_name]
        pli = PLI((column_name,))
        pli.build(column)
        PLIs[(column_name,)] = pli
        column_names.append(column_name)
    return PLIs, column_names


def combine(K):  # (A,B)
    K = tuple(sorted(list(K)))
    if K in PLIs.keys():
        return PLIs[K]
    combine_K = None
    # print(K)
    i = len(K)
    while i > 0:
        if K[0:i] in PLIs:
            combine_K = PLIs[K[0:i]]
            while i < len(K):
                combine_K = combine_K.merge(PLIs[(K[i],)])
                if combine_K.isUniqueness():
                    combine_K.uniqueness = True
                else:
                    combine_K.uniqueness = False
                PLIs[combine_K.column_name] = combine_K
                i += 1
            return combine_K
        else:
            i -= 1
    return combine_K


# modified
def check_all_unique(PLIs):
    list_unique_columns = []
    list_nonunique_columns = []
    for _, pli in PLIs.items():
        if pli.isUniqueness():
            list_unique_columns.append(PLI)
            pli.uniqueness = True
        else:
            list_nonunique_columns.append(pli)
            pli.uniqueness = False
    return list_unique_columns, list_nonunique_columns


def produce_seeds(list_nonunique_columns):
    seeds = []
    for i in range(len(list_nonunique_columns)):
        for j in range(i):
            combine_key = list_nonunique_columns[i].column_name + list_nonunique_columns[j].column_name
            seeds.append(combine_key)
    return seeds  # (A,B)


if __name__ == '__main__':
    data = pd.read_csv('testdata.csv')
    # data = pd.read_csv('test2.csv')
    # data = pd.read_csv(sys.argv[1])
    mUcs = set()
    mnUcs = set()
    PLIs, column_names = build_plis(data)
    list_unique_columns, list_nonunique_columns = check_all_unique(PLIs)
    # uniqueGraph = UniqueGraph(PLIs.keys())
    seeds = produce_seeds(list_nonunique_columns)
    for pli in list_unique_columns:
        mUcs.add(pli)
    pathTrace = []

    # while len(seeds) > 0:
    while len(seeds) > 0:
        K = strategy_take(seeds)
        # print(K)
        while K is not None:
            combine_K = combine(K)

            # check uniqueness
            if combine_K.uniqueness is None:
                if combine_K.isUniqueness():
                    combine_K.uniqueness = True
                    # uniqueGraph.insert_unique(combine_K)
                else:
                    combine_K.uniqueness = False
                    # uniqueGraph.insert_none_unique(combine_K)

            # find mUc and mnUc
            if combine_K.uniqueness and check_subset_nonunique(combine_K):
                mUcs.add(combine_K)
            elif not combine_K.uniqueness and check_superset_unique(combine_K):
                mnUcs.add(combine_K)

            K = randomWalkStep(combine_K, pathTrace)
        # seeds = strategyNextSeeds()

    print("mUcs:")
    print([i.column_name for i in mUcs])
    print("mnUcs:")
    print([i.column_name for i in mnUcs])
