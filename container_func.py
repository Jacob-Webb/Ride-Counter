"""***********************************************************************
Library for list functions: difference and union
***********************************************************************"""
def list_union(list1, list2):
    s_list1 = sorted(list1)
    s_list2 = sorted(list2)
    list_union = []

    i = j = 0

    while i < len(s_list1) and j < len(s_list2):
    # while moving through the lists add all values but so that they only appear
    # in list_union once
        if s_list1[i] < s_list2[j]:
            list_union.append(s_list1[i])
            i += 1
        elif s_list1[i] > s_list2[j]:
            list_union.append(s_list2[j])
            j += 1
        else:
        # if both lists' values are the same then add one of the values
            list_union.append(s_list1[i])
            i += 1
            j += 1

    while i < len(s_list1):
    # if the above made it through list2 add on all remaining s_list1 values
        list_union.append(s_list1[i])
        i += 1

    while j < len(s_list2):
    # if the above made it through list1, add on all remaining s_list2 values
        list_union.append(s_list2[j])
        j += 1

    return list_union

def list_diff(list1, list2):
    s_list1 = sorted(list1)
    s_list2 = sorted(list2)
    list_diff = []

    i = j = 0

    while i < len(s_list1) and j < len(s_list2):
    # while moving through the lists add the keys to dict_diff that are in dict1 but not dict2
        if s_list1[i] < s_list2[j]:
        # if the value in dict1 is less than dict2 then it isn't in dict2
            list_diff.append(s_list1[i])
            i += 1
        elif s_list1[i] > s_list2[j]:
        # if the value in dict1 is greater than in dict2 then check the next dict2 value
            j += 1
        else:
        # if both lists' values are the same then check the next set
            i += 1
            j += 1

    while i < len(s_list1):
    # any keys of dict1 that were greater than those in dict2 will be added
        list_diff.append(s_list1[i])
        i += 1

    return list_diff

"""**********************************************************************
Library for dict functions: difference, difference in keys, and union
**********************************************************************"""
# DictDiff will get the difference between two dict containers.
def dict_diff(dict1, dict2):
    dict_diff = {}
    dict1_keys = sorted(dict1)
    dict2_keys = sorted(dict2)
    i = j = 0

    # First, move through the lists to add the keys, value pair to dict_diff
    # that are in dict1 but not dict2

    while i < len(dict1_keys) and j < len(dict2_keys):
        if dict1_keys[i] < dict2_keys[j]:
        # if the value in dict1 is less than dict2 then it isn't in dict2.
        # add the whole key and value list
            dict_diff[dict1_keys[i]] = dict1.get(dict1_keys[i])
            i += 1
        elif dict1_keys[i] > dict2_keys[j]:
        # if the value in dict1 is greater than in dict2 then check the
        # next dict2 value
            j += 1
        else:
        # if both lists' values are the same, get differences in values,
        # then check the next set
            value_list1 = dict1.get(dict1_keys[i])
            value_list2 = dict2.get(dict2_keys[j])

            dict_diff[dict1_keys[i]] = list_diff(value_list1, value_list2)

            i += 1
            j += 1

    # Then, add all key, value pairs from dict1 that haven't yet been addressed
    # above; they aren't in dict2

    while i < len(dict1_keys):
    # any keys of dict1 that were greater than those in dict2 will be added
    # along with the value
        dict_diff[dict1_keys[i]] = dict1.get(dict1_keys[i])
        i += 1

    return dict_diff

def key_diff(dict1, dict2):
    dict1_keys = dict1.keys()
    dict2_keys = dict2.keys()
    return list_diff(dict1_keys, dict2_keys)

def dict_union(dict1, dict2):
    dict_union = {}
    dict1_keys = sorted(dict1)
    dict2_keys = sorted(dict2)
    i = j = 0

    # First, move through the lists to add the keys, value pair to dict_union
    # that are either dict1 or dict2

    while i < len(dict1_keys) and j < len(dict2_keys):
        if dict1_keys[i] < dict2_keys[j]:
        # if the value in dict1 is less than dict2 then it isn't in dict2.
        # add the whole key and value list
            dict_union[dict1_keys[i]] = dict1.get(dict1_keys[i])
            i += 1
        elif dict1_keys[i] > dict2_keys[j]:
        # if the value in dict1 is greater than in dict2 then check the
        # next dict2 value
            dict_union[dict2_keys[j]] = dict2.get(dict2_keys[j])
            j += 1
        else:
        # if both lists' values are the same, get union of there lists,
        # then check the next set
            value_list1 = dict1.get(dict1_keys[i])
            value_list2 = dict2.get(dict2_keys[j])

            dict_union[dict1_keys[i]] = list_union(value_list1, value_list2)
            #dict_union[dict1_keys[i]] = dict1.get(dict1_keys[i])
            i += 1
            j += 1

    # Then, add all key, value pairs from dict1 that haven't yet been addressed
    # above; they aren't in dict2

    while i < len(dict1_keys):
    # if the above algo got through dict2_keys add the rest of dict1
        dict_union[dict1_keys[i]] = dict1.get(dict1_keys[i])
        i += 1

    while j < len(dict2_keys):
    # if the above alfo got through dict1_keys add the rest of dict2
        dict_union[dict2_keys[j]] = dict2.get(dict2_keys[j])
        j += 1

    return dict_union
