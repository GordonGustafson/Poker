def all_equal(lst):
    if not lst:
        # there are no elements in the list, so all elements are the same value
        return True
    # return whether the number of occurrences of the first element
    # are equal to the number of elements in the list.
    return lst.count(lst[0]) == len(lst)
