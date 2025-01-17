# this algorithm finds next elements of a sequence given by a polynomial with the greatest power of n - 1, where n is the number of the given elements

# 0th degree delta of a sequence is the original sequence
# 1st degree delta of a sequence contains differences between its consequent elements, which is a sequence one element shorter
# 2nd degree delta is the differences between differences, two elements shorter than the original list – delta of the first-degree delta
# ... and so on
# len - 1th degree delta is a single difference value (between the two values of len-2th degree delta)
# for predicting the next elements of the sequence, assume it remains constant for further elements added
def get_delta(sequence):
    delta = [sequence[i] - sequence[i - 1] for i in range(1, len(sequence))]
    return delta

def get_deltas(sequence):
    deltas = [list(sequence)]
    while len(deltas[-1]) > 1:
        deltas.append(get_delta(deltas[-1]))
    return deltas

def print_deltas(deltas):
    for i in range(len(deltas)):
        print(deltas[-1 - i])

# for a sequence like [1, 2, 3, 4, 5], the first delta is already constant
# differences between the consequent elements are all 1, so the next (and consequent) deltas are all zeroes
# the single highest delta dictates the difference between all elements in the delta below:
# ... the sequence of just two elements will therefore always be interpreted and expanded as algebraic sequence
# this is a_n = n and it is interpreted as such in one delta (first delta is constant), it needs 2 elements

# the sequence of a_n = n^2 like [1, 4, 9, 16, 25] is interpreted as such in two deltas (second delta is constant), it needs 3 elemetns
# similarly, the sequence of a_n = n^3 like [1, 8, 27, 64, 125] is interpreted in three deltas (needs 4 elements)

# the sequence (all of its elements) can be increased by a constant, which doesn't affect the interpretation as deltas remain the same
# therefore, a sequence of a_n = n^p + b can be interpreted as such given p + 1 first of its elements

# a sequence that is the sum of the two 'polynomial' sequences and a constant,
# like a_n = n^3 + n^2 + 1, that's [3, 13, 37, 81, 151], is still interpreted with 4 elements
# ... that is the number needed for the highest power

# to generalise, a polynomial sequence of s_n = a * n^p + b * n^(p - 1) + c * n^(p - 2) + ..., is interpreted with (p + 1) elements
# this means that, assuming each element of it is given by this formula, the next element can be predicted if (p + 1) preceding ones are given
def expand_deltas(deltas):
    for i in range(1, len(deltas)):
        difference = deltas[-i][-1]
        # add element to a delta based on the difference given in the higher delta
        deltas[-i - 1].append(deltas[-i - 1][-1] + difference)

sequence = [1, 4, 9]
deltas = get_deltas(sequence)
while(True):
    print_deltas(deltas)
    if input() == 'c': break
    expand_deltas(deltas)
    print('expanded:')
    # for i in range(len(deltas) + 1):
    #     print("\033[F\033[K", end="")