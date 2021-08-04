# SFERA

An open-source infrastructure for the 99%.

## Installation

Clone the repository and run the installation script:

```sh
/home/user$ git clone git@github.com:sfera-institute/sfera.git
...
/home/user$ cd sfera/
/home/user/sfera$ scripts/install.sh
...
```

To work on SFERA, activate the virtual environment, and you should be good to go:

```sh
/home/user/sfera$ . .env/bin/activate
(sfera) /home/user/sfera$ # Ready to roll!
```

To use SFERA in another project, run the distribution script (just make sure you've activated the virtual
environment of the other project, so SFERA gets installed there; or, more generally, that your `python`
command resolves to whatever Python distribution you want to install SFERA in):

```sh
/home/user/sfera$ ./scripts/distribute.sh
...
/home/user/sfera$ python
>>> import sfera # Ta-da!
```

## Usage

```python
>>> import sfera
>>> sfera.version
'0.1.0'
```

## Reference

- [Auto-Import](docs/autoimport.md)

  A mechanism that automatically collects and exposes SFERA's public API.

- [Classes](docs/classes.md)

  A collection of useful classes.

- [Functions](docs/functions.md)

  A collection of useful functions.