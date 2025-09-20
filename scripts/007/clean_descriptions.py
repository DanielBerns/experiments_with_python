import re
from collections import defaultdict

def generate_descriptors(descriptions):
    """
    Analyzes a list of article descriptions to generate a hierarchical list of descriptors.

    The function identifies two types of descriptors:
    1.  Base Descriptions: The core product name with quantities, units, and prices removed.
    2.  Branch Descriptors: Common prefixes that represent categories for multiple products.

    Args:
        descriptions (list[str]): A list of article description strings.

    Returns:
        list[str]: A sorted list of unique descriptor strings.
    """
    # Define words to be removed from the end of descriptions (units, packaging, etc.)
    stop_words = {
        'lt', 'l', 'cc', 'ml', 'g', 'kg', 'gr', 'pet', 'sport', 'bidon', 'cero', 'en'
    }

    # --- Step 1: Clean descriptions to get the "base" product name ---
    # This removes price information and trailing words like units or quantities.
    base_descriptions = set()
    for desc in descriptions:
        # Remove the price part (e.g., ": 42") using regex
        clean_desc = re.sub(r':\s*\d+\s*$', '', desc).strip()
        words = clean_desc.split()

        # Remove trailing stop words and numbers from the end of the list
        while words:
            last_word = words[-1].lower()
            # Check if the last word is a number or a stop word
            if last_word.isnumeric() or re.match(r'^\d+(\.\d+)?$', last_word) or last_word in stop_words:
                words.pop()
            else:
                break

        if words:
            base_descriptions.add(" ".join(words))

    # --- Step 2: Identify "branch" prefixes that act as categories ---
    # A prefix is a "branch" if it is the start of at least two descriptions
    # that continue with different next words.
    # For example, "agua saborizada" is a branch because it's followed by
    # "limonada", "manzana", "pera", etc.

    # Find all possible prefixes from all base descriptions
    all_prefixes = set()
    for desc in base_descriptions:
        words = desc.split()
        for i in range(1, len(words)):
            all_prefixes.add(" ".join(words[:i]))

    branch_prefixes = set()
    for prefix in all_prefixes:
        next_words = set()
        prefix_with_space = prefix + ' '
        # Find all base descriptions that start with this prefix
        for desc in base_descriptions:
            if desc.startswith(prefix_with_space):
                # Get the word immediately following the prefix
                suffix = desc[len(prefix_with_space):]
                if suffix: # Ensure there is a next word
                    next_word = suffix.split()[0]
                    next_words.add(next_word)

        # If there is more than one unique "next word", it's a branch
        if len(next_words) > 1:
            branch_prefixes.add(prefix)

    # --- Step 3: Combine base descriptions and branch prefixes ---
    # The final list includes all unique products and the categories they belong to.
    final_descriptors = base_descriptions.union(branch_prefixes)

    return sorted(list(final_descriptors))

# --- Example Usage ---

# # Your example list of article descriptions
# article_descriptions = [
#     "agua mineral sin gas eco de los andes 1 lt: 42",
#     "agua mineral sin gas eco de los andes 2 lt: 68",
#     "agua mineral sin gas eco de los andes 500 cc: 77",
#     "agua mineral sin gas eco de los andes 850 ml: 24",
#     "agua mineral sin gas en bidon nestle 6.3 lt: 69",
#     "agua mineral sin gas glaciar 750 cc: 61",
#     "agua mineral sin gas nestle pureza vital 500 cc: 73",
#     "agua mineral sin gas orizon 2.25 lt: 39",
#     "agua mineral sin gas orizon 6.25 lt: 44",
#     "agua mineral sin gas pet villavicencio 1.5 lt: 69",
#     "agua mineral sin gas pet villavicencio 2 lt: 71",
#     "agua mineral sin gas villa del sur 2.25 lt: 72",
#     "agua mineral sin gas villa del sur 600 cc: 56",
#     "agua mineral sin gas villavicencio sport 750 cc: 42",
#     "agua mineralizada sin gas cellier favaloro 2 lt: 84",
#     "agua mineralizada sin gas glaciar 2 lt: 73",
#     "agua mineralizada sin gas glaciar 500 cc: 83",
#     "agua saborizada limonada sin gas aquarius 1.5 lt: 36",
#     "agua saborizada limonada sin gas aquarius 500 cc: 66",
#     "agua saborizada manzana sin gas aquarius 1.5 lt: 83",
#     "agua saborizada manzana sin gas aquarius 2.25 lt: 83",
#     "agua saborizada manzana sin gas aquarius 500 cc: 58",
#     "agua saborizada manzana sin gas levite 1.5 lt: 65",
#     "agua saborizada manzana sin gas levite 2.25 lt: 65",
#     "agua saborizada manzana sin gas levite cero 1.5 lt: 67",
#     "agua saborizada manzana sin gas levite cero 2.25 lt: 45",
#     "agua saborizada manzana sin gas villa del sur levite 500 cc: 77",
#     "agua saborizada naranja aquarius 2.25 lt: 81",
#     "agua saborizada naranja sin gas aquarius 1.5 lt: 81",
#     "agua saborizada naranja sin gas aquarius 500 cc: 73",
#     "agua saborizada naranja sin gas levite 1.5 lt: 73",
#     "agua saborizada naranja sin gas levite cero 1.5 lt: 66",
#     "agua saborizada naranja sin gas levite cero 2.25 lt: 61",
#     "agua saborizada naranja sin gas sierra de los padres 1.5 lt: 51",
#     "agua saborizada naranja sin gas villa del sur levite 2.25 lt: 75",
#     "agua saborizada pera sin gas aquarius 1.5 lt: 78",
#     "agua saborizada pera sin gas aquarius 2.25 lt: 74",
#     "agua saborizada pera sin gas aquarius 500 cc: 65",
#     "agua saborizada pera sin gas levite 1.5 lt: 60",
#     "agua saborizada pomelo sin gas aquarius 1.5 lt: 84",
#     "agua saborizada pomelo sin gas aquarius 2.25 lt: 81",
#     "agua saborizada pomelo sin gas aquarius 500 cc: 69",
#     "agua saborizada pomelo sin gas levite 1.5 lt: 80",
#     "agua saborizada pomelo sin gas levite cero 1.5 lt: 67",
#     "agua saborizada pomelo sin gas levite cero 2.25 lt: 70",
#     "agua saborizada pomelo sin gas villa del sur levite 500 cc: 84",
#     "agua saborizada sin gas pera levite villa sur 500 cc: 62",
#     "agua saborizada uva aquarius 500 cc: 26",
#     "agua sin gas bidon glaciar 6.3 lt: 78",
# ]
#

try:
    with open('articles.txt', 'r', encoding='utf-8') as f:
        article_descriptions = f.read().splitlines()
except FileNotFoundError:
    print("Error: articles.txt not found. Using the example list.")


# Generate the descriptors
descriptors = generate_descriptors(article_descriptions)

# Print the result
for descriptor in descriptors:
    print(descriptor)

