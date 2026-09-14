# Portofolio in progress
# Locust for Performance Testing Portfolio

## Website being used as a test object
```
https://dummyjson.com/
```

## To run the performance test script
```
Run this in cmd:
locust -f dummyjson.py -u 10 -r 0.1 --html=dummyjson_result.html > dummyjson.log 2>&1

The test will have 10 maximum concurrent vusers, with a spawn rate of 0.1/sec.
After the test run is over, locust will generate an html named dummyjson.html containing the performance result
While the test is running, it will also print the log to dummyjson.log
```

## API Flow
```
1. POST https://dummyjson.com/auth/login
2. POST https://dummyjson.com/products/add
3. GET  https://dummyjson.com/recipes/search
```