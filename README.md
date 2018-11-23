## Bikes Assignment ##

[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/a-torrano-m/BikeZeus/master)

BikeZeus is a repository of all my Jupyter Notebooks for the assignment.
Each Jupyter contains python code and/or text solving each one of the questions.
Besides, some notebooks will render heatmaps on the fly ( please follow above [launch|BINDER] link to see them ).
So, there is no need to download any source code and run it in local. But in case it was needed,
all scripts could be executed from their own under 'src' directory.

Directory contents:

data/HOSCO 	: MongoDB dump files for retrieved snapshots of stations. Each five minutes during 
twenty four hours the script stored a snapshot.

html 		: Target directory where script from Question 2 writes its resulting rendered heatmaps as 
html files.

img  		: Some figures used by the Jupyter Notebooks.

src  		: Source directory. There is a subdirectory for each question. Scripts must be ran from 
their own directory.

./BikesNotebook_question0.ipynb		: Data retrieval part for answering question 2.

./BikesNotebook_question1.ipynb		: Answer to question 1.

./BikesNotebook_question2.ipynb		: Answer to question 2 ( follow above [launch-BINDER] link 
in order to get the embedded maps and figures). Maps are DRAGGABLE and ZOOMABLE.

./BikesNotebook_question2_SIMUL.ipynb	: Solution to question 2 from the Operations Research/Simulation
point of view. It is possible to map the district and estimate mean commute time for each point in a grid
spanning all Gracia district under the parameters of time constraints, bikes, and depleted stations.
(under construnction)

./BikesNotebook_question3.ipynb		: Answer to question 3, plain explation with a simple diagram.

./README.md	 			: This file.

./environment.yml			: configuration file for BINDER environment.




 
