# Measuring Sensitivity of Central Tendency Measures to Outliers - Shiny for Python

### Introduction

In this exercise you will be able to see and analyze how outiler values, both in quantity (more or less outliers) and value (larger or smaller outliers), have an impact on two central tendency measures widely used in statistics: mean and median.

In order to see how sensitive are these measures to outliers, I created an application using [Shiny for Python](https://shiny.rstudio.com/py/). In this application, you will find the following tuneable parameters that will help you see the effect of the outliers:

* Sample size: Number of variables in the data.
* Number of bins: Number of bins of the histogram.
* Add outlier to distribution: If selected, other parameters related to outliers will be displayed.
  * Offset: Value of the outliers (larger or smaller outliers).
  * Amount of outliers: Number of outlier values that will added to the dataset.
  
 ---
 
 ### Example
  
This is an example screenshot of how the Shiny app looks:



<img src="https://user-images.githubusercontent.com/61316451/201291600-16323ba4-5360-47a6-8bc9-e80e435f22e8.png" width="1000" height="600">

---

### Install dependencies

In order to run the Shiny app, the first step is to install all the dependencies.

`pip install -r requirements.txt`

---

### Run Shiny application

Once all the packages and dependencies are installed, we can run the Shiny app and analyze how Central Tendency Measures behave when outliers are added to our dataset.

`shiny run --reload my_app/app.py`
