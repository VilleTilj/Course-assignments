"""The assignment for Data-Intensive Programming 2022"""

from typing import List, Tuple

from pyspark import rdd
from pyspark.sql import DataFrame
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType, StructType, StructField, DoubleType, StringType
from pyspark.sql.functions import when, regexp_replace
from pyspark.ml.clustering import KMeans
from pyspark.ml.evaluation import ClusteringEvaluator
from pyspark.ml.feature import VectorAssembler, MinMaxScaler
import numpy as np
from pyspark.ml import Pipeline
from pyspark.ml import PipelineModel
import matplotlib.pyplot as plt


class Assignment:
    spark: SparkSession = SparkSession.builder \
                                        .appName("assignment") \
                                        .config("spark.driver.host", "localhost") \
                                        .master("local") \
                                        .getOrCreate()

    # Schemas for the datatypes
    schema2: StructType = StructType([StructField('a', DoubleType(), True), StructField('b', DoubleType(), True),
     StructField('LABEL', StringType(), True)])

    schema3: StructType = StructType([StructField('a', DoubleType(), True), StructField('b', DoubleType(), True),
     StructField('c', DoubleType(), True), StructField('LABEL', StringType(), True)])

    # the data frame to be used in tasks 1 and 4, drop values that are not in the schema specified and remove any rows
    # with null as a value in any column.
    dataD2: DataFrame = spark.read.csv("data/dataD2.csv", sep=",", schema=schema2, header=True, mode="DROPMALFORMED").na.drop()

    # the data frame to be used in task 2
    dataD3: DataFrame = spark.read.csv("data/dataD3.csv", sep=",", schema=schema3, header=True, mode="DROPMALFORMED").na.drop()

    # the data frame to be used in task 3 (based on dataD2 but containing numeric labels)
    dataD2WithLabels: DataFrame = dataD2.withColumn("LABEL", when(dataD2.LABEL == "Ok", regexp_replace(dataD2.LABEL, "Ok", "1"))
                                                    .otherwise(regexp_replace(dataD2.LABEL, "Fatal", "0")).cast(IntegerType()))



    @staticmethod
    def task1(df: DataFrame, k: int) -> List[Tuple[float, float]]:
        '''

        :param df:
        :param k:
        :return:
        '''

        max: np.ndarray = np.array([df.agg({"a": "max"}).collect()[0][0], df.agg({"b": "max"}).collect()[0][0]])
        min: np.ndarray = np.array([df.agg({"a": "min"}).collect()[0][0], df.agg({"b": "min"}).collect()[0][0]])

        means: np.ndarray
        _, means = Assignment.training_pipeline(df, ["a", "b"], k)
        means = (np.array(means)*(max - min)) + min

        means_list: List[Tuple[float, float]] = list(map(tuple, means))
        return means_list

    @staticmethod
    def task2(df: DataFrame, k: int) -> List[Tuple[float, float, float]]:
        '''

        :param df:
        :param k:
        :return:
        '''

        max: np.ndarray = np.array([df.agg({"a": "max"}).collect()[0][0], df.agg({"b": "max"}).collect()[0][0],
                        df.agg({"c": "max"}).collect()[0][0]])
        min: np.ndarray = np.array([df.agg({"a": "min"}).collect()[0][0], df.agg({"b": "min"}).collect()[0][0],
                        df.agg({"c": "min"}).collect()[0][0]])

        means: np.ndarray
        _, means = Assignment.training_pipeline(df, ["a", "b", "c"], k)
        means = (np.array(means)*(max - min)) + min

        means_list: List[Tuple[float, float, float]] = list(map(tuple, means))
        return means_list

    @staticmethod
    def task3(df: DataFrame, k: int) -> List[Tuple[float, float]]:
        '''

        :param df:
        :param k:
        :return:
        '''

        max: np.ndarray = np.array([df.agg({"a": "max"}).collect()[0][0], df.agg({"b": "max"}).collect()[0][0]])
        min: np.ndarray = np.array([df.agg({"a": "min"}).collect()[0][0], df.agg({"b": "min"}).collect()[0][0]])

        data: DataFrame
        cluster_centers: np.ndarray
        data, cluster_centers = Assignment.training_pipeline(df, ["a", "b", "LABEL"], k)

        dataRDD: rdd = data.rdd.map(lambda x: [x[5], x[2]]).reduceByKey(lambda a, b: a+b).sortBy(lambda x: x[1])

        cluster_with_most_fatalities: list = [dataRDD.collect()[0][0], dataRDD.collect()[1][0]]
        center_with_most_fatalities: Tuple[np.ndarray, np.ndarray] = cluster_centers[cluster_with_most_fatalities[0]][:2]\
            ,cluster_centers[cluster_with_most_fatalities[1]][:2]
        center_with_most_fatalities: np.ndarray = (np.array(center_with_most_fatalities)*(max - min)) + min

        return [tuple(i) for i in center_with_most_fatalities]

    # Parameter low is the lowest k and high is the highest one.
    @staticmethod
    def task4(df: DataFrame, low: int, high: int) -> List[Tuple[int, float]]:
        '''
        :param df:
        :param low:
        :param high:
        :return:
        '''

        scores: List[Tuple[int, float]] = Assignment.task4_recursion(df, low, high)
        plt.plot(*zip(*scores))
        plt.draw()
        plt.pause(3)
        plt.close()
        return scores

    @staticmethod
    def task4_recursion(df: DataFrame, low: int, high: int):
        to_return: List[Tuple[int, float]] = []
        evaluator: ClusteringEvaluator = ClusteringEvaluator(predictionCol='prediction', featuresCol='scaled').\
            setMetricName('silhouette')
        means, _ = Assignment.training_pipeline(df, ["a", "b"], low)
        score: float = evaluator.evaluate(means)
        to_return.append((low, score))

        if low == high:
            return to_return
        else:
            to_return.extend(Assignment.task4_recursion(df, low+1, high))
            return to_return

    @staticmethod
    def training_pipeline(df: DataFrame, inputcols, k) -> Tuple[DataFrame, np.ndarray]:
        """
        :param df: The dataframe inputted to the pipeline
        :param inputcols: Which columns we want to use for the clustering
        :param k: k-means clustering k value
        :return: Dataframe manipulated by the pipeline and the clustering centers for that K-means clustering
        """
        vecAssembler: VectorAssembler = VectorAssembler(inputCols=inputcols, outputCol='features')
        minmaxer: MinMaxScaler = MinMaxScaler(inputCol='features', outputCol='scaled', min=0, max=1)
        kmeans: KMeans = KMeans(featuresCol='scaled', k=k, seed=1)

        pipeline: Pipeline = Pipeline(stages=[vecAssembler, minmaxer, kmeans])
        fit_model: PipelineModel = pipeline.fit(df)
        to_return: DataFrame = fit_model.transform(df)

        cluster_centers: np.ndarray = fit_model.stages[2].clusterCenters()

        return to_return, cluster_centers

