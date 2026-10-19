# INGREDINT NORMALISATION 
import re

unnecessary_words = {
    # Preparation words
    "beaten",
    "blanched",
    "boned",
    "chopped",
    "cleaned",
    "cored",
    "crumbled",
    "crushed",
    "cubed",
    "cut",
    "diced",
    "divided",
    "drained",
    "grated",
    "grnd",
    "ground",
    "halved",
    "juiced",
    "mashed",
    "minced",
    "pared",
    "peeled",
    "pitted",
    "pressed",
    "quartered",
    "rinsed",
    "scraped",
    "seeded",
    "shaved",
    "shredded",
    "skinned",
    "sliced",
    "slivered",
    "snipped",
    "squeezed",
    "stemmed",
    "torn",
    "trimmed",
    "washed",
    "carefully",
    "coarsely",
    "finely",
    "freshly",
    "gently",
    "lightly",
    "loosely",
    "roughly",
    "slightly",
    "stiffly",
    "thinly",
    "thoroughly",
    "chilled",
    "cold",
    "cooled",
    "cool",
    "warm",
    "boiling",
    "heated",
    "cooled",
    "lukewarm",
    "room-temperature",
    "room_temperature",
    "finely",
    "roughly",
    "thinly",
    "coarsely",
    "softened",
    "melted",
    "rinsed",
    "drained",
    "peeled",
    "seeded",
    "pitted",
    "zested",
    "julienned",
    "deveined",
    "cored",
    "trimmed",
    "bunch",
    "bunches",
    "dash",
    "drop",
    "drops",
    "generous",
    "handful",
    "handfuls",
    "pinch",
    "sprig",
    "sprigs",
    "bag",
    "bags",
    "bottle",
    "bottles",
    "box",
    "boxes",
    "can",
    "cans",
    "jar",
    "jars",
    "package",
    "packages",
    "packet",
    "packets",
    "additional",
    "approximately",
    "desired",
    "needed",
    "optional",
    "preferably",
    "remaining",
    "reserved",
    "serving"
}


def remove_unnecessary_words(ingredient):
    words = ingredient.split()

    cleaned_words = [
        word for word in words
        if word not in unnecessary_words
    ]

    return " ".join(cleaned_words).strip()




# remove remaining quantity and measurement artefacts

def remove_quantity_noise(ingredient):

    # remove standalone unicode fractions
    ingredient = re.sub(
        r"(?<!\w)[¼½¾⅓⅔⅛⅜⅝⅞](?!\w)",
        " ",
        ingredient
    )

    # remove numeric quantities, including decimals and fractions
    ingredient = re.sub(
        r"\b\d+(?:[./]\d+)?\b",
        " ",
        ingredient
    )

    # remove standalone measurement units
    ingredient = re.sub(
        r"\b(?:tsp|tbsp|teaspoon|teaspoons|tablespoon|tablespoons|"
        r"cup|cups|oz|ounce|ounces|lb|lbs|pound|pounds|"
        r"gram|grams|kg|ml|litre|litres)\b",
        " ",
        ingredient
    )

    # remove isolated punctuation and underscores
    ingredient = re.sub(r"[_+*]+", " ", ingredient)

    # remove extra whitespace
    ingredient = re.sub(r"\s+", " ", ingredient).strip()

    # discard known incomplete or meaningless ingredient entries
    invalid_ingredients = {
        "",
        "t",
        "o",
        "ingredients",
        "ingredient",
        "skinless",
        "all-purpose"
    }

    if ingredient in invalid_ingredients:
        return ""

    return ingredient
    
