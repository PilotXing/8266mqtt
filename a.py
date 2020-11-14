from machine import Timer


def aaa(self):
    """
    docstring
    """
    print("arostnaorien")


t1 = Timer(1)
t1.init(mode=Timer.PERIODIC, period=300, callback=aaa)
