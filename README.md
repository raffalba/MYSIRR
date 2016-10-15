**MY SIRR v.3.0**
----------

### Minimalist agro-hYdrologicalmodel for Sustainable IRRigation management- soil moisture and crop dynamics
----------
<p align="left"><img src="https://github.com/raffalba/MYSIRR/blob/master/img/logo.png"/></p>

**MY SIRR** is a software written in python programming language with a simple Graphical User Interface (GUI) for quantitatively assess and compare agricultural enterprises across climates, soil types, crops, and irrigation strategies, accounting for the unpredictability of the hydro-climatic forcing.

## Table of Contents

* [**Team/Authors**](#team-authors)
* [**Project Details**](#project-details)  
    * [Scope](#scope)
    * [Background](#background)
    * [License](#license)
    * [Metadata](#metadata)
* [**MY SIRR Installation Instruction**](#project-details)  
    * [Requirements](#requirements)
	* [Source Install](#source-install)
	* [Binary Install](#binary-install)
* [**MY SIRR Quick Start**](#quick-start)
    * [Input data](#input)
    * [Benchmark Input DataSet](#inputdata)
	* [Literature DataSet Collection](#dataset)
    * [How to Run the Model](#run)
    * [output data](#input)
* [**Reference**](#reference)
    * [Full article (Software X, under revision)](http://www.journals.elsevier.com/softwarex/)
* [**Acknowledgements**](#acknowledgements)
* [**Bug Report**](#bug-report)

## Team
- [Raffaele Albano] (http://www2.unibas.it/raffaelealbano/) (Co-Founder of [Wat-TUBE] (http://wat-tube.it/index.php/it/) spin-off UNIBAS, Research Associate at University of Basilicata (UNIBAS))
- [Salvatore Manfreda]  (http://www2.unibas.it/manfreda/HydroLab/home.html) (Associate Professor of University of Basilicata, Co-Founder of [Wat-TUBE] (http://wat-tube.it/index.php/it/) spin-off UNIBAS)
- [Giuseppe Celano](https://sites.google.com/a/agrariaunibas.net/frutticoltura/Home) (Associate Professor of University of Basilicata)

## Project Details
Learn more about the **MY SIRR** project: scope, background and licensing.

### Scope
*MY SIRR* is designed to inform farmers, especially from the developing countries or smallholders, for short- and long-term water-related agricultural management. Its parameters are explicit and mostly intuitive and the model maintains sufficient balance between accuracy, simplicity and robustness. The tool accounts in a parsimonious and flexible way for the main climate, soil and vegetation characteristics, and includes the most important source of uncertainty in soil moisture variability (i.e., rainfall), also, with stochastic approach.

### Background
The field of ecohydrology, traditionally focusing on natural ecosystems, has the potential to offer the necessary quantitative tools to assess and compare agricultural enterprises across climates, soil types, crops, and irrigation strategies, accounting for the unpredictability of the hydro-climatic forcing. Ecohydrological processes are often strongly nonlinear—a fact that amplifies the intermittency and unpredictability of the external hydroclimatic fluctuations that drive them. Irrigation represents one of the main strategies to enhance and stabilize agricultural productivity, by mitigating the effects of rainfall vagaries. 
Thus, a framework that blends process-based representations of ecohydrological dynamics, nonlinearities, and random components of the forcing is necessary to tackle the problem of sustainable management of water, soil, and crop development in agroecosystem in a quantitative way.
Along these lines, the methods developed by stochastic ecohydrology ([Rodriguez-Iturbe and Porporato, 2004] (http://www.journals.uchicago.edu/doi/10.1086/424970)) focus on nonlinear interactions and temporal stochasticity, while smoothing out spatial heterogeneities through spatially lumped representations, is here used in *MY SIRR* in order to realize a simple, widely applicable agro-hydrological tool is designed to inform farmers, especially from the developing countries or smallholders, for short- and long-term water-related agricultural management.
In this approach, agricultural sustainability and productivity are assessed with reference to water productivity (defined as the ratio between yield and total supplied water), i.e. the inverse of [Water Footprint] (http://waterfootprint.org/en/), yields, water requirements, and their variability — a crucial element for food security and resource allocation planning.

The physical interpretation of the processes is at the daily time scale level. At this scale, rainfall, percolation, and concentrated irrigation events may be conveniently treated as impulsive, thus considerably simplifying the results without compromising the realisms of the description.
The model can be used to quantify water productivity, crop yields, and irrigation requirements, as well as their variability, a crucial element for food security and resource allocation planning. The model does not account for the effects of pests and diseases. Moreover, we assume that plant productivity is not nutrient limited and do not discuss salinity problems. In the following a schematic representation of the utilized approach.
<p align="center"><img src="https://github.com/raffalba/MYSIRR/blob/master/img/Climate-Soil-Crop.png"/></p>

### License
This project is completely licensed [GPL v3+](https://github.com/raffalba/MYSIRR/blob/master/LICENSE).

### Metadata
| Metadata Title	| Description 	|
|:--------------------:	|:-------------------------------:	|:--------------------------------:	|
|       Current Code version       	|           v. 3.0             	|                           	|
|    Permanent link to code / repository used of this code version      	|         https://github.com/raffalba/MYSIRR           |
|      Software Code Language used        	|             Python (v. 2.7)           
|      Compilation requirements, Operating environments & dependencies  |            Matplotlib and numpy packages  
|      Computing platform / Operating System   |            Linux, OS X, Microsoft Windows  
|      License   |            GNU GPL v.3

## MY SIRR Installation Instruction

### Requirements
Before using the MY SIRR package, you will need a working Python installation on your computer. Python can be obtained from [http://www.python.org] (http://www.python.org), if it is not already present on your system. 
In addition, the model depends on a number of 3rd party Python packages, the main are:

- [matplotlib] (http://matplotlib.org/) and [numpy] (http://www.numpy.org/) package
- If you use Microsoft excel input file, it is requires also [xlrd] (https://pypi.python.org/pypi/xlrd) and [xlwt] (https://pypi.python.org/pypi/xlwt) python package
- If you want to use the provided GUI, you should install [PySide] (https://pypi.python.org/pypi/PySide/1.2.4) python package

All of the 3rd party packages must be installed and working on your system for MY SIRR to work correctly.

### Source Install
The MY SIRR package currently consists of pure [Python (v.2.7)] (https://www.python.org/) code and does not require any extension modules to be built, so installation from source is straightforward on all popular operating systems.  
However the model depends on a number of 3rd party Python packages.  A dependecy file list is provided as "[requirement.txt] (https://github.com/raffalba/MYSIRR/blob/master/scripts/requirement.txt)". To install directly all the dependencies into a new machine please use "[pip package] (https://pypi.python.org/pypi/pip)" using the command:

	pip install -r requirement.txt

### Binary Installer
Source releases of the MY SIRR code, as exectutable file for same operative systems, can be downloaded, as compressed file, in the folder [download] (https://github.com/raffalba/MYSIRR/blob/master/download)


## MY SIRR Quick Start
The tool is composed by four main classes: 
the class that contains the several main functions "[myfun.py](https://github.com/raffalba/MYSIRR/blob/master/scripts/myfun.py)" utilized in the main class "[mysirr.py](https://github.com/raffalba/MYSIRR/blob/master/scripts/mysirr.py)", that managed the input parameters to evaluate the results and, therefore, to create the outputs, and finally the class "[mysim.py](https://github.com/raffalba/MYSIRR/blob/master/scripts/mysim.py)" used to read the project file and its components and run the proposed model. Finally, the class "[mysirrGUI_mainWindow.py](https://github.com/raffalba/MYSIRR/blob/master/scripts/mysirrGUI_mainWindow.py)" can be used to run the model by graphical user interface (GUI). The native file of the GUI is also provided, check "[mainWindow.ui](https://github.com/raffalba/MYSIRR/blob/master/scripts/mainWindow.ui)".

### Input data
MY SIRR uses fairly intuitive input variables, either widely used or largely requiring simple methods for their determination. Input data is a project files, encoding in Extensible Markup Language (XLM), composed by a set of input modules in comma separated value or Microsoft excel format:
<p align="center"><img src="https://github.com/raffalba/MYSIRR/blob/master/img/input.png"/></p>

 i) Climate Module:
 
This module requires the user's set of daily Reference Evapotranspiration ET0 (mm) and daily rainfall amount (mm).
ET0 represents the potential evaporation of a well-watered grass crop. The water needs of other crops are directly linked to this climatic parameter.
Although several methods exist to determine ETo, the Penman-Monteith ([Allen et al., 1998] (http://www.fao.org/docrep/X0490E/X0490E00.htm)) and  Blaney-Criddle method ([Blaney and Criddle, 1962] (https://naldc.nal.usda.gov/naldc/download.xhtml?id=CAT87201264&content=PDF)) has been implemented in MY SIRR to determine ETo from climatic data on temperature, humidity, sunshine, windspeed. 
Moreover, the model allows estimating the rainfall amount, if not provided by user, with a stochastic approach proposed by ([Rodriguez-Iturbe et al., 1999] (http://rspa.royalsocietypublishing.org/content/455/1990/3789)). In this way, the rainfall is modeled as instantaneous events occurring according to a marked Poisson process of rate lambda (mean frequency of rainfall events) and with exponentially distributed depths with mean alpha.

 ii) Soil Module:
 
The soil is modeled as a horizontal layer of depth Zr with homogeneous characteristics. The needed parameters are: volumetric water content at field capacity (sfc), permanent wilting point (sw), soil moisture level corresponding to incipient stomatal closure (s*) and soil porosity (n).
See [Literature DataSet Collection] (#dataset) for a list of soil information collection

 iii) Crop Module:
 
The model uses a small number of crop parameters, (e.g. the biologic correction factor (Kc), that takes into account the species and the development stadium of plant, the active rooting depth (Zr), the maximum yield (Ymax), i.e. the asymptotic yield, to characterize the crop with its development, growth and yield processes.
See [Literature DataSet Collection] (#dataset) for a list of crop information collection

 iv) Management Module:
 
Management options include the definition of the schedule by specifying the time, depth of the irrigation water and the selection of water application methods, (i.e. sprinkler, surface, or drip either sprinkler or surface)
Moreover, the method use an optimization function for the estimation of the amount of irrigation volume and application time maximizing Water Productivity (WP) , i.e. measure of the efficiency with which total available water supply is transformed into marketable yield.
According to ([Vico and Porporato, 2010](http://onlinelibrary.wiley.com/doi/10.1029/2009WR008130/abstract)), MY SIRR uses plant water status to characterize demand-based irrigation through soil mosture levels by means of two parameters: The soil moisture threshold which triggers the irrigation application ("intervention point") and the amount of water applied at each tratment or, equivalently, the soil moisture level restored by irrigation apllication, i.e. "traget level".
In this way, irrigation volumes and frequencies not only depend on the rainfall forcing but also on crop and soil features. 

### Benchmark Input DataSet
A set of sample data to test the plugin is provided in [input] (https://github.com/raffalba/MYSIRR/blob/master/data/input) folder

### Literature DataSet Collection
A local survey or monitoring should be carried out in order to assess climate (e.g. Rainfall), soil (e.g. soil texture class and hydrological characteristics), crop (e.g. root deph, crop development stages, crop coefficient) and irrigation strategy (e.g. drip, sprinckler or surface irrigation) at farmer scale. In case these information could not be available, a dataset of literature values of the model parameters for several type of soil and crop are provided here, in [literature_dataset] (https://github.com/raffalba/MYSIRR/blob/master/data/literature_dataset) folder. In this way, several non-expert users, such as farmers living in developing regions, can be made an assessment of water management strategies in agro-ecosystems on the basis of their needs.

### How to Run the Model
The model has a simple and easy to use Graphical User Interface (GUI) (see the following figures):
<p align="center"><img src="https://github.com/raffalba/MYSIRR/blob/master/img/gui.png"/></p>
The left panel is able to upload the input files,  required to run the model, and to set the path of the output file. The rigth panel can help the users to set the principal parameters, such as information about ET0 (i.e. BT if ET0 is evaluated by Blaney-Criddle method, PM if estimated by Penman-Monteith equation and N if ET0 is provided by the user), set the rain parameters, ie. if it is given by the user (N) or if use stochastic method to evaluate the rainfall time and amount (Y), set the method for the assesment of Yeld (i.e. EMP for empirical formula and DIC for dichotomic  process), set the number of cell in which perform the calculation (cell ID), and, finally, set if you want to use the optimize the irrigation time and amount maximizing Water Productivity).
Finally, The "Menu Bar" permits to upload a project file, encoding in Extensible Markup Language (XLM), or to check for recent project files. These files stores the PATH_NAME of all input modules, encoded as comma separated value or Microsoft excel format, required to run the model (see the [Input data](#input) section). In this menu, you can save the project by clicking the button “Save Project”. In case you want to make a copy of the project you can use the button “Save Project as..”.

Moreover you can run the model without the user interface. The model simulation could be easily run by terminal or through a batch or python interpreterand. The scripts could be easly used for iterative runs. The user can run the model: (i) lunching the class "[mysim.py](https://github.com/raffalba/MYSIRR/blob/master/scripts/mysim.py)" that requires as input the project file (XLM) and the name of output file or (ii) lunching the main class "[mysirr.py](https://github.com/raffalba/MYSIRR/blob/master/scripts/mysirr.py)" giving as input the following information (that are store in xlm format in the project file):

1. furnish the name of all input modules (i.e. climate.csv, soil.csv, crop.csv and management.csv)
2. select the number of the soil cell to run (e.g. 1)
3. provide information about ET0 (i.e. BT if ET0 is evaluated by Blaney-Criddle method, PM if estimated by Penman-Monteith equation and N if ET0 is provided by the user)
4. choose if the rain is given by the user (N) or if use stochastic method to evaluate the rainfall time and amount (Y)
5. provide the name of the input file (e.g. output.csv)
6. choose the method for the assesment of Yeld (i.e. EMP for empirical formula and DIC for dichotomic  process)
7. choose if you want or not use the optimization function for assess the irrigation time and frequency maximizing WP


### Output data
The results consist of the Climate-Crop-Soil water output diagrammed in two main graphs and stored an output file (csv or excel) that could be easily retrieved in spreadsheet programmers for further processing and analysis.
The main output of the models are:

* Rainfall (also stochastic generated)
* ETnorm (i.e., to the evapotranspiration rate normalized by the active soil depth)
* Relative Soil Moisture dynamic (i.e., the fraction of water-filled soil pore volumes, ranging from 0 for dry soils to 1 at soil saturation)
* Irrigation amount time series
* Plant Water Stress dynamic related to the soil moisture condition at the time under consideration
* Likage amount
* Crop development during the growing season
* Effective user of water (the fraction of water made available to the plant that is indeed used for productive uses)
* Yeld
* WaterFootprint(considered as the inverse of Water Productivity)

## Reference
*Albano, R., Manfreda, S., Celano, C., MY SIRR: Minimalist agro-hYdrological model for Sustainable Irrigation management – soil moisture and crop dynamics, [Software X] (http://www.journals.elsevier.com/softwarex/) (under review)*

## Acknowledgements
Funding for this study was provided by Life + Project, named [CarbOnFarm] (http://www.carbonfarm.eu/), Technologies to stabilize soil organic carbon and farm productivity, promote waste value and climate change mitigation, project number: Life12 ENV/IT/719

## Bug Report
The best place to file bug reports is at the [Bug Tracker] (https://github.com/raffalba/MYSIRR/issues), this requires a free [Github] (https://github.com/) account.

Please ensure that bug reports clearly describe the bug and if possible provide a simple script that can reproduce the problem. If in doubt contact [Raffaele Albano] (http://www2.unibas.it/raffaelealbano/?page_id=115).
