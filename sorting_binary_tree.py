from typing import List, Optional
from collections import deque
import math


class ListNode:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next


class AdvancedSorter:

    def __init__(self):
        pass

    # =========================================================
    # 1. ARRAY MERGE SORT
    #    (Virtual Sublists + Single tmpArray)
    # =========================================================
    def sort_array(self, arr: List[int]) -> List[int]:

        if len(arr) <= 1:
            return arr

        # HANYA SATU tmpArray dialokasikan
        tmp_array = [0] * len(arr)

        self._rec_merge_sort(arr, 0, len(arr) - 1, tmp_array)

        return arr

    def _rec_merge_sort(self, arr, first, last, tmp_array):

        if first >= last:
            return

        mid = (first + last) // 2

        self._rec_merge_sort(arr, first, mid, tmp_array)
        self._rec_merge_sort(arr, mid + 1, last, tmp_array)

        self._merge_virtual(arr, first, mid, last, tmp_array)

    def _merge_virtual(self, arr, left_start, mid, right_end, tmp_array):

        left = left_start
        right = mid + 1
        index = left_start

        # STABLE merge
        while left <= mid and right <= right_end:

            # <= menjaga stabilitas
            if arr[left] <= arr[right]:
                tmp_array[index] = arr[left]
                left += 1
            else:
                tmp_array[index] = arr[right]
                right += 1

            index += 1

        while left <= mid:
            tmp_array[index] = arr[left]
            left += 1
            index += 1

        while right <= right_end:
            tmp_array[index] = arr[right]
            right += 1
            index += 1

        # Copy balik
        for i in range(left_start, right_end + 1):
            arr[i] = tmp_array[i]

    # =========================================================
    # 2. LINKED LIST MERGE SORT
    # =========================================================
    def sort_linked_list(self, head: Optional[ListNode]) -> Optional[ListNode]:

        if head is None or head.next is None:
            return head

        right_head = self._split_linked_list(head)

        left_sorted = self.sort_linked_list(head)
        right_sorted = self.sort_linked_list(right_head)

        return self._merge_linked_lists(left_sorted, right_sorted)

    def _split_linked_list(self, head: ListNode) -> Optional[ListNode]:

        if head is None or head.next is None:
            return None

        # Fast-Slow Pointer
        midPoint = head
        curNode = head.next

        while curNode and curNode.next:
            midPoint = midPoint.next
            curNode = curNode.next.next

        right_head = midPoint.next

        # Putus linked list
        midPoint.next = None

        return right_head

    def _merge_linked_lists(
        self,
        listA: Optional[ListNode],
        listB: Optional[ListNode]
    ) -> Optional[ListNode]:

        # HANYA 1 dummy node
        dummy = ListNode(0)
        tail = dummy

        while listA and listB:

            # <= menjaga stabilitas
            if listA.data <= listB.data:
                tail.next = listA
                listA = listA.next
            else:
                tail.next = listB
                listB = listB.next

            tail = tail.next

        tail.next = listA if listA else listB

        return dummy.next

    # =========================================================
    # 3. QUICK SORT
    #    Median-of-Three + Depth Limiter
    # =========================================================
    def quick_sort(self, arr: List[int]) -> List[int]:

        if len(arr) <= 1:
            return arr

        depth_limit = 2 * math.log2(len(arr))

        # tmp_array fallback HANYA SATU KALI
        tmp_array = [0] * len(arr)

        self._quick_sort_recursive(
            arr,
            0,
            len(arr) - 1,
            0,
            depth_limit,
            tmp_array
        )

        return arr

    def _quick_sort_recursive(
        self,
        arr,
        first,
        last,
        depth,
        depth_limit,
        tmp_array
    ):

        if first >= last:
            return

        # Fallback ke merge sort
        if depth > depth_limit:
            self._rec_merge_sort(arr, first, last, tmp_array)
            return

        pivot_pos = self.partition_quick(arr, first, last)

        self._quick_sort_recursive(
            arr,
            first,
            pivot_pos - 1,
            depth + 1,
            depth_limit,
            tmp_array
        )

        self._quick_sort_recursive(
            arr,
            pivot_pos + 1,
            last,
            depth + 1,
            depth_limit,
            tmp_array
        )

    def partition_quick(self, arr: List[int], first: int, last: int) -> int:

        mid = (first + last) // 2

        # Median-of-three
        if arr[first] > arr[mid]:
            arr[first], arr[mid] = arr[mid], arr[first]

        if arr[first] > arr[last]:
            arr[first], arr[last] = arr[last], arr[first]

        if arr[mid] > arr[last]:
            arr[mid], arr[last] = arr[last], arr[mid]

        # Pindahkan median ke first
        arr[first], arr[mid] = arr[mid], arr[first]

        pivot = arr[first]

        left = first + 1
        right = last

        while True:

            while left <= right and arr[left] <= pivot:
                left += 1

            while left <= right and arr[right] > pivot:
                right -= 1

            if left > right:
                break

            arr[left], arr[right] = arr[right], arr[left]

        arr[first], arr[right] = arr[right], arr[first]

        return right


