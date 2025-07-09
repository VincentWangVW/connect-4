import random

if __name__ == "__main__":
    # generate 1000 coin flips and return the number of heads
    coin_flips = [random.choice(['H', 'T']) for _ in range(1000)]
    num_heads = coin_flips.count('H')
    print(f"Number of heads in 1000 coin flips: {num_heads}")
    print(random.randint(400,600))