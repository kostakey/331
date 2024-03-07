"""
Project 2 - Hybrid Sorting
CSE 331 Spring 2024
Aman T., Daniel B., David R., Matt W.
"""

from typing import TypeVar, List, Callable

T = TypeVar("T")  # represents generic type


# This is an optional helper function but HIGHLY recommended,  especially for the application problem!
def do_comparison(first: T, second: T, comparator: Callable[[T, T], bool], descending: bool) -> bool:
    """
    Takes elements first and second, the comparator, and descending as arguments, and tells you whether or not to put a
        before b in the sorted list
    :param first: the first element of comparison
    :param second: the second element of comparison
    :param comparator: A function which takes two arguments of type T and returns True when the first argument should
        be treated as less than the second argument
    :param descending: Performs the sort in descending order when this is True, defaults to False
    :return: True if an element should come before the other element, False otherwise
    """
    if descending:
        # inverts the comparison between the two values
        # inverts the input, NOT the operation as there can be a conflict with </>= stuff
        return comparator(second, first)
    else:
        # meets comparison condition between the two values
        return comparator(first, second)


def selection_sort(data: List[T], *, comparator: Callable[[T, T], bool] = lambda x, y: x < y,
                   descending: bool = False) -> None:
    """
    Sorts a list in-place using the selection sort algorithm and the provided comparator, and performs the sort in
        descending order if descending is True
    :param data: list of items to be sorted
    :param comparator: A function which takes two arguments of type T and returns True when the first argument should
        be treated as less than the second argument
    :param descending: Performs the sort in descending order when this is True, defaults to False
    :return: None
    """
    for i in range(len(data)):
        min_idx = i
        for j in range(i + 1, len(data)):
            if do_comparison(data[j], data[min_idx], comparator, descending):
                min_idx = j
        # pythonic swapping of indexes
        data[i], data[min_idx] = data[min_idx], data[i]
    return


def bubble_sort(data: List[T], *, comparator: Callable[[T, T], bool] = lambda x, y: x < y,
                descending: bool = False) -> None:
    """
    Sorts a list in-place using the bubble sort algorithm and the provided comparator, and performs the sort in
        descending order if descending is True
    :param data: list of items to be sorted
    :param comparator: A function which takes two arguments of type T and returns True when the first argument should
        be treated as less than the second argument
    :param descending: Performs the sort in descending order when this is True, defaults to False
    :return: None
    """
    # for no out of range errors :)
    swap_range = len(data)-1
    no_swap_cnt = 0
    # condition to continue passing through the loop, breaks when a pass is filled with no swaps
    while no_swap_cnt < swap_range:
        # reset counter if the list is still left unsorted
        no_swap_cnt = 0
        # for loop that iterates through the list
        for i in range(swap_range):
            if do_comparison(data[i+1], data[i], comparator, descending):
                data[i], data[i+1] = data[i+1], data[i]
            else:
                # increment every time there is a comparison that is already satisfied
                no_swap_cnt += 1
    return


def insertion_sort(data: List[T], *, comparator: Callable[[T, T], bool] = lambda x, y: x < y,
                   descending: bool = False) -> None:
    """
    Sorts a list in-place using the insertion sort algorithm and the provided comparator, and performs the sort in
        descending order if descending is True
    :param data: list of items to be sorted
    :param comparator: A function which takes two arguments of type T and returns True when the first argument should
        be treated as less than the second argument
    :param descending: Performs the sort in descending order when this is True, defaults to False
    :return: None
    """
    # start iterating on the second element of the list, so index j doesn't go to the last element
    for i in range(1, len(data)):
        # index of the current element
        curr = data[i]
        # index of the "last" element of the sorted list
        j = i-1
        # going down the elements in the sorted list, until reaching the first element
        while j >= 0 and do_comparison(curr, data[j], comparator, descending):
            # swap the elements that meet the above condition
            data[j+1] = data[j]
            # and then...
            # update the index closer to the "start" of the sorted list
            j -= 1
        # after reaching the "first" element of the sorted list...
        # update the current element to the unsorted portion of the list
        data[j+1] = curr
    return


def hybrid_merge_sort(data: List[T], *, threshold: int = 12,
                      comparator: Callable[[T, T], bool] = lambda x, y: x < y, descending: bool = False) -> None:
    """
    Sorts a list using a hybrid sort with the merge sort and insertion sort algorithms and the provided comparator,
        and performs the sort in descending order if descending is True
    :param data: list of items to be sorted
    :param threshold: maximum size at which insertion sort will be used instead of merge sort
    :param comparator: a function which takes two arguments of type T and returns True when the first argument should
        be treated as less than the second argument
    :param descending: performs the sort in descending order when this is True, defaults to False
    :return: None
    """
    def hybrid_merge_sort_inner(arr1: List[T]) -> List[T]:
        """
        Function that handles the recursive calls, used in the hybrid_merge_sort wrapper
        :param arr1: list of items to be sorted
        :return: sorted list
        """
        if len(arr1) > 1:
            if len(arr1) <= threshold:
                insertion_sort(arr1, comparator=comparator, descending=descending)
            else:
                # find the midpoint (floored)
                midpoint = len(arr1) // 2
                # recursive call
                l1 = arr1[:midpoint]
                l2 = arr1[midpoint:]

                if len(l1) <= threshold:
                    insertion_sort(l1, comparator=comparator, descending=descending)
                else:
                    hybrid_merge_sort_inner(l1)

                if len(l2) <= threshold:
                    insertion_sort(l2, comparator=comparator, descending=descending)
                else:
                    hybrid_merge_sort_inner(l2)

                # l1 iterator
                i = 0
                # l2 iterator
                j = 0
                # main list iterator
                k = 0

                while i < len(l1) and j < len(l2):
                    # if ascending...
                    if do_comparison(l1[i], l2[j], comparator, descending):
                        arr1[k] = l1[i]
                        i += 1
                    else:
                        arr1[k] = l2[j]
                        j += 1
                    k += 1

                while i < len(l1):
                    arr1[k] = l1[i]
                    i += 1
                    k += 1

                while j < len(l2):
                    arr1[k] = l2[j]
                    j += 1
                    k += 1
        return arr1

    # inner function to handle recursion
    hybrid_merge_sort_inner(data)
    return