# =========================================================
# EXPRESSION TREE + HEAPSORT
# =========================================================
class ExprHeapSorter:

    def __init__(self, expr_str: str):
        self.expr = expr_str
        self.values = []

    def parse_and_evaluate(self) -> List[int]:

        tokens = deque(self.expr.replace(" ", ""))

        root = self._build_tree(tokens)

        self.values = []

        final_result = self._eval_tree(root)

        self.values.append(final_result)

        return self.values

    # =========================================================
    # EXPRESSION TREE
    # =========================================================
    def _build_tree(self, tokens: deque) -> Optional[dict]:

        if not tokens:
            return None

        token = tokens.popleft()

        # Subtree
        if token == '(':

            left = self._build_tree(tokens)

            if not tokens:
                raise ValueError("Operator hilang")

            operator = tokens.popleft()

            if operator not in ['+', '-', '*', '/']:
                raise ValueError("Operator tidak valid")

            right = self._build_tree(tokens)

            if not tokens or tokens.popleft() != ')':
                raise ValueError("Kurung tutup tidak valid")

            return {
                'val': operator,
                'left': left,
                'right': right
            }

        # Operand
        elif token.isdigit():

            return {
                'val': int(token),
                'left': None,
                'right': None
            }

        else:
            raise ValueError("Token tidak valid")

    # =========================================================
    # POSTORDER EVALUATION
    # =========================================================
    def _eval_tree(self, node: Optional[dict]) -> int:

        if node is None:
            return 0

        # Leaf node
        if node['left'] is None and node['right'] is None:
            return node['val']

        left = self._eval_tree(node['left'])
        right = self._eval_tree(node['right'])

        op = node['val']

        if op == '+':
            return left + right

        elif op == '-':
            return left - right

        elif op == '*':
            return left * right

        elif op == '/':

            if right == 0:
                raise ValueError("Division by zero")

            return left // right

        raise ValueError("Operator tidak valid")

    # =========================================================
    # HEAPSORT IN-PLACE
    # =========================================================
    def heapsort_inplace(self, arr: List[int]) -> List[int]:

        n = len(arr)

        if n <= 1:
            return arr

        # Build max heap
        for i in range(n // 2 - 1, -1, -1):
            self._sift_down(arr, n, i)

        # Extract
        for end in range(n - 1, 0, -1):

            arr[0], arr[end] = arr[end], arr[0]

            self._sift_down(arr, end, 0)

        return arr

    def _sift_down(self, arr: List[int], heap_size: int, idx: int):

        while True:

            largest = idx

            left = 2 * idx + 1
            right = 2 * idx + 2

            if left < heap_size and arr[left] > arr[largest]:
                largest = left

            if right < heap_size and arr[right] > arr[largest]:
                largest = right

            if largest == idx:
                break

            arr[idx], arr[largest] = arr[largest], arr[idx]

            idx = largest

    # =========================================================
    # COMPLETE TREE VALIDATOR
    # =========================================================
    def is_complete_tree(self, arr: List[int]) -> bool:

        n = len(arr)

        for i in range(n):

            left = 2 * i + 1
            right = 2 * i + 2

            # Tidak boleh right child tanpa left child
            if right < n and left >= n:
                return False

        return True


# =========================================================
# TESTING
# =========================================================
if __name__ == "__main__":

    sorter = AdvancedSorter()

    # ARRAY MERGE SORT
    arr = [9, 4, 7, 1, 3, 8]
    print("Merge Sort:")
    print(sorter.sort_array(arr))

    # QUICK SORT
    arr2 = [10, 7, 8, 9, 1, 5]
    print("\nQuick Sort:")
    print(sorter.quick_sort(arr2))

    # LINKED LIST MERGE SORT
    head = ListNode(4)
    head.next = ListNode(2)
    head.next.next = ListNode(5)
    head.next.next.next = ListNode(1)

    sorted_head = sorter.sort_linked_list(head)

    print("\nLinked List Merge Sort:")

    current = sorted_head
    while current:
        print(current.data, end=" -> ")
        current = current.next

    print("None")

    # EXPRESSION TREE + HEAPSORT
    expr = "((8*5)+(9/(7-4)))"

    heap_sorter = ExprHeapSorter(expr)

    values = heap_sorter.parse_and_evaluate()

    print("\nExpression Result:")
    print(values)

    extra_values = values + [12, 7, 25, 3, 19, 1, 8]

    print("\nHeapSort In-Place:")
    print(heap_sorter.heapsort_inplace(extra_values))

    print("\nComplete Tree Check:")
    print(heap_sorter.is_complete_tree(extra_values))