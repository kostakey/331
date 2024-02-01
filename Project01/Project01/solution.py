"""
Project 1
CSE 331 SS24 (Onsay)
Authors of DLL: Andrew McDonald, Alex Woodring, Andrew Haas, Matt Kight, Lukas Richters, 
                Anna De Biasi, Tanawan Premsri, Hank Murdock, & Sai Ramesh
solution.py
"""

from typing import TypeVar, List

# for more information on type hinting, check out https://docs.python.org/3/library/typing.html
T = TypeVar("T")  # represents generic type
Node = TypeVar("Node")  # represents a Node object (forward-declare to use in Node __init__)
DLL = TypeVar("DLL")


# pro tip: PyCharm auto-renders docstrings (the multiline strings under each function definition)
# in its "Documentation" view when written in the format we use here. Open the "Documentation"
# view to quickly see what a function does by placing your cursor on it and using CTRL + Q.
# https://www.jetbrains.com/help/pycharm/documentation-tool-window.html


class Node:
    """
    Implementation of a doubly linked list node.
    DO NOT MODIFY
    """
    __slots__ = ["value", "next", "prev", "child"]

    def __init__(self, value: T, next: Node = None, prev: Node = None, child: Node = None) -> None:
        """
        Construct a doubly linked list node.

        :param value: value held by the Node.
        :param next: reference to the next Node in the linked list.
        :param prev: reference to the previous Node in the linked list.
        :return: None.
        DO NOT MODIFY
        """
        self.next = next
        self.prev = prev
        self.value = value

        # The child attribute is only used for the application problem
        self.child = child

    def __repr__(self) -> str:
        """
        Represents the Node as a string.

        :return: string representation of the Node.
        DO NOT MODIFY
        """
        return f"Node({str(self.value)})"

    __str__ = __repr__