def quicksort(data: List[T]) -> None:
    """
    Sorts a list in place using quicksort
    :param data: Data to sort
    """

    def quicksort_inner(first: int, last: int) -> None:
        """
        Sorts portion of list at indices in interval [first, last] using quicksort

        :param first: first index of portion of data to sort
        :param last: last index of portion of data to sort
        """
        # List must already be sorted in this case
        if first >= last:
            return

        left = first
        right = last

        # Need to start by getting median of 3 to use for pivot
        # We can do this by sorting the first, middle, and last elements
        midpoint = (right - left) // 2 + left
        if data[left] > data[right]:
            data[left], data[right] = data[right], data[left]
        if data[left] > data[midpoint]:
            data[left], data[midpoint] = data[midpoint], data[left]
        if data[midpoint] > data[right]:
            data[midpoint], data[right] = data[right], data[midpoint]
        # data[midpoint] now contains the median of first, last, and middle elements
        pivot = data[midpoint]
        # First and last elements are already on right side of pivot since they are sorted
        left += 1
        right -= 1

        # Move pointers until they cross
        while left <= right:
            # Move left and right pointers until they cross or reach values which could be swapped
            # Anything < pivot must move to left side, anything > pivot must move to right side
            #
            # Not allowing one pointer to stop moving when it reached the pivot (data[left/right] == pivot)
            # could cause one pointer to move all the way to one side in the pathological case of the pivot being
            # the min or max element, leading to infinitely calling the inner function on the same indices without
            # ever swapping
            while left <= right and data[left] < pivot:
                left += 1
            while left <= right and data[right] > pivot:
                right -= 1

            # Swap, but only if pointers haven't crossed
            if left <= right:
                data[left], data[right] = data[right], data[left]
                left += 1
                right -= 1

        quicksort_inner(first, left - 1)
        quicksort_inner(left, last)

    # Perform sort in the inner function
    quicksort_inner(0, len(data) - 1)


###########################################################
# DO NOT MODIFY
###########################################################

class Score:
    """
    Class that represents SAT scores
    NOTE: While it is possible to implement Python "magic methods" to prevent the need of a key function,
    this is not allowed for this application problems so students can learn how to create comparators of custom objects.
    Additionally, an individual section score can be outside the range [400, 800] and may not be a multiple of 10
    """

    __slots__ = ['english', 'math']

    def __init__(self, english: int, math: int) -> None:
        """
        Constructor for the Score class
        :param english: Score for the english portion of the exam
        :param math: Score for the math portion of the exam
        :return: None
        """
        self.english = english
        self.math = math

    def __repr__(self) -> str:
        """
        Represent the Score as a string
        :return: representation of the score
        """
        return str(self)

    def __str__(self) -> str:
        """
        Convert the Score to a string
        :return: string representation of the score
        """
        return f'<English: {self.english}, Math: {self.math}>'


###########################################################
# MODIFY BELOW
###########################################################

def better_than_most(scores: List[Score], student_score: Score) -> str:
    """
    Determines if a selected student's SAT score (or part of it) is greater than the median of current MSU student's
        SAT scores
    :param scores: A list of Score objects representing the SAT score of every student
    :param student_score: A Score object representing a student's SAT score broken into two values: English and Math
    :return: A string which is one of:
        'Both' - if the student's English and Math scores are above the median
        'Math' - if only their Math score is above the median
        'English' - if only their English score is above the median
        'None' - if neither score is above the median
    """
    # initialize booleans
    e_bool = False
    m_bool = False

    # initialize lists
    e_list = []
    m_list = []

    # short circuit for when the input scores list is empty
    if len(scores) == 0:
        return 'Both'

    # O(n) time/space list forming
    for element in scores:
        e_list.append(element.english)
        m_list.append(element.math)

    # everyone takes math and english section, so both lists should be the same size
    l_len = len(e_list)

    # O(nlogn) time sorting
    hybrid_merge_sort(e_list)
    hybrid_merge_sort(m_list)

    # find the median from both lists
    e_med = e_list[l_len // 2]
    m_med = m_list[l_len // 2]

    # compare the median score from each list to the score the student received
    if student_score.english > e_med:
        e_bool = True
    if student_score.math > m_med:
        m_bool = True

    if e_bool is True and m_bool is True:
        return 'Both'
    if not e_bool and not m_bool:
        return 'None'
    if e_bool:
        return 'English'
    if m_bool:
        return 'Math'
