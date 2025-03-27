# Ohjelmistotekniikka
[Laskarit](https://github.com/rautiais/ot-harjoitustyo/tree/main/laskarit)

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
2. Perform the required initialization operations with the command:
```
poetry run invoke build
```
3. Start the application with the command:
```
poetry run invoke start
```