### Installation
#### Set environment variable
The API key can be retrieved from ***Mite &#8594; My user:***
1. Enable "Allow API access"
2. Copy API key
3. Save
4. Set environment variable e.g. in "~/.zprofile" with following entry:
```
export MITE_API_KEY="<your API key>"
```
#### Clone project
```
git clone https://github.com/captain-bu/mite-insights
cd mite-insights
```
#### Create virtual environment
```
python3 -m venv venv
source venv/bin/activate
```

#### Install pypi packages
`pip install -r requirements.txt`

#### Execute code
`python main.py`