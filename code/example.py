from __future__ import print_function

def add(a, b):
    """
    Trivial function to demonstrate usage of nosetests.
    """
    return a + b

def main():
    """
    Function for demonstrating 'make analysis'.
    """
    a = 1
    b = 2
    c = add(a, b)
    print("Running analysis...")
    print("%s + %s = %s" %(a, b, c))
    print("Done!")

if __name__ == "__main__":
    main()
