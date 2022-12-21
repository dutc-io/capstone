# Good→Better→Best Python µtraining Capstone 

Do you want to write code that you might actually want to reuse? Do you write
code that you need to share with others? Do you think about the design of that
code, its maintainability and readability? In short, do you want to write good
Python, better Python, or the best Python?

If quality Python is your goal, and you'd like to come away with a tangible,
demonstrable result from what you've learned, then you must attend this
two-week, hands-on micro-training from the Python experts at [Don't Use This
Code!](https://www.dontusethiscode.com/)


## Initial build 

To build the containers from scratch:

```
docker compose -f base.yml -f dev.yml up --build
```

or use the convenience shell script

```
./up.sh --build
```

Once the containers are built you should be able to reach the
[*Frontend*](http://localhost:3000/) and
[*Backend*](http://localhost:8000/test/simple).

For the subsequent runs if you don't need to rebuild the containers you start
the containers via:

```
docker compose -f base.yml -f dev.yml up
```

or 

```
./up.sh
```
