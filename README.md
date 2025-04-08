## Volleyball Statistics Tracking Application

The _volleyball statistics tracking application_ is used for tracking various **statistics** in a volleyball game, initially focusing on serve-receive.

## Documentation

- [Requirements Specification](https://github.com/rautiais/ot-harjoitustyo/blob/main/volleystats-app/dokumentaatio/vaatimusmaarittely.md)
- [Time sheets](https://github.com/rautiais/ot-harjoitustyo/blob/main/volleystats-app/dokumentaatio/tuntikirjanpito.md)
- [Changelog](https://github.com/rautiais/ot-harjoitustyo/blob/main/volleystats-app/dokumentaatio/changelog.md)

## Installation

### Startup instructions

1. Install the dependencies with the command:
```
poetry install
```
2. Start the application with the command:
```
poetry run invoke start
```

### Testing

Run tests with the command:
```
poetry run invoke test
```

### Pylint

Run the checks defined in the file [.pylintrc](https://github.com/rautiais/ot-harjoitustyo/blob/main/volleystats-app/.pylintrc) with the command:
```
poetry run invoke lint
```