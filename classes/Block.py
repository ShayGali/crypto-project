
def validate_block(validate_function):
    return validate_function()


def validate_function():
    print("hello")


a = lambda: print("hello")

validate_block(validate_function)
