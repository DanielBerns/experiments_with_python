import bisect
from typing import List, Tuple, Optional

def find_insertion_context(reference: List[str], candidate: List[str]) -> List[Tuple[Optional[str], str, Optional[str]]]:
    """
    For each element in the candidate list, finds its insertion point in the
    sorted reference list and returns the element, along with the elements
    immediately before and after the insertion point.

    This function leverages the `bisect` module for efficient O(log n) lookups,
    making it suitable for very large lists.

    Args:
        reference: A sorted list of strings where context will be found.
        candidate: A list of strings to find context for.

    Returns:
        A list of tuples. Each tuple contains three elements:
        - The element from the reference list just before the insertion point (or None).
        - The element from the candidate list.
        - The element from the reference list at the insertion point (or None).
    """
    results = []
    for item in candidate:
        # Find the insertion point using binary search.
        # This is the index where 'item' would be inserted.
        ip = bisect.bisect_left(reference, item)

        # Determine the element before the insertion point, handling the edge case
        # where the insertion point is at the beginning of the list.
        before = reference[ip - 1] if ip > 0 else None

        # Determine the element after the insertion point, handling the edge case
        # where the insertion point is at the end of the list.
        after = reference[ip] if ip < len(reference) else None

        results.append((before, item, after))
    return results

def compare(red: str, blue: str) -> Tuple[int, int]:
    idx = 0
    for rr, bb in zip(red, blue):
        if rr == bb:
            idx += 1
        else:
            break
    return (idx, min(len(red), len(blue)))

# Example of how to use the function.
if __name__ == '__main__':
    # 1. Define the sorted reference list (can be very large).
    reference_list = [
        "apple", "banana", "cherry", "date", "fig", "grape", "kiwi",
        "lemon", "mango", "nectarine", "orange", "peach", "quince",
        "raspberry", "strawberry", "tangerine", "watermelon"
    ]

    # 2. Define the candidate list of items to find context for (can also be very large).
    candidate_list = ["abba", "blueberry", "kiwi", "pear", "apricot", "zucchini"]

    # 3. Call the function to get the insertion contexts.
    contexts = find_insertion_context(reference_list, candidate_list)

    # --- Display the results for clarity ---
    print(f"Reference List: {reference_list}\n")
    print(f"Candidate List: {candidate_list}\n")
    print("-" * 40)
    print("Insertion Context Results:")
    print("-" * 40)

    for before, candidate_item, after in contexts:
        # Format the output to be readable, handling None for edge cases.
        before_str = before if before else "N/A (start of list)"
        after_str = after if after else "N/A (end of list)"
        print(f"For '{candidate_item}':")
        print(f"  Context: ({before_str}, '{candidate_item}', {after_str})\n")
        (idx, size) = compare(before_str, candidate_item)
        print(f"  {before_str, candidate_item}: {idx} - {size}")
        (idx, size) = compare(after_str, candidate_item)
        print(f"  {after_str, candidate_item}: {idx} - {size}")

