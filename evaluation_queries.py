

# EVALUATION QUERIES

# IMPORTS
import hashlib
import random
import pandas as pd

# query lengths, seeds and number of source recipes for evaluation
QUERY_LENGTHS = (3, 4, 5, 6)
SPLIT_SEED = 34
VALIDATION_SEED = 83
NUMBER_OF_QUERIES = 50
MIN_SOURCE_INGREDIENTS = min(QUERY_LENGTHS)

# fixed ingredient groups for manual queries
MANUAL_QUERY_GROUPS = {
    "tomato_pasta": ["pasta", "tomato", "garlic", "onion", "olive oil", "basil"],
    "white_cake": ["flour", "sugar", "egg", "butter", "milk", "vanilla"],
    "mashed_potatoes": ["potato", "butter", "salt", "pepper", "milk", "onion"],
    "tomato_chilli": ["cumin", "onion", "garlic", "tomato", "chili powder", "salt"],
    "beef_rice": ["rice", "beef", "onion", "salt", "pepper", "tomato"],
}

# MANUAL QUERIES
# function to create manual queries - longer queries add ingredients to shorter queries
def make_manual_queries(query_lengths=QUERY_LENGTHS):
    """Return fixed, nested manual queries."""
    # store query information for each group and query length
    rows = []
    for group, ingredients in MANUAL_QUERY_GROUPS.items():
        for n in query_lengths:
            # check group has enough ingredients for query length
            if n > len(ingredients):
                raise ValueError(f"{group} contains only {len(ingredients)} ingredients")
            # select first n ingredients and save query information
            rows.append({
                "query_id": f"{group}_{n}",
                "group": group,
                "query_length": n,
                "query": ", ".join(ingredients[:n]),
            })
    # return queries as a DF
    return pd.DataFrame(rows)


# RANDOM QUERIES
# function to create repeatable queries using validation or test source recipes
def make_random_queries(
    recipes,
    partition="validation",
    query_lengths=QUERY_LENGTHS,
    number_of_queries=NUMBER_OF_QUERIES,
    split_seed=SPLIT_SEED,
    query_seed=VALIDATION_SEED,
    min_source_ingredients=MIN_SOURCE_INGREDIENTS,
):
    
    # check partition, query lengths, query count and recipe indices
    if partition not in ("validation", "test"):
        raise ValueError("partition must be 'validation' or 'test'")
    lengths = tuple(query_lengths)
    if not lengths or any(not isinstance(n, int) or n < 1 for n in lengths):
        raise ValueError("query_lengths must contain positive integers")
    if number_of_queries < 1:
        raise ValueError("number_of_queries must be positive")
    if not recipes.index.is_unique:
        raise ValueError("Recipe DataFrame indices must be unique")

    # keep minimum ingredient count the same for validation and test split
    if min_source_ingredients > min(lengths):
        raise ValueError(
            "min_source_ingredients must not exceed the shortest query length; "
            "change notebook MIN_SOURCE_INGREDIENTS to 3"
        )

    # select recipes with enough unique ingredients
    eligible = [
        idx for idx, ingredients in recipes["processing_ingredients"].items()
        if len(set(ingredients)) >= min_source_ingredients
    ]
    # shuffle using split seed so validation and test recipes stay the same each run
    random.Random(split_seed).shuffle(eligible)
    # split source recipes into separate validation and test halves
    midpoint = len(eligible) // 2
    partition_indices = eligible[:midpoint] if partition == "validation" else eligible[midpoint:]

    # select source recipes with enough ingredients for longest query
    available = [
        idx for idx in partition_indices
        if len(set(recipes.at[idx, "processing_ingredients"])) >= max(lengths)
    ]
    # check there are enough source recipes for requested query count
    if number_of_queries > len(available):
        raise ValueError(
            f"Only {len(available)} eligible source recipes for "
            f"length {max(lengths)} in {partition}"
        )

    # sample same source recipes for every query length using query seed
    rng = random.Random(query_seed)
    source_indices = rng.sample(available, number_of_queries)
    rows = []

    for query_number, source_index in enumerate(source_indices, start=1):
        # remove duplicate ingredients and sort before shuffling
        ingredients = sorted(set(recipes.at[source_index, "processing_ingredients"]))
        # create repeatable seed for each source recipe using query seed and recipe index
        seed_bytes = f"{query_seed}:{source_index}".encode("utf-8")
        recipe_seed = int.from_bytes(hashlib.sha256(seed_bytes).digest()[:8], "big")
        # shuffle ingredients once - longer queries extend shorter queries
        ordered = random.Random(recipe_seed).sample(ingredients, len(ingredients))

        # select first n ingredients and save query information
        for n in lengths:
            rows.append({
                "query_id": f"{partition}_{query_number:03d}_{n}",
                "partition": partition,
                "query_number": query_number,
                "source_index": source_index,
                "query_length": n,
                "query": ", ".join(ordered[:n]),
                "split_seed": split_seed,
                "query_seed": query_seed,
            })
    # return queries as DF
    return pd.DataFrame(rows)
