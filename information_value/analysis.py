import multiprocessing
import operator
from calculator import InformationValueCalculator, WindowSizeTooLarge
import config

# The amount of words that will be counted on the total sum

SUM_THRESHOLD = config.SUM_THRESHOLD

class WindowAnalysis(object):
    def __init__(self, window_size, iv_words, number_of_words):
        self.window_size = window_size
        amount_to_be_taken = int(len(iv_words) * SUM_THRESHOLD)
        sorted_words = sorted(iv_words.iteritems(), key=operator.itemgetter(1), reverse=True)[:amount_to_be_taken]
        self.max_iv = sorted_words[0][1]
        # Sum the reverse of sorted_words to improve numerical stability
        self.iv_sum = reduce(lambda x,y: x+y[1], reversed(sorted_words), 0)
        self.top_words = sorted_words[:20]

    def encode(self):
        return {
            "window_size": self.window_size,
            "top_words": self.top_words,
            "iv_sum": self.iv_sum,
            "max_iv" : self.max_iv,
        }




# This global variable is shared across the threads
information_value_calculator = None
number_of_words = 20


def get_window_size_analysis(window_size):
    try:
        print "Probando window_size = %s" % window_size
        iv_words = information_value_calculator.information_value(window_size)
        return (window_size, WindowAnalysis(window_size, iv_words, number_of_words))
    except WindowSizeTooLarge as e:
        return (window_size, None)

def get_all_analysis(tokens, window_sizes, number_of_words=20):
    global information_value_calculator
    information_value_calculator = InformationValueCalculator(tokens)
    pool = multiprocessing.Pool(processes=3)
    return dict(pool.map(get_window_size_analysis, window_sizes))

def get_optimal_window_size(tokens, window_sizes, number_of_words=20, sum_threshold=config.SUM_THRESHOLD):
    results_per_window_size = get_all_analysis(tokens, window_sizes, number_of_words)
    SUM_THRESHOLD = sum_threshold
    #Criterio: maximo de promedio de IV sobre todas las palabras
    best_result = max(results_per_window_size.iteritems(),
        key= lambda res: res[1].iv_sum
        )
    
    return best_result