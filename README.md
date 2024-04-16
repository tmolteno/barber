# barber

Worlds stupidest tool. Just finds the largest visibility and reports stuff for you.

## Install


Then make sure python3-casacore is installed.

    sudo aptitude install python3-casacore

Just clone this repository:

    git clone https://github.com/tmolteno/barber.git

Then run barber

    python3 barber.py --ms myms.ms

## Usage

    usage: barber.py [-h] --ms MS [--field FIELD] [--debug] [--version]

    Barber: It will remove your fringe in a jiffy.

    options:
    -h, --help     show this help message and exit
    --ms MS        The source measurement set. (default: None)
    --field FIELD  Use this FIELD_ID from the measurement set. (default: 0)
    --debug        Display debugging information (default: False)
    --version      Display the current version (default: False)

## Credits

Thanks to Kenda for inspiring this silly tool.

## TODO

Use dask so that the ms doesn't have to fit in memory at all.

## Changelog

- 0.1.0a1 First test release
