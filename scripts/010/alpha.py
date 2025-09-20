def levenshtein_distance(s1, s2):
    """
    Calculates the Levenshtein distance between two strings using dynamic programming.

    The Levenshtein distance is the minimum number of single-character edits
    (insertions, deletions or substitutions) required to change one word into the other.

    Args:
        s1: The first string.
        s2: The second string.

    Returns:
        The Levenshtein distance between the two strings.
    """
    m, n = len(s1), len(s2)

    # Initialize a DP matrix (m+1 rows, n+1 columns)
    # dp[i][j] will be the Levenshtein distance between the first i chars of s1
    # and the first j chars of s2
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Initialize the first row and column of the matrix
    # The distance from an empty string to a string of length j is j
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    # Fill in the rest of the matrix
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # If the characters are the same, the cost is 0, otherwise it's 1
            cost = 0 if s1[i - 1] == s2[j - 1] else 1

            # The value at dp[i][j] is the minimum of three operations:
            # 1. Deletion: dp[i-1][j] + 1
            # 2. Insertion: dp[i][j-1] + 1
            # 3. Substitution: dp[i-1][j-1] + cost
            dp[i][j] = min(dp[i - 1][j] + 1,        # Deletion
                           dp[i][j - 1] + 1,        # Insertion
                           dp[i - 1][j - 1] + cost) # Substitution

    # The final distance is in the bottom-right cell
    return dp[m][n]

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
