import os

if __name__ == '__main__':

    file = open('/Users/lzl/Documents/头像.jpeg', 'rb')

    a = open('/Users/lzl/Desktop/a', 'wb')
    b = open('/Users/lzl/Desktop/b', 'wb')
    c = open('/Users/lzl/Desktop/c', 'wb')

    a.write(file.read(30000))
    b.write(file.read(30000))
    c.write(file.read(998))

    file.close()
    a.close()
    b.close()
    c.close()
#

