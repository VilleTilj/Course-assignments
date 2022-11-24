"""Exercise 5 for Data-Intensive Programming"""

from typing import List, Tuple

from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.rdd import RDD


def main():
    # Create the Spark session
    spark: SparkSession = SparkSession.builder \
                                      .appName("ex5") \
                                      .config("spark.driver.host", "localhost") \
                                      .master("local") \
                                      .getOrCreate()

    # suppress informational log messages related to the inner working of Spark
    sc: SparkContext = spark.sparkContext
    sc.setLogLevel("WARN")

    spark.conf.set("spark.sql.shuffle.partitions", "5")

    # There are three scientific articles in the directory "articles"
    # The call sc.textFile(...) returns an RDD consisting of the lines of the articles:
    articlesRdd: RDD[str] = sc.textFile("articles/*")



    printTaskLine(1)
    # Task #1: How do you get the first 10 lines as a list?
    lines10: List[str] = articlesRdd.take(10)
    print(*lines10, sep="\n")



    printTaskLine(2)
    # Task #2: Compute how many lines there are in total in the articles.
    #          And then count the total number of words in the articles
    #          You can assume that words in each line are separated by the space character (i.e. " ")
    nbrOfLines: int = articlesRdd.count()
    print(f"#lines = {nbrOfLines}")

    words: int = len(articlesRdd.flatMap(lambda x: x.split()).collect())
    print(f"#words = {words}")



    printTaskLine(3)
    # Task #3: What is the count of non-white space characters? (it is enough to count the non " "-characters for this)
    #          And how many numerical characters are there in total? (i.e., 0, 1, 2, ..., 9 characters)
    chars: int = sum(articlesRdd.flatMap(lambda x: x.split(" ")).map(lambda x: len(x)).collect())
    print(f"#chars = {chars}")

    numChars: int = len(articlesRdd.flatMap(lambda x: [c for c in x if c.isdigit()]).collect())
    print(f"#numChars = {numChars}")



    printTaskLine(4)
    # Task #4: How many 5-character words that are not "DisCo" are there in the corpus?
    #          And what is the most often appearing 5-character word (that is not "DisCo") and how many times does it appear?
    words5Count: int = len(articlesRdd.flatMap(lambda x: x.split()).filter(lambda x: x != "DisCo" and len(x) == 5).collect())
    print(f"5-character words = {words5Count}")

    word_list = articlesRdd.flatMap(lambda x: x.split()).filter(lambda x: x != "DisCo" and len(x) == 5).collect()
    commonWord: str = max(set(word_list), key=word_list.count)
    print(commonWord)
    commonWordCount: int = word_list.count(commonWord)
    print(f"The most common word is '{commonWord}' and it appears {commonWordCount} times")



    # You are given a factorization function that returns the prime factors for a given number:
    # For example, factorization(28) would return [2, 2, 7]
    def factorization(number: int) -> List[int]:
        def checkFactor(currentNumber: int, factor: int, factorList: List[int]) -> List[int]:
            if currentNumber == 1:
                return factorList
            if factor * factor > currentNumber:
                return factorList + [currentNumber]
            if currentNumber % factor == 0:
                return checkFactor(currentNumber // factor, factor, factorList + [factor])
            return checkFactor(currentNumber, factor + 1, factorList)

        if number < 2:
            return [1]
        return checkFactor(number, 2, [])



    printTaskLine(5)
    # Task #5: You are given a sequence of integers and a factorization function.
    #          Using them create a pair RDD that contains the integers and their prime factors.
    #          Get all the distinct prime factors from the RDD.
    values: List[int] = list(range(12, 18)) + list(range(123, 128)) + list(range(1234, 1238))

    factorRdd: RDD[Tuple[int, List[int]]] = sc.parallelize(values).map(lambda x: (x, factorization(x)))
    print(*[f"{n}: {factors}" for n, factors in factorRdd.collect()], sep="\n")

    distinctPrimes: List[int] = list(set([item for sublist in factorRdd.values().collect() for item in sublist]))
    distinctPrimes.sort()
    print(f"distinct primes: {distinctPrimes}")



    printTaskLine(6)
    # Task #6: Here is a code snippet. Explain how it works.
    lyricsRdd = sc.textFile("lyrics/*.txt")

    lyricsCount = lyricsRdd.flatMap(lambda line: line.split(" ")) \
                           .map(lambda word: (word, 1)) \
                           .reduceByKey(lambda v1, v2: v1 + v2)

    print(*(lyricsCount.collect()), sep="\n")

    print('''
    First, the snippet reads the lyrics data to RDD from text file.
    Then the whole RDD is flattened to list of words. 
    For example ["Sheena is a Punk rocker now"] => ["Sheena", "is", "a", "Punk", "rocker", "now"]
    Then the list elements are converted to tuples with value (word, 1).
    After that the occurrence of the words are counted with reduceByKey.
    ''')


# Helper function to separate the task outputs from each other
def printTaskLine(taskNumber: int) -> None:
    print(f"======\nTask {taskNumber}\n======")


if __name__ == "__main__":
    main()
