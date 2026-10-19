# BASELINE RETRIEVAL METHODS

# IMPORTS
import ast
from importlib import import_module

np = import_module("numpy")
pd = import_module("pandas")
TfidfVectorizer = import_module("sklearn.feature_extraction.text").TfidfVectorizer
cosine_similarity = import_module("sklearn.metrics.pairwise").cosine_similarity
SentenceTransformer = import_module("sentence_transformers").SentenceTransformer

from ingredient_normalisation import normalise_user_ingredients


#conversion to python list
recipes_dataset_normalised = pd.read_csv("recipes_dataset_normalised.csv")
recipes_dataset_normalised.head()
recipes_dataset_normalised["processing_ingredients"] = (recipes_dataset_normalised["processing_ingredients"]
    .apply(ast.literal_eval))


# BASELINE MODEL 1 - TF-IDF with cosine similarity

# for preprocessing ingredients for TFIDF - stops tfidf counting a space as a two seperate words 
def tfidf_ingredients_preprocess(ingredient_list):
    tfidf_ingredients = [ingredient.replace(" ", "_")
        for ingredient in ingredient_list]

    return " ".join(tfidf_ingredients)

# save for tfidf ingredients
recipes_dataset_normalised["tfidf_ingredients"] = (recipes_dataset_normalised["processing_ingredients"] .apply(tfidf_ingredients_preprocess))

# initialise tfidf vectorizer
tfidf_vectorizer = TfidfVectorizer()
# turn every recipe to tfidf vector
tfidf_matrix = tfidf_vectorizer.fit_transform(recipes_dataset_normalised["tfidf_ingredients"])

# function for recommending recipes using tfidf & cosine similarity - return top 5 similarities
def tfidf_model(user_input, top_k=5):

    #  normalise data using dataset 
    user_ingredients = normalise_user_ingredients(user_input)

    # normalise ingredients user enters - same format for tfidf with _
    user_tfidf_text = tfidf_ingredients_preprocess(user_ingredients)

    # user query to a tfidf vector 
    user_vector = tfidf_vectorizer.transform([user_tfidf_text])

    # cosine similarity between user vector & recipe vector
    similarity_scores = cosine_similarity(user_vector, tfidf_matrix).flatten()

    # retrieve highest scoring recipes according to top_k
    top_indices = similarity_scores.argsort()[::-1][:top_k]

    # select those, use copy to create independent DF so original isn't altered
    recommendations = recipes_dataset_normalised.iloc[top_indices].copy()

    # add similarity score in a new column
    recommendations["tfidf_similarity"] = (similarity_scores[top_indices])

    # return only relevant information
    return recommendations[
        ["recipe_title", "processing_ingredients", "tfidf_similarity"]]


# BASELINE MODEL 2 - JACCARD SIMILARITY
# function for jaccard similarity calculation
def jaccard_similarity(user_ingredients, recipe_ingredients):

    # convert user ingredient list to set
    user_set = set(user_ingredients)
    # convert recipe ingredient list to a set
    recipe_set = set(recipe_ingredients)

    # find ingredients appearing in both user ingredients list and recioe 
    intersection = user_set.intersection(recipe_set)
    # find all unique ingredients appearing in either user query or recipe
    union = user_set.union(recipe_set)

    # prevent div. by0 if both empty
    if len(union) == 0:
        return 0.0
    # calculate jaccard similarity 
    return len(intersection) / len(union)


# function to recommend recipes using jaccard similarity - 
def jaccard_model(user_input, top_k=5):
     # normalise data using dataset 
    user_ingredients = normalise_user_ingredients(user_input)
    

    # calculate similariy score for user query and every recipe
    similarity_scores = (recipes_dataset_normalised["processing_ingredients"]
        .apply(lambda recipe_ingredients:jaccard_similarity(user_ingredients, recipe_ingredients)
        )
    )

    # retrieve higher scoring recipe according to topk
    top_indices = similarity_scores.argsort()[::-1][:top_k]

    # select those, use copy to create independent DF so original isn't altered
    recommendations = recipes_dataset_normalised.iloc[top_indices].copy()

    # add similarity score in a new column
    recommendations["jaccard_similarity"] = (similarity_scores.iloc[top_indices].values)

    # return only relevant information
    return recommendations[
        ["recipe_title", "processing_ingredients", "jaccard_similarity"]]


# BASELINE MODEL 3 - MINILM WITH COSINE SIMILARITY
# function to turn ingredient lists to natural language text (removes brackets etc.)
def minilm_ingredients_preprocess(ingredient_list):
    return ", ".join(ingredient_list)

# add minilm preprocesssing func to every recipe - store in new column
recipes_dataset_normalised["minilm_ingredients"] = (recipes_dataset_normalised["processing_ingredients"]
    .apply(minilm_ingredients_preprocess))


# initialise minilm objects when needed
minilm_encoder = None
recipe_embeddings = None


# function to load minilm and encode recipes once per session
def initialise_minilm():
    global minilm_encoder, recipe_embeddings

    # only initialise if embeddings have not been created
    if recipe_embeddings is None:

        # load pretrained sentence embedding model
        minilm_encoder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

        # encode all recipe ingredient lists
        recipe_embeddings = minilm_encoder.encode(recipes_dataset_normalised["minilm_ingredients"].tolist(), show_progress_bar=False)

def minilm_model(user_input, top_k=5):
    
    # minilm model and recipe embeddings  ready
    initialise_minilm() 

    #  normalise data using dataset 
    user_ingredients = normalise_user_ingredients(user_input)
   

    # convert ingredients into natural text
    user_text = minilm_ingredients_preprocess(user_ingredients)

    # create embedding for user ingredients query
    user_embedding = minilm_encoder.encode([user_text])

    # calculate cosine similarity btwn user embedding and recipe embedding
    similarity_scores = cosine_similarity(user_embedding, recipe_embeddings).flatten()

    # retrieve higher scoring recipe according to topk
    top_indices = similarity_scores.argsort()[::-1][:top_k]

    # select those, use copy to create independent DF so original isn't altered
    recommendations = recipes_dataset_normalised.iloc[top_indices].copy()

    # add miniLM similarity score in new column
    recommendations["minilm_similarity"] = (similarity_scores[top_indices])

    # return only relevant information
    return recommendations[
        ["recipe_title", "processing_ingredients", "minilm_similarity"]]