plural_to_singular = {
    "almonds": "almond",
    "anchovies": "anchovy",
    "apples": "apple",
    "apricots": "apricot",
    "artichokes": "artichoke",
    "aubergines": "aubergine",
    "avocadoes": "avocado",
    "avocados": "avocado",
    "bananas": "banana",
    "beans": "bean",
    "beets": "beet",
    "berries": "berry",
    "blackberries": "blackberry",
    "blueberries": "blueberry",
    "boysenberries": "boysenberry",
    "breasts": "breast",
    "cabbages": "cabbage",
    "candies": "candy",
    "cantaloupes": "cantaloupe",
    "carrots": "carrot",
    "cashews": "cashew",
    "cauliflowers": "cauliflower",
    "cherries": "cherry",
    "chestnuts": "chestnut",
    "chickens": "chicken",
    "chickpeas": "chickpea",
    "chiles": "chile",
    "chilies": "chili",
    "chillies": "chilli",
    "clams": "clam",
    "clementines": "clementine",
    "cloves": "clove",
    "coconuts": "coconut",
    "courgettes": "courgette",
    "cranberries": "cranberry",
    "cucumbers": "cucumber",
    "currants": "currant",
    "dates": "date",
    "eggplants": "eggplant",
    "eggs": "egg",
    "endives": "endive",
    "figs": "fig",
    "fillets": "fillet",
    "flaxseeds": "flaxseed",
    "florets": "floret",
    "frankfurters": "frankfurter",
    "garlics": "garlic",
    "gherkins": "gherkin",
    "grapefruits": "grapefruit",
    "grapes": "grape",
    "hazelnuts": "hazelnut",
    "hens": "hen",
    "jalapenos": "jalapeno",
    "kernels": "kernel",
    "kiwis": "kiwi",
    "kumquats": "kumquat",
    "leaves": "leaf",
    "leeks": "leek",
    "lemons": "lemon",
    "lentils": "lentil",
    "lettuces": "lettuce",
    "limes": "lime",
    "livers": "liver",
    "loaves": "loaf",
    "lobsters": "lobster",
    "mangoes": "mango",
    "mangos": "mango",
    "marshmallows": "marshmallow",
    "meatballs": "meatball",
    "muffins": "muffin",
    "mushrooms": "mushroom",
    "mussels": "mussel",
    "nectarines": "nectarine",
    "noodles": "noodle",
    "nuts": "nut",
    "olives": "olive",
    "onions": "onion",
    "oranges": "orange",


    "oysters": "oyster",
    "papayas": "papaya",
    "parsnips": "parsnip",
    "patties": "patty",
    "peaches": "peach",
    "peanuts": "peanut",
    "pears": "pear",
    "peas": "pea",
    "pecans": "pecan",
    "peppercorns": "peppercorn",
    "peppers": "pepper",
    "pickles": "pickle",
    "pineapples": "pineapple",
    "pistachios": "pistachio",
    "plantains": "plantain",
    "plums": "plum",
    "potatoes": "potato",
    "prawns": "prawn",
    "prunes": "prune",
    "radishes": "radish",
    "tomatoes": "tomato",
    "shallots": "shallot",
    "yolks": "yolk",
    "whites": "white",
    "raisins": "raisin",
    "chips": "chip",
    "seeds": "seed",
    "strawberries": "strawberry",
    "crackers": "cracker",
    "chives": "chive",
    "tortillas": "tortilla",
    "flakes": "flake",
    "pimentos": "pimento",
    "pimientos": "pimiento",
    "sticks": "stick",
    "chops": "chop",
    "thighs": "thigh",
    "cubes": "cube",
    "wedges": "wedge",
    "ribs": "rib",
    "drumsticks": "drumstick",
    "wings": "wing",
    "scallops": "scallop",
    "sausages": "sausage",
    "biscuits": "biscuit",
    "cookies": "cookie",
    "rolls": "roll",
    "buns": "bun",
    "pancakes": "pancake",
    "walnuts": "walnut",
    "pizzas": "pizza",
    "zucchinis": "zucchini",
    "tomatillos": "tomatillo",
    "chilies": "chili",
    "chillies": "chilli",
    "chilis": "chili",
    "radicchios": "radicchio",
    "asparagus": "asparagus"
    }


def singularise_ingredient(ingredient):
    words = ingredient.split()

    # Check every word so multi-word ingredients also work
    words = [plural_to_singular.get(word, word)
        for word in words]

    return " ".join(words)