class DLL:
    """
    Implementation of a doubly linked list without padding nodes.
    Modify only below indicated line.
    """
    __slots__ = ["head", "tail", "size"]

    def __init__(self) -> None:
        """
        Construct an empty doubly linked list.

        :return: None.
        DO NOT MODIFY
        """
        self.head = self.tail = None
        self.size = 0

    def __repr__(self) -> str:
        """
        Represent the DLL as a string.

        :return: string representation of the DLL.
        DO NOT MODIFY
        """
        result = []
        node = self.head
        while node is not None:
            result.append(str(node))
            node = node.next
            if node is self.head:
                break
        return " <-> ".join(result)

    def __str__(self) -> str:
        """
        Represent the DLL as a string.

        :return: string representation of the DLL.
        """
        return repr(self)

    def __eq__(self, other: DLL) -> bool:
        """
        :param other: compares equality with this List
        :return: True if equal otherwise False
        DO NOT MODIFY
        """
        cur_node = self.head
        other_node = other.head
        while True:
            if cur_node != other_node:
                return False
            if cur_node is None and other_node is None:
                return True
            if cur_node is None or other_node is None:
                return False
            cur_node = cur_node.next
            other_node = other_node.next
            if cur_node is self.head and other_node is other.head:
                return True
            if cur_node is self.head or other_node is other.head:
                return False

    # MODIFY BELOW #
    # Refer to the classes provided to understand the problems better#

    def empty(self) -> bool:
        """
        Returns a boolean indicating whether the DLL is empty
        :return: True if the DLL is empty, False if the DLL is not empty
        """
        if self.size == 0:
            return True
        return False

    def push(self, val: T, back: bool = True) -> None:
        """
        Adds a Node containing val to the back or front of the DLL and updates size accordingly
        :param val: value stored in the pushed node
        :param back: if True (default), node will be appended to DLL, if False, node will be prepended to DLL
        :return: None
        """
        new_node = Node(val)
        # if the new node is the only node in the DLL
        if self.size == 0:
            self.head = new_node
            self.tail = new_node
            self.size += 1
            return None
        # pushing to front of the DLL (prepend)
        if self.size != 0 and back is False:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
            self.size += 1
        # pushing to back of the DLL (append)
        if self.size != 0 and back is True:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
            self.size += 1
        return None

    def pop(self, back: bool = True) -> None:
        """
        Removes the Node at either the beginning or end of the DLL
        :param back: if True (default), node will be popped from the back of the DLL, if False, node will be popped
            from the beginning of the DLL
        :return: None
        """
        # do nothing if the DLL is empty
        if self.size == 0:
            return None
        # when there is one node left in the DLL
        if self.size == 1:
            self.tail = self.head
            self.head = None
            self.tail = None
            self.size -= 1
            return None
        # pop the node on the front of the list
        if self.size != 0 and back is False:
            self.head = self.head.next
            self.head.prev = None
            self.size -= 1
        # pop the node on the back of the list
        if self.size != 0 and back is True:
            self.tail = self.tail.prev
            self.tail.next = None
            self.size -= 1
        return None

    def list_to_dll(self, source: List[T]) -> None:
        """
        Creates a DLL from a standard Python list. If there are already nodes in the DLL, it should get wiped and
            completely replaced by the source
        :param source: standard Python list to construct a DLL from
        :return: None
        """
        # clear the DLL on every call to this function
        self.head = None
        self.tail = None
        self.size = 0

        for num, val in enumerate(source):
            new_node = Node(val)
            # for the first element of the source
            if num == 0:
                self.head = new_node
                self.tail = new_node
            # for every element of the source besides the first
            else:
                new_node.prev = self.tail
                self.tail.next = new_node
                self.tail = new_node
            self.size += 1
        return None

    def dll_to_list(self) -> List[T]:
        """
        Creates a standard Python list from a DLL
        :return: List[T] containing the values of the nodes from the DLL
        """
        new_list = []
        curr = self.head
        while curr:
            new_list.append(curr.value)
            curr = curr.next
        return new_list

    def _find_nodes(self, val: T, find_first: bool = False) -> List[Node]:
        """
        Constructs a list of Nodes with value, val, in the DLL and returns the associated Node object list
        :param val: value to be found in the DLL
        :param find_first: if True, find only the first element in the DLL, if False, find all instances of the
            elements in the DLL
        :return: list of Node objects in the DLL whose value is val. If val does not exist in the DLL, returns
            empty list
        """
        all_list = []
        first_list = []
        curr = self.head
        while curr:
            if curr.value == val and find_first is False:
                all_list.append(curr)
            if curr.value == val and find_first is True:
                first_list.append(curr)
                return first_list
            curr = curr.next
        return all_list

    def find(self, val: T) -> Node:
        """
        Finds the first Node with the value 'val' in the DLL and returns the associated Node object
        :param val: value to be found in the DLL
        :return: None
        """
        node_list = self._find_nodes(val, True)

        # is in constant time because there is only one element in the list
        for element in node_list:
            return element

    def find_all(self, val: T) -> List[Node]:
        """
        Finds all Node objects with value 'val' in the DLL and returns a standard Python list of the associated Node
            objects
        :param val: value to be found in the DLL
        :return: standard Python list of all Node objects in the DLL whose value is val. If val does not exist in the
            DLL, returns an empty list
        """
        return self._find_nodes(val)

    def _remove_node(self, to_remove: Node) -> None:
        """
        Removes a Node from the linked list when given a reference to a Node
        :param to_remove: Node to be removed
        :return: None
        """
        # single node case
        if self.head is to_remove and self.tail is to_remove:
            self.head = None
            self.tail = None
            self.size -= 1
            return None
        # removing head
        if self.head is to_remove:
            to_remove.next.prev = None
            self.head = to_remove.next
            to_remove.next = None
            self.size -= 1
            return None
        # removing tail
        if self.tail is to_remove:
            to_remove.prev.next = None
            self.tail = to_remove.prev
            to_remove.prev = None
            self.size -= 1
            return None
        to_remove.prev.next = to_remove.next
        to_remove.next.prev = to_remove.prev
        to_remove.prev = None
        to_remove.next = None
        self.size -= 1
        return None

    def remove(self, val: T) -> bool:
        """
        Removes the first node with value 'val' in the DLL
        :param val: Value to be removed from the DLL
        :return: True if a Node with value 'val' was found and removed from the DLL, else False
        """
        if self.size == 0 or not self.find(val):
            return False

        self._remove_node(self.find(val))
        return True

    def remove_all(self, val: T) -> int:
        """
        Removes all Node objects with teh value 'val' in the DLL
        :param val: Value to be removed from the DLL
        :return: number of Node objects with value 'val' removed from the DLL. If no Node containing 'val' exits in
            the DLL, returns 0
        """
        count = 0
        # removing from empty DLL
        if len(self.find_all(val)) == 0:
            return 0
        while len(self.find_all(val)) > 0:
            self._remove_node(self.find(val))
            count += 1
        return count

    def reverse(self) -> None:
        """
        Reverses the DLL in-place by modifying all next and prev references of Node objects in DLL. Updates self.head
            and self.tail accordingly.
        :return: None
        """
        # reversing empty DLL
        if self.size == 0:
            return None
        # reversing single node DLL
        if self.head is self.tail:
            return None

        curr = self.head
        while curr:
            temp = curr.prev
            curr.prev = curr.next
            curr.next = temp
            curr = curr.prev
        # update head and tail
        temp = self.head
        self.head = self.tail
        self.tail = temp
        return None

def dream_escaper(dll: DLL) -> DLL:
    """
    Turns a multilevel DLL into a single level DLL
    :param dll: A DLL where each Node holds a value of str where the string is the task. The Node may also hold a child
        in .child and store the child DLL to the current node
    :return: a DLL holding a str representing the names of all the tasks
    """
    curr = dll.head
    child_bool = False
    # temp points to the parent.next node
    temp = None
    tail = dll.tail
    temp_tail = False

    while curr:

        # identifies whether there is a child in the dll or not
        if curr.child:
            child_bool = True

        # no children in dll at all
        if curr.next is None and not child_bool:
            return dll

        # if the current node has a child and the next node is not null
        if curr.child and curr.next:
            # remember the parent.next node before pointing to the child
            temp = curr.next
            curr.next = curr.child
            curr.next.prev = curr
            curr.child = None

        # flag whenever the parent.next node is the tail node
        if temp:
            if temp is tail:
                temp_tail = True

        # if the current node has a child and the next node is null
        if curr.child and (curr.next is None):
            curr.next = curr.child
            curr.next.prev = curr
            curr.child = None

        # if the current node doesn't have a child and the next node is null
        if (curr.child is None) and (curr.next is None):
            if temp:
                curr.next = temp
                # prepend to temp
                temp.prev = curr
                temp = None

        # tail node correction/management
        if (curr.next is None) and (curr.child is None):
            # if last node of main dll has child, new tail from child node
            if dll.tail is not curr and not temp_tail:
                dll.tail = curr
            # correction for when the loop has reached the end of the new dll but the last node isn't the tail node
            if dll.tail is not curr and temp_tail:
                curr.next = dll.tail
                dll.tail.prev = curr

        curr = curr.next

    return dll
