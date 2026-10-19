# AIML339_FINAL

 1. Requirements

 - python, jupyter : project run on VScode but any python + jupyter code base
- CPU program, GPU not required.

python libraries (to be installed before running notebook):

- pandas
- numpy
- scikit-learn
- sentence-transformers
- scipy
- matplotlib
- Jupyter / ipykernel

3. Data Prepartion

A 10,000 recipe randomly extracted subset of the RecipeNLG dataset was used. The subset used, and additionally it's normalised version have been uploaded. The subset is normalised before the model uses it, and it will be saved as it's normalised dataset, and that is what the project uses. This normalisation is also applied to the user query. Considering the subset was randomly selected, and the original dataset is 2,000,000 recipes, it has not been uploaded.
relevant columns
`title`: Recipe name
`NER`: Extracted ingredient names
`ingredients`: Original ingredient quantities and descriptions
`directions`: Recipe preparation instructions

4. How to run model/system
The file system can be run in the following order 
Main models: 
1. normalisation.ipynb 
2. baseline_models.ipynb
3. reranking.ipynb
4. reranking_v2.ipynb
5. reranking_v3.ipynb
6. reranking_v4.ipynb

Evaluation notebooks <- AFTER ALL MAIN MODELS HAVE RUN
1. baseeline_tests.ipynb 
2. evaluation1.ipynb 
3. evaluation2.ipynb 
4. evaluation3.ipynb 
5. evaluation4.ipynb 
7. v2_configuration_validation.ipynb
8. v2_weight_testing_random_and_manual.ipynb
9. final_test. ipynb
10. statistical_analysis copy.ipynb

-PYTHON MODULES
- baseline_retrieval.py - reusable baseline retrieval functions
- ingredient_normalisation.py - reusable preprocessing functions
- evaluation_queries.py - reusable to generate manual and synthetic queries

Running the Project

Open project folder -> select kernel -> ensure libraries installed -> ensure dataset + python modules available -> open notebooks in that order, all evaluations can be done after main <- run all in order above
- some evaluations (repeated seeds, MiniLM) tend to take longer because of CPU - notebook outputs have been kept so results can be viewed without running everything

4. WHAT CORRESPONDS TO REPORT:

-CSV files generated during preprocessing
- baseline demonstrations
- evaluation validation and final testing <- .csv's generated for these as well

these files have also been kept so they can be viewed without rerunning everything.
 PLEASE NOTE - notebooks autogenerate CSV files, if this is rerun, existing files may be overwritten, and may not correspond exactly in terms of exact numbers to the report.

NOTE: runtime may differ based on CPU/hardware
