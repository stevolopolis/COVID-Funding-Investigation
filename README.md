# COVID-19 Funding Behavior Investigation
## User Manual
### Prerequisites
1. Install Python-3.9
2. Run `pip install -r requirements.txt`
3. Chrome must be installed in your computer. (Other browswers are not supported yet.)
4. Download all files in this repository, espcially the "data" folder which contains the scraped data.
### Running the code
1. To webscrape data from CB-Insights.
    1. Create a folder in the same directory for saving webscraped csv files and change `CSV_SAVE_DIR` to the name of the folder on `line 34`.
    2. Run `py -3.9 main.py` and type `n`, as shown below:
    ```
    Have you scraped the data? ("y" or "n")
    n
    ```
2. To visualize data
    1. Run `py -3.9 main.py`
    2. An interactive terminal session will start. You may answer accordingly to your liking.
    3. The following code block presents a sample usage:
    ```
    Have you scraped the data? ("y", "n")
    y
    Start visualizing? ("y" or "n")
    y
    Would you like to visualize pie graphs or line graphs? ("p" or "l")
    p
    What category would you like to visualize? ("company", "country", "industry", "stage")
    stage
    Would you like to visualize multiple years of pie graph? ("y" or "n")
    n
    ```
![Output image from the sample code block](figures/stage-pie.png)
