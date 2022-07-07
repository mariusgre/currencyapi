# Run locally
1. In terminal:

Windows:
```
> py -3 -m venv venv
> venv\Scripts\activate
```
macOS:
```
$ python3 -m venv venv
$ . venv/bin/activate
```

install related packages:

```
pip install -r requirements.txt
```

2. Add your api key in .env file.

3. Run app:

```
cd app
flask run
```

4. Navigate to:

```
http://127.0.0.1:5000/quote?baseCurrency=USD&quoteCurrency=GBP&baseAmount=500
```

5. Run tests on machine 

```
cd app/tests
pytest
```

# Run on docker

1. Add your api key in .env file.

2. On root path run:

```
docker build -t <image name> .
docker run --name <container-name> -d -p 8080:8080 <image name>
```

3. Navigate to:
```
http://localhost:8080/quote?baseCurrency=USD&quoteCurrency=GBP&baseAmount=250
```
