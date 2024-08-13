# Python Playground

This is a playground for Python.

## Installation

### With Direnv + Nix

```bash
$ direnv allow
$ pip install -r requirements.txt
```

### With Python Virtual Environment

```bash
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

## Usage

### Arrows

#### Help
```bash
$ ./arrows -h
usage: arrow [-h] [-n NUMBER] [-s SYMBOLS [SYMBOLS ...]] [-f FILLERS [FILLERS ...]]

Print an arrow to stdout.

options:
  -h, --help            show this help message and exit
  -n NUMBER, --number NUMBER
                        amount of arrows with size ranging from 0 to 'number' (default: 10)
  -s SYMBOLS [SYMBOLS ...], --symbols SYMBOLS [SYMBOLS ...]
                        symbols to use (default: '*' '#' '$' '@' '&' '+') NOTE: requires '--fillers' of equal length to symbols
  -f FILLERS [FILLERS ...], --fillers FILLERS [FILLERS ...]
                        fillers to use (default: ' ' '.' '`' '_' '^' '~') NOTE: requires '--symbols' be of equal length to fillers
```

#### Example
```bash
$ ./arrow -n 3 -s '*' '#' -f ' ' '.'
########################## 0 ##########################
symbol: '*', filler: ' '  | symbol: '#', filler: '.'  |
------------------------- | ------------------------- |
                          |                           |
  *                       | ..#..                     |
 * *                      | .#.#.                     |
** **                     | ##.##                     |
 * *                      | .#.#.                     |
 ***                      | .###.                     |
                          |                           |
-------------------------------------------------------

########################## 1 ##########################
symbol: '#', filler: '.'  | symbol: '*', filler: ' '  |
------------------------- | ------------------------- |
                          |                           |
...#...                   |    *                      |
..#.#..                   |   * *                     |
.#...#.                   |  *   *                    |
###.###                   | *** ***                   |
..#.#..                   |   * *                     |
..#.#..                   |   * *                     |
..###..                   |   ***                     |
                          |                           |
-------------------------------------------------------

########################## 2 ##########################
symbol: '*', filler: ' '  | symbol: '#', filler: '.'  |
------------------------- | ------------------------- |
                          |                           |
    *                     | ....#....                 |
   * *                    | ...#.#...                 |
  *   *                   | ..#...#..                 |
 *     *                  | .#.....#.                 |
***   ***                 | ###...###                 |
  *   *                   | ..#...#..                 |
  *   *                   | ..#...#..                 |
  *   *                   | ..#...#..                 |
  *****                   | ..#####..                 |
                          |                           |
-------------------------------------------------------
```
