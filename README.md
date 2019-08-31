## Description

This script converts star data from the [Gaia 2 data repository](http://cdn.gea.esac.esa.int/Gaia/gdr2/gaia_source/csv/) into entires with 3-d coordinates, and color calculated according to rules which can be [found here](http://www.vendian.org/mncharity/dir3/starcolor/details.html).

Only the final results are stored into hard drive (as database entry). Conversion, and data download are done in-memory.

Not every `Gaia 2` entry qualifies for conversion. It must have following parameters measured:
* parallax [coordinates calculation]
* teff_val [color calculation]

## Result

Qualified, converted `Gaia 2` entries end up as following entry in the `star` table:

|     source_id      |  color  |         x         |         y         |         z|
|--------------------|---------|-------------------|-------------------|-------------------|
| 100331161884562048 | #ffecd8 | 0.882547517030588 | 0.558620431078222 | 0.415778835972991 |

where
* *source_id* is `Gaia 2` star id
* *color* is RGB color in hex format
* *x,y,z* are 3d coordinates [parsec]


## Requirements
* Python3
* PostgresSql database
* Internet connection

## How to run

Go to the project directory. Run `./Setup.py` from the main directory to configure parameters. For example:

```
python Setup.py -p "password" -u "postgres" -n "universe_db" -c 13 -r 0.05
```

Run `python Setup.py -h` for help.

After successfully configuring parameters, run following command:
```
python Main.py
```
you will be asked if you want to `Recreate/Initialise tables`. For the first run hit `'Y'` end `'<enter>'`.

## Notes

Converting `Gaia 2` data is extremely lengthy process. Total amount of compressed data to be downloaded is around `100GB` (`500GB` after unpacking). Final result, depending on the chosen value of `ratio`, can be around `100GB`.