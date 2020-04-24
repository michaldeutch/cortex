![build status](https://api.travis-ci.com/michaldeutch/cortex.svg?branch=master)
![coverage](https://codecov.io/gh/michaldeutch/cortex/branch/master/graph/badge.svg)
# cortex

## Installation

1. Clone the repository and enter it:

    ```sh
    $ git clone git@github.com:michaldeutch/cortex.git
    ...
    $ cd cortex/
    ```

2. Run the installation script and activate the virtual environment:

    ```sh
    $ ./scripts/install.sh
    ...
    $ source .env/bin/activate
    [cortex] $ # you're good to go!
    ```

3. To check that everything is working as expected, run the tests:

    ```sh
    $ pytest tests/
    ...
    ```

## Quick Start

1. Run everything:

    ```sh
    $ ./run_pipeline.sh
    ```
   
2. Send you own .mind file (can be .mind.gz):

    ```sh
    $ python -m cortex.client upload-sample <mind_file>
    ```
  
3. Wait for it to finish and check out your browser at 'http://localhost:8080/'

## HowTo add Parser?

1. Add your on `<parser>.py` file [here](cortex/parsers/parsers)

2. Declare in `<parser>.py` one of the two:
    
    * Class in the format:
    ```python
   class MyParser:
       field = 'parser_name'
       def parse(self, data):
           ...
    ```
      
    * Method in the format:
    
    ```python
   def parse_parser(data):
       ...
   
   parse_parser.field = 'parser_name'
    ```

## Usage

* Client

    ```python
  from cortex.client import upload_sample

  upload_sample(host='127.0.0.1', port=8000, path='sample.mind.gz')

    ```
  
  or
  
  ```sh
  $ python -m cortex.client upload-sample \
      -h/--host '127.0.0.1'             \
      -p/--port 8000                    \
      'snapshot.mind.gz'

  ```
  

* Server

    ```python
  from cortex.server import run_server
  def print_message(message):
      print(message)
  run_server(host='127.0.0.1', port=8000, publish=print_message)
    ```
  
  or
  
  ```sh
  $ python -m cortex.server run-server \
      -h/--host '127.0.0.1'          \
      -p/--port 8000                 \
      'rabbitmq://127.0.0.1:5672/'
  ```
  
* Parser

    ```python
  from cortex.parsers import run_parser
  data = {'snapshot': ..., 'user_id': 1}
  result = run_parser('pose', data)
    ```
  
  or
  
  ```sh
  $  python -m cortex.parsers parse 'pose' 'snapshot.raw' > 'pose.result'
  ```
  
  ```sh
  $   python -m cortex.parsers run-parser 'pose' 'rabbitmq://127.0.0.1:5672/'
  ```
  
* Saver

    ```python
  from cortex.saver import Saver
  import json
  
  saver = Saver(database_url='mongodb://127.0.0.1/27017')
  saver.save('pose', json.dumps({
        'user_id': 1,
        'timestamp': 132,
        'content': 'data'
    }))
    ```
  
  or
  
  ```sh
  $  python -m cortex.saver save                     \
      -d/--database 'postgresql://127.0.0.1:5432' \
     'pose'                                       \
     'pose.result' 
  ``` 
 
* Saver

    ```python
  from cortex.api import run_api_server
  
  run_api_server(
      host='127.0.0.1', 
      port=5000, 
      database_url='mongodb://127.0.0.1/27017')
    ```
  
  or
  
  ```sh
  $  python -m cortex.api run-server \
      -h/--host '127.0.0.1'       \
      -p/--port 5000              \
      -d/--database 'mongodb://127.0.0.1/27017'
  ``` 
  
* Cli
  
  ```sh
    $ python -m cortex.cli get-users
    …
    $ python -m cortex.cli get-user 1
    …
    $ python -m cortex.cli get-snapshots 1
    …
    $ python -m cortex.cli get-snapshot 1 2
    …
    $ python -m cortex.cli get-result 1 2 'pose'
    …

  ``` 
  
* Gui - React reflecting Api
   
    ```python
  from cortex.gui import run_server
  
  run_server(
      host='127.0.0.1', 
      port=8080, 
      api_host='127.0.0.1',
      api_port=5000
  )
    ```
  
  or
  
  ```sh
  $ python -m cortex.gui run-server \
      -h/--host '127.0.0.1'       \
      -p/--port 8080              \
      -H/--api-host '127.0.0.1'   \
      -P/--api-port 5000
  ``` 
  