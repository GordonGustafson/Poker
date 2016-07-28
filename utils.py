def all_equal(lst):
    if not lst:
        # there are no elements in the list, so all elements are the same value
        return True
    # return whether the number of occurrences of the first element
    # are equal to the number of elements in the list.
    return lst.count(lst[0]) == len(lst)


def chunks_of_sizes(lst, chunk_sizes):
    """
    A List of sublists of `lst` of the lengths specified in chunks_sizes.
    Discards unused elements of `lst` if `len(lst) > sum(chunks_sizes)`.

    parameters:
        lst: a List to partition into chunks
        chunk_sizes: a List of sizes to make the chunks

    chunks_of_sizes([1, 2, 3, 4], [1, 2]) == [[1], [2, 3]]
    """
    if len(chunk_sizes) == 0:
        return []
    else:
        size_of_this_chunk = chunk_sizes[0]
        # This will stack overflow if `chunks_sizes` is large!
        return [lst[0:size_of_this_chunk]] + \
            chunks_of_sizes(lst[size_of_this_chunk:], chunk_sizes[1:])


def cmp(left, right):
    if left < right:
        return -1
    elif right < left:
        return 1
    else:
        return 0
