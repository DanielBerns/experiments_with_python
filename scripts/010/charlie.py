def levenshtein_distance(s1, s2):
    """
    Calculates the Levenshtein distance between two strings using dynamic programming.
    This version is optimized for space, using O(min(len(s1), len(s2))) space.

    The Levenshtein distance is the minimum number of single-character edits
    (insertions, deletions or substitutions) required to change one word into the other.

    Args:
        s1: The first string.
        s2: The second string.

    Returns:
        The Levenshtein distance between the two strings.
    """
    m, n = len(s1), len(s2)

    # To optimize space, we want the outer loop to be over the longer string
    # and our DP rows to be the size of the shorter string.
    if m < n:
        s1, s2 = s2, s1
        m, n = n, m

    # We only need to keep track of the previous row to compute the current row.
    # `prev_row` is initialized to the distance from an empty string.
    prev_row = list(range(n + 1))

    # Fill in the conceptual matrix row by row
    for i in range(1, m + 1):
        # `current_row` will be built based on `prev_row`.
        # The first element of the current row is `i` (deletions from s1).
        current_row = [i] * (n + 1)
        for j in range(1, n + 1):
            # If the characters are the same, the cost is 0, otherwise it's 1
            cost = 0 if s1[i - 1] == s2[j - 1] else 1

            # The value is the minimum of three operations:
            deletion = prev_row[j] + 1
            insertion = current_row[j - 1] + 1
            substitution = prev_row[j - 1] + cost
            current_row[j] = min(deletion, insertion, substitution)

        # The current row becomes the previous row for the next iteration
        prev_row = current_row

    # The final distance is the last element of the last computed row
    return prev_row[n]

# --- Example Usage ---
if __name__ == "__main__":
    string1 = "kitten"
    string2 = "sitting"
    distance = levenshtein_distance(string1, string2)
    print(f"The Levenshtein distance between '{string1}' and '{string2}' is: {distance}")

    string3 = "flaw"
    string4 = "lawn"
    distance2 = levenshtein_distance(string3, string4)
    print(f"The Levenshtein distance between '{string3}' and '{string4}' is: {distance2}")

    string5 = "saturday"
    string6 = "sunday"
    distance3 = levenshtein_distance(string5, string6)
    print(f"The Levenshtein distance between '{string5}' and '{string6}' is: {distance3}")

    string1 = "paparota"
    string2 = "nullklusen"
    distance = levenshtein_distance(string1, string2)
    print(f"The Levenshtein distance between '{string1}' and '{string2}' is: {distance}")


    string1 = "aceite de girasol cañuelas 1.5 lt"
    string2 = "aceite de girasol cañuelas 900 cc"
    distance = levenshtein_distance(string1, string2)
    print(f"The Levenshtein distance between '{string1}' and '{string2}' is: {distance}")
