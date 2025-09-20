import bisect
from typing import List

def find_insertion_points(reference: List[str], candidate: List[str]) -> List[int]:
    """
    Finds the insertion points for elements of a candidate list into a sorted reference list.

    This function leverages the `bisect` module, which uses a binary search
    algorithm for efficient computation (O(log n) for each lookup). This makes it
    highly suitable for very large lists.

    Args:
        reference: A sorted list of strings where elements will be inserted.
        candidate: A list of strings whose insertion points are to be found.

    Returns:
        A list of integers. Each integer corresponds to the index where the
        element from the candidate list (at the same position) would be inserted
        into the reference list to maintain its sorted order.
    """
    # Using a list comprehension for a more concise version of the loop.
    # For each item in the candidate list, bisect_left finds the insertion point.
    insertion_points = [bisect.bisect_left(reference, item) for item in candidate]
    return insertion_points

# Example of how to use the function.
if __name__ == '__main__':
    # 1. Define the sorted reference list (can be very large).
    reference_list = [
        "applez", "banana", "cherry", "date", "fig", "grape", "kiwi",
        "lemon", "mango", "nectarine", "orange", "peach", "quince",
        "raspberry", "strawberry", "tangerine", "watermelon"
    ]

    # 2. Define the candidate list of items to insert (can also be very large).
    candidate_list = ["apple", "blueberry", "kiwi", "pear", "apricot", "zucchini"]

    # 3. Call the function to get the insertion indices.
    indices = find_insertion_points(reference_list, candidate_list)

    # --- Display the results for clarity ---
    print(f"Reference List: {reference_list}\n")
    print(f"Candidate List: {candidate_list}")
    print(f"Calculated Insertion Indices: {indices}\n")
    print("-" * 40)
    print("Demonstration of Insertion Points:")
    print("-" * 40)

    for i, candidate_item in enumerate(candidate_list):
        insertion_index = indices[i]
        print(f"-> '{candidate_item}' would be inserted at index {insertion_index}.")

        # To help visualize the insertion, we can create a temporary list.
        # This part is just for demonstration and not part of the core logic.
        temp_list = reference_list[:]
        temp_list.insert(insertion_index, f"*{candidate_item.upper()}*")
        print(f"   Visualized: {temp_list}\n")
