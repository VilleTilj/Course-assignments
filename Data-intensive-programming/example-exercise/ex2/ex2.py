"""Exercise 2 for Data-Intensive Programming"""

from typing import List

from pyspark.sql import functions
from pyspark.sql import DataFrame
from pyspark.sql import Row
from pyspark.sql import SparkSession


def main():
    # Create the Spark session
    spark: SparkSession = SparkSession.builder \
                                      .appName("ex2") \
                                      .config("spark.driver.host", "localhost") \
                                      .master("local") \
                                      .getOrCreate()

    # suppress informational log messages related to the inner working of Spark
    spark.sparkContext.setLogLevel("ERROR")

    spark.conf.set("spark.sql.shuffle.partitions", "5")



    printTaskLine(1)
    # Task 1: File "data/rdu-weather-history.csv" contains weather data in csv format.
    #         Study the file and read the data into DataFrame weatherDataFrame.
    #         Let Spark infer the schema. Study the schema.
    weatherDataFrame: DataFrame = __undefined__

    # Study the schema of the DataFrame:
    weatherDataFrame.printSchema()



    printTaskLine(1)
    # Task 2: print three first elements of the data frame to stdout
    weatherSample: List[Row] = __undefined__
    print(*weatherSample, sep="\n")  # prints each Row to its own line



    printTaskLine(3)
    # Task 3: Find min and max temperatures from the whole DataFrame
    minTemp: float = __undefined__
    maxTemp: float = __undefined__

    print(f"Min temperature is {minTemp}")
    print(f"Max temperature is {maxTemp}")



    printTaskLine(4)
    # Task 4: Add a new column "year" to the weatherDataFrame.
    # The type of the column is integer and value is calculated from column "date".
    # You can use function year from pyspark.sql.functions
    # See documentation: "def year" from https://spark.apache.org/docs/3.3.0/api/scala/org/apache/spark/sql/functions$.html
    weatherDataFrameWithYear: DataFrame = __undefined__
    weatherDataFrameWithYear.printSchema()



    printTaskLine(5)
    # Task 5: Find min and max temperature for each year
    aggregatedDF: DataFrame = __undefined__

    aggregatedDF.printSchema()
    print(*(aggregatedDF.collect()), sep="\n")



    printTaskLine(6)
    # Task 6: Expansion of task 5.
    #         In addition to the min and max temperature for each year find out also the following:
    #         - count for how many records there are for each year
    #         - the average wind speed for each year (rounded to 2 decimal precision)
    task6DF: DataFrame = __undefined__

    task6DF.show()


    # Stop the Spark session
    spark.stop()


# Helper function to separate the task outputs from each other
def printTaskLine(taskNumber: int) -> None:
    print(f"======\nTask {taskNumber}\n======")


if __name__ == "__main__":
    main()
