# Amtrak Helper Script

## Quickstart

You must set `AMTRAK_GUEST_REWARDS_USERNAME` and
`AMTRAK_GUEST_REWARDS_PASSWORD`, and your profile must be fully filled out for
some of the `--csv` mode stuff to work.

```
pipenv run pytest -vvvv amtrakomatic
pipenv run python amtrakomatic/main.py --csv example.csv
pipenv run python amtrakomatic/main.py --source galesburg --destination denver --date  09/15/2019
pipenv run python amtrakomatic/main.py --source galesburg --destination denver --date  09/15/2019 --use-points
```

Example output (single search mode):

```
pipenv run python amtrakomatic/main.py --source galesburg --destination denver --date 09/14/2019 --use-points
4:38pm -> 7:15am, Sun Sep 15 (15h 37m): $93, $116, $224, $418
    5 California Zephyr           | 4:38pm -> 7:15am, Sun Sep 15 (15h 37m)

5:26pm -> 6:20pm (25h 54m): $145, $169, $280, $447
    3 Southwest Chief             | 5:26pm -> 10:25am, Sun Sep 15 (17h 59m)
        TRANSFER: Raton, NM (2h 50m)
    8406 Thruway Bus              | 1:15pm -> 6:20pm (5h 5m)

5:26pm -> 9:25pm (28h 59m): $145, $169, $280, $447
    3 Southwest Chief             | 5:26pm -> 10:25am, Sun Sep 15 (17h 59m)
        TRANSFER: Raton, NM (7h 5m)
    8604 Thruway Bus              | 5:30pm -> 9:25pm (3h 55m)

4:38pm -> 7:15am, Sun Sep 15 (15h 37m): 4,002 points, 14,421 points
    5 California Zephyr           | 4:38pm -> 7:15am, Sun Sep 15 (15h 37m)

5:26pm -> 6:20pm (25h 54m): 5,831 points, 15,422 points
    3 Southwest Chief             | 5:26pm -> 10:25am, Sun Sep 15 (17h 59m)
        TRANSFER: Raton, NM (2h 50m)
    8406 Thruway Bus              | 1:15pm -> 6:20pm (5h 5m)

5:26pm -> 9:25pm (28h 59m): 5,831 points, 15,422 points
    3 Southwest Chief             | 5:26pm -> 10:25am, Sun Sep 15 (17h 59m)
        TRANSFER: Raton, NM (7h 5m)
    8604 Thruway Bus              | 5:30pm -> 9:25pm (3h 55m)

```

Example output (CSV Mode):

```
$ pipenv run python amtrakomatic/main.py --csv example.csv
['Harrisburg', 'pittsburgh', '08/31/2019', '43 Pennsylvanian', 'dollars']
2:36pm -> 7:59pm (5h 23m): $42, $53, $104, $69
    43 Pennsylvanian              | 2:36pm -> 7:59pm (5h 23m)

Price (dollars): $42.00
['pittsburgh', 'chicago', '08/31/2019', '29 Capitol Limited', 'points']
11:59pm -> 8:45am, Sun Sep 1 (9h 46m): 2,484 points, 8,280 points
    29 Capitol Limited            | 11:59pm -> 8:45am, Sun Sep 1 (9h 46m)

Price (points): 2,484
['chicago', 'kansascity', '09/01/2019', '3 Southwest Chief', 'dollars']
2:50pm -> 10:00pm (7h 10m): $55, $69, $133, $206
    3 Southwest Chief             | 2:50pm -> 10:00pm (7h 10m)

Price (dollars): $55.00
Total point cost: 2484
Total dollar cost: 97.0
```