synonym_map = {
        # pasta shapes mapped to the general ingredient "pasta"
    "penne": "pasta",
    "penne pasta": "pasta",
    "fusilli": "pasta",
    "fusilli pasta": "pasta",
    "farfalle": "pasta",
    "farfalle pasta": "pasta",
    "rigatoni": "pasta",
    "rigatoni pasta": "pasta",
    "spaghetti": "pasta",
    "spaghetti pasta": "pasta",
    "macaroni": "pasta",
    "elbow macaroni": "pasta",
    "linguine": "pasta",
    "linguine pasta": "pasta",
    "fettuccine": "pasta",
    "fettuccine pasta": "pasta",
    "tagliatelle": "pasta",
    "tagliatelle pasta": "pasta",
    "pappardelle": "pasta",
    "pappardelle pasta": "pasta",
    "rotini": "pasta",
    "rotini pasta": "pasta",
    "ziti": "pasta",
    "ziti pasta": "pasta",
    "bucatini": "pasta",
    "bucatini pasta": "pasta",
    "orzo": "pasta",
    "orzo pasta": "pasta",
    "cavatappi": "pasta",
    "cavatappi pasta": "pasta",
    "conchiglie": "pasta",
    "shell pasta": "pasta",
    "pasta shells": "pasta",
    "angel hair pasta": "pasta",
    "angel hair": "pasta",
    "vermicelli pasta": "pasta",
    "lasagna noodles": "pasta",
    "lasagne sheets": "pasta",
    "lasagna sheets": "pasta",
    
    "bell pepper": "capsicum",
    "scallion": "green onion",
    "spring onion": "green onion",
    "aubergine": "eggplant",
    "courgette": "zucchini",
    "garbanzo bean": "chickpea",
    "icing sugar": "powdered sugar",
    "confectioners sugar": "powdered sugar",
    "confectioner sugar": "powdered sugar",
    "confectionery sugar": "powdered sugar",
    "rocket": "arugula",
    "prawn": "shrimp",
    "rockmelon": "cantaloupe",
    "catsup": "ketchup",
    "bread crumbs": "breadcrumbs",
    "bread crumb": "breadcrumbs",
    "parmesan": "parmesan cheese",
    "cheddar": "cheddar cheese",
    "mozzarella": "mozzarella cheese",
    "mayo": "mayonnaise",
    "corn starch": "cornstarch",
    "baking pwdr": "baking powder",
    "superfine sugar": "caster sugar",
    "gingerroot": "ginger",
    "ginger root": "ginger",
    "lemon rind": "lemon zest",
    "orange rind": "orange zest",
    "crabmeat": "crab meat",
    "cider vinegar": "apple cider vinegar",
    "pimiento": "pimento",
    "pimientos": "pimento",
    "pimentoes": "pimento",
    "chilli": "chili",
    "green scallion": "green onion",
    "cherry tomatoes": "cherry tomato",
    "plum tomatoes": "plum tomato",
    "roma tomatoes": "roma tomato",
    "fresh mozzarella": "mozzarella cheese"
}


# map ingredient synonyms without accidentally replacing parts of words

def map_synonyms(ingredient):

    # check for a synonym matching the complete ingredient name
    if ingredient in synonym_map:
        return synonym_map[ingredient]

    # otherwise leave the ingredient unchanged
    return ingredient.strip()

# normalise ingredients entered by the user

def normalise_user_ingredients(user_input):

    # split comma-separated ingredients, lowercase and strip whitespace
    ingredients = [
        ingredient.strip().lower()
        for ingredient in user_input.split(",")
        if ingredient.strip()
    ]

    # remove preparation and descriptive words
    ingredients = [
        remove_unnecessary_words(ingredient)
        for ingredient in ingredients
    ]

    # remove quantities, measurements and noise
    ingredients = [
        remove_quantity_noise(ingredient)
        for ingredient in ingredients
    ]

    # convert plurals to singular ingredient names
    ingredients = [
        singularise_ingredient(ingredient)
        for ingredient in ingredients
    ]

    # map synonyms to canonical ingredient names
    ingredients = [
        map_synonyms(ingredient)
        for ingredient in ingredients
    ]

    # remove empty ingredients and duplicates
    ingredients = list(dict.fromkeys(
        ingredient for ingredient in ingredients
        if ingredient
    ))

    return ingredients