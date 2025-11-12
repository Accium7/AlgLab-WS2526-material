from data_schema import Instance, Solution


def solve(instance: Instance) -> Solution:
    """
    Implement your solver for the problem here!
    """
    x = len(instance.numbers)
    while True:
        for number in range(len(instance.numbers)-1):
            if instance.numbers[number] > instance.numbers[number+1]:
                tmp = instance.numbers[number]
                instance.numbers[number] = instance.numbers[number+1]
                instance.numbers[number + 1] = tmp
                x = x-1
        if x == len(instance.numbers) :
            break
        x = len(instance.numbers)

    return Solution(
        number_a=instance.numbers[0],
        number_b=instance.numbers[-1],
        distance=abs(instance.numbers[0] - instance.numbers[-1]),
    )
