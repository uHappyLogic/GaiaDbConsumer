#!/usr/bin/python
import csv
import gzip
import io
import math
import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed
from distutils.util import strtobool

from tqdm import tqdm

from GaiaHelpers.DbHandler import DbHandler
from GaiaHelpers.GaiaDatafilesGetter import GaiaDatafilesGetter
from GaiaHelpers.LocalConfig import LocalConfig
from GaiaHelpers.StarColorConverter import StarColorConverter

db_handler = None
color_converter = None


def get_db_handler():
    global db_handler
    if db_handler is None:
        db_handler = DbHandler()
    return db_handler


def get_color_converter():
    global color_converter
    if color_converter is None:
        color_converter = StarColorConverter()

    return color_converter


def parallel_procedure(array, procedure, n_jobs=16):
    if n_jobs == 1:
        for a in tqdm(array):
            procedure(a)

    with ProcessPoolExecutor(max_workers=n_jobs) as pool:
        futures = [pool.submit(procedure, a) for a in array]

        for _ in tqdm(as_completed(futures), total=len(futures)):
            pass


class BatchSaver:
    queue = []

    def save(self, s_id, hex_color, x, y, z):
        self.queue.append([s_id, hex_color, x, y, z])

        if len(self.queue) == 400:
            self.flush()

    def flush(self):

        if len(self.queue) == 0:
            return

        get_db_handler().bulk_save_to_db(self.queue)
        self.queue = []


def handle_file(file):
    try:
        if get_db_handler().check_if_done(file):
            return

        saver = BatchSaver()
        with GaiaDatafilesGetter.get_file_request(file) as request:
            with gzip.open(io.BytesIO(request.content), mode="rt") as csv_file:
                headers = []

                lines = [line for line in csv_file]

                first = True

                qualified_stars = 0

                for row in csv.reader(lines, delimiter=','):
                    if first:
                        first = False
                        headers = row
                    else:
                        if row[headers.index('parallax')] == '':
                            continue

                        if row[headers.index('teff_val')] == '':  # stellar effective temperature (float, [K])
                            continue

                        qualified_stars = (qualified_stars + 1) % int(1 / LocalConfig.get_star_ratio())

                        if qualified_stars != 1:
                            continue

                        rec = [row[headers.index(x)] for x in ['source_id', 'ra', 'dec', 'teff_val']]
                        parallax = 1 / float(row[headers.index('parallax')])

                        deg2_rad = math.pi / 180

                        x_coord = math.cos(float(rec[1]) * deg2_rad) * math.cos(float(rec[2]) * deg2_rad) * parallax
                        y_coord = math.sin(float(rec[1]) * deg2_rad) * math.cos(float(rec[2]) * deg2_rad) * parallax
                        z_coord = math.sin(float(rec[2]) * deg2_rad) * parallax

                        saver.save(rec[0], get_color_converter().get_color(float(rec[3])), x_coord, y_coord, z_coord)

        saver.flush()
        get_db_handler().mark_as_done(file)

    except Exception as e:
        print("Exception happened while converting {}".format(file))
        print(e)
        traceback.print_exc()


def files_converter(files):
    parallel_procedure(files, handle_file, n_jobs=LocalConfig.get_workers_count())


if __name__ == "__main__":
    if strtobool(input("Recreate/Initialise tables [Y/n]?\n")):
        get_db_handler().drop_tables()
        get_db_handler().create_tables()

    files_converter(GaiaDatafilesGetter.get_files_list())
