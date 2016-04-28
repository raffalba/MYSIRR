**MY SIRR v.2.0**
----------

### Minimalist agro-hYdrologicalmodel for Sustainable IRRigation management- soil moisture and crop dynamics*
----------
<p align="left"><img src="https://github.com/raffalba/MYSIRR/blob/master/img/logo.png"/></p>

**MY SIRR** is a software written in python programming language with a simple Graphical User Interface (GUI) for quantitativly assess and compare agricultural enterprises across climates, soil types, crops, and irrigation strategies, accounting for the unpredictability of the hydro-climatic forcing.

## Table of Contents

* [**Team/Authors**](#team-authors)
* [**Project Details**](#project-details)  
    * [Scope](#scope)
    * [Requirements](#requirements)
    * [License](#license)
    * [Metadata](#metadata)
* [**Quick Start**](#quick-start)
    * [Input data](#input)
    * [how to run the model](#run)
    * [output data](#input)
* [**Documentation**](#documentation)
    * [Full documentation (Science of Computer Programming Journal, if accepted)](http://www.journals.elsevier.com/science-of-computer-programming/)
* [**Acknowledgements**](#acknowledgements)

## Team
- [Raffaele Albano] (http://www2.unibas.it/raffaelealbano/) [Co-Founder of [Wat-TUBE] (http://wat-tube.it/index.php/it/) spin-off UNIBAS, Research Associate at [University of Basilicata] (http://portale.unibas.it/site/home.html) (UNIBAS), [ECS Representatives] (http://www.egu.eu/ecs/representatives/) of NH Division of European Geosciences Union (EGU)]
- [Salvatore Manfreda]  (http://www2.unibas.it/manfreda/HydroLab/home.html)[Associate Professor of University of Basilicata UNIBAS, Co-Founder of [Wat-TUBE] (http://wat-tube.it/index.php/it/) spin-off UNIBAS]
- [Giuseppe Celano](https://sites.google.com/a/agrariaunibas.net/frutticoltura/Home) [Associate Professor of University of Basilicata UNIBAS]

## Project Details
Learn more about the **MYSIRR** project scope, requirements, and licensing.

### Scope
*MY SIRR* is designed to inform farmers, especially from the developing countries or smallholders, for short- and long-term water-related agricultural management. Its parameters are explicit and mostly intuitive and the model maintains sufficient balance between accuracy, simplicity and robustness. The tool accounts in a parsimonious and flexible way for the main climate, soil and vegetation characteristics, and includes the most important source of uncertainty in soil moisture variability (i.e., rainfall) with stochastic approach.

### Requirements
- Requires [Python (v.2.7)] (https://www.python.org/)
- Requires [matplotlib] (http://matplotlib.org/) and [numpy] (http://www.numpy.org/) package
- If you use Microsoft excel input file, it is requires also [xlrd] (https://pypi.python.org/pypi/xlrd) and [xlwt] (https://pypi.python.org/pypi/xlwt) python package
- If you want to use the provided GUI, you should install [PySide] (https://pypi.python.org/pypi/PySide/1.2.4) python package

### License
This project is completely licensed [GPL v3+](https://github.com/raffalba/MYSIRR/blob/master/LICENSE).

### Metadata
| Metadata Title	| Description 	|
|:--------------------:	|:-------------------------------:	|:--------------------------------:	|
|       Current Code version       	|            iOS 7.0             	|             1.0              	|
|    Permanent link to code / repository used of this code version      	|          Xcode 6.1.1            	|           https://github.com/mozart/mozart2            |
|      Software Code Language used        	|             Python (v. 2.7)           
|      Compilation requirements, Operating environments & dependencies  |            Matplotlib and numpy packages  
|      Computing platform / Operating System   |            Linux, OS X, Microsoft Windows  
|      License   |            GNU GPL v.3

## Quick Start
The tool is composed by three main classes: the class that contains the several main functions "[myfun.py](https://github.com/raffalba/MYSIRR/blob/master/scripts/myfun.py)" utilized in the main class "[mysirr.py](https://github.com/raffalba/MYSIRR/blob/master/scripts/mysirr.py)", that managed the input parameters to evaluate the results and, therefore, to create the outputs, and finally the class "[mysim.py](https://github.com/raffalba/MYSIRR/blob/master/scripts/mysim.py)" used to read the project file and its components and run the proposed model. Finally, the class "[mysirrGUI_mainWindow.py](https://github.com/raffalba/MYSIRR/blob/master/scripts/mysirrGUI_mainWindow.py)" culd be used to run the model by graphical user interface (GUI). The native file of the GUI is also provided, check "[mainWindow.ui](https://github.com/raffalba/MYSIRR/blob/master/scripts/mainWindow.ui)".
 
### Input data
MY SIRR uses fairly intuitive input variables, either widely used or largely requiring simple methods for their determination. 
Input data is a project files, encoding in Extensible Markup Language (XLM), composed by a set of input modules in comma separated value or Microsoft excel format (see the following figures):
<p align="center"><img src="https://github.com/raffalba/MYSIRR/blob/master/img/input.png"/></p>

### how to run the model
The model has a simple and easy to use Graphical User Interface (GUI) (see the following figures):
<p align="center"><img src="https://github.com/raffalba/MYSIRR/blob/master/img/gui.png"/></p>
The left panel is able to upload the input files,  required to run the model, and to set the path of the output file. The rigth panel can help the users to set the principal parameters, such as information about ET0 (i.e. BT if ET0 is evaluated by Blaney-Criddle method, PM if estimated by Penman-Monteith equation and N if ET0 is provided by the user), set the rain parameters, ie. if it is given by the user (N) or if use stochastic method to evaluate the rainfall time and amount (Y), set the method for the assesment of Yeld (i.e. EMP for empirical formula and DIC for dichotomic  process), and, finally, set the number of cell in which perform the calculation (cell ID). Finally, The "Menu Bar" permits to upload a project file, encoding in Extensible Markup Language (XLM), or to check for recent project files. These files stores the PATH_NAME of all input modules, encoded as comma separated value or Microsoft excel format, required to run the model (see the [Input data](#input) section. In this menu, you can save the project by clicking the button “Save Project”. In case you want to make a copy of the project you can use the button “Save Project as..”.

Moreover you can run the model without the user interface. The model simulation could be easily run by terminal or through a batch or python interpreterand. The scripts could be easly used for iterative runs. The user can run the model: (i) lunching the class "[mysim.py](https://github.com/raffalba/MYSIRR/blob/master/scripts/mysim.py)" that requires as input the project file (XLM) and the name of output file or (ii) lunching the main class "[mysirr.py](https://github.com/raffalba/MYSIRR/blob/master/scripts/mysirr.py)" giving as input the following information (that are store in xlm format in the project file):
1) furnish the name of all input modules (i.e. climate.csv, soil.csv, crop.csv and management.csv) 
2) select the number of the soil cell to run (e.g. 1)
3) provide information about ET0 (i.e. BT if ET0 is evaluated by Blaney-Criddle method, PM if estimated by Penman-Monteith equation and N if ET0 is provided by the user)
4) choose if the rain is given by the user (N) or if use stochastic method to evaluate the rainfall time and amount (Y)
5) provide the name of the input file (e.g. output.csv)
6) choose the method for the assesment of Yeld (i.e. EMP for empirical formula and DIC for dichotomic  process)

### Output data
The results consist of the Climate-Crop-Soil water output diagrammed in two main graphs and stored an output file (csv or excel) that could be easily retrieved in spreadsheet programmers for further processing and analysis.
<p align="center"><img src="https://github.com/raffalba/MYSIRR/blob/master/img/Climate-Soil-Crop.png"/></p>

## Documentation
*See the full article on [Software X] (http://www.journals.elsevier.com/softwarex/) - Elsevir Journal, submitted.*

## Acknowledgements
Funding for this study was provided by Life + Project, named [CarbOnFarm] (http://www.carbonfarm.eu/), Technologies to stabilize soil organic carbon and farm productivity, promote waste value and climate change mitigation, project number: Life12 ENV/IT/719

