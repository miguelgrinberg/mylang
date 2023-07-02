# The My Programming Language

This is the official repository for the "my" programming language from my [toy language tutorial](https://blog.miguelgrinberg.com/post/building-a-toy-programming-language-in-python).

The language supports variable assignments and print statements. Expressions can use addition, subtraction, multiplication and division between integers and/or variables previously defined.

Example program:

```python
a = 4 + 5 * 6 - 7
b = a / 2
print b + 1
```

To run the program, save it to a file such as *test.my*, then execute it as follows:

```bash
$ python my.py test.my
14
```

