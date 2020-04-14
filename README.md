![build status](https://api.travis-ci.com/michaldeutch/cortex.svg?branch=master)
![coverage](https://codecov.io/gh/michaldeutch/ASDServerClient/branch/master/graph/badge.svg)
# ASDServerClient

An example package. See [full documentation](https://advanced-system-design-foobar.readthedocs.io/en/latest/).

## Installation

1. Clone the repository and enter it:

    ```sh
    $ git clone git@github.com:michaldeutch/ASDServerClient.git
    ...
    $ cd foobar/
    ```

2. Run the installation script and activate the virtual environment:

    ```sh
    $ ./scripts/install.sh
    ...
    $ source .env/bin/activate
    [serverclient] $ # you're good to go!
    ```

3. To check that everything is working as expected, run the tests:


    ```sh
    $ pytest tests/
    ...
    ```

## Usage

The `serverclient` packages provides the following classes:

- `Thought`

    This class encapsulates the concept of `thought`, which includes the
     `user id`, `timestamp`, and the thought itself.


The `serverclient` packages provides the following functionalities:

- `run_server(host, port, data)`

    This function allows running a server on address host;port, 
    and uses directory <data> to store information.
    
- `run_webserver(address, data)`
    This function allows running a web server on address host;port, 
    and uses directory <data> to store information.
    
- `upload_thought(address, user, thought)`

    This function is used to upload thought that is related to a certain
    user, to the server running on address.

The `serverclient` package also provides a command-line interface:

```sh
$ python -m serverclient --version
foobar, version 0.1.0
```

All commands accept the `-q` or `--quiet` flag to suppress output, and the `-t`
or `--traceback` flag to show the full traceback when an exception is raised
(by default, only the error message is printed, and the program exits with a
non-zero code).

The CLI provides the `server` command, with the `run` subcommand:

```sh
$ python -m serverclient server run 127.0.0.1:5000 /tmp/data
```

The CLI further provides the `webserver` command, with the `run` subcommand:

```sh
$ python -m serverclient webserver run localhost:5000 /tmp/data
```

The CLI further provides the `thought` command, with the `upload` subcommand:

```sh
$ python -m serverclient thought upload 127.0.0.1:5000 1 "I'm hungry"
```


Do note that each command's options should be passed to *that* command, so for
example the `-q` and `-t` options should be passed to `server`, not `run`.

```sh
$ python -m serverclient server run -q  127.0.0.1:5000 /tmp/data # this
 doesn't work
ERROR: no such option: -q
$ python -m serverclient -q server run 127.0.0.1:5000 /tmp/data # this does work
```
