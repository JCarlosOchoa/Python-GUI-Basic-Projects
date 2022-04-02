print("hello world")

def basic_thing(number):
    squares = []
    for i in range(number):
        if ( (i**2) % 4 == 0 ):
            squares.append(i ** 2)
    return squares


print (basic_thing(25))