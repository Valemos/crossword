import random
import time


def clamp(value, min_v, max_v):
    return max(min(value, max_v), min_v)


def random_deviation(min_v, amplitude):
    a = min_v
    b = min_v + amplitude
    if a > b: a, b = b, a
    return random.uniform(a, b)


def random_human_time(time_min, time_max):
    interval_magnitude = time_max - time_min
    mu = interval_magnitude * 0.5 + time_min
    sigma = interval_magnitude / 4
    sleep_time = random.normalvariate(mu, sigma)

    min_deviation = random_deviation(0, interval_magnitude * 0.1)
    max_deviation = random_deviation(0, interval_magnitude * 0.1)

    sleep_time = clamp(sleep_time, time_min + min_deviation, time_max - max_deviation)

    return sleep_time


def reaction_delay():
    return random_human_time(0.250, 0.5)


def long_reaction_delay():
    return random_human_time(0.7, 2)


def thinking_delay():
    return random_human_time(4, 10)


def keyboard_type_delay():
    return random_human_time(0.01, 0.2)


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    plt.hist([keyboard_type_delay() for i in range(10000)])
    plt.show()
