import pip

def install(package):
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])

# Example
if __name__ == '__main__':
    answer = input("Did you mean to execute this program? y for Yes, n for No\n")
    if answer == "y":
        install('pillow')
        install('python-kasa')
        install('bleak')
    else:
        exit()
