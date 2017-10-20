from __future__ import absolute_import, division, print_function
import bonobo
import os
from shutil import copyfile

from olapy.core.mdx.executor.execute import MdxEngine

GEN_FOLDER = 'etl_generated'


class ETL(object):
    def __init__(self,
                 source_type,
                 facts_table,
                 source_folder='input_demos',
                 separator=None,
                 target_cube='etl_cube'):
        """

        :param source_type: csv | file | pickle
        :param headers:
        """
        self.source_type = source_type
        self.facts_table = facts_table
        self.cube_path = MdxEngine._get_default_cube_directory()
        self.seperator = self._get_default_seperator() if not separator else separator
        self.target_cube = target_cube
        self.source_folder = source_folder
        self.olapy_cube_path = os.path.join(
            MdxEngine._get_default_cube_directory(), MdxEngine.CUBE_FOLDER)
        # pass some data to transform without bonobo shitty configuration
        self.current_dim_id_column = None
        self.dim_first_row_headers = True
        self.dim_headers = []
        if not os.path.exists(GEN_FOLDER):
            os.mkdir(GEN_FOLDER)
        if os.listdir(GEN_FOLDER):
            for file in os.listdir(GEN_FOLDER):
                os.remove(os.path.join(GEN_FOLDER, file))

    def _get_default_seperator(self):
        if self.source_type.upper() in ['CSV', 'FILE']:
            return ','

    def add_id_prefix(self, header):
        headers = []
        for column_header in header:
            if column_header in self.current_dim_id_column and '_id' not in column_header[-3:]:
                column_header = column_header + '_id'
            headers.append(column_header)
        return headers

    def transform_file(self, line):
        """

        :param table_type: facts | dimension
        :return:
        """
        # fix
        line = line[0]
        transformed = {}

        if self.dim_first_row_headers:
            # split headers
            splited = line.split(self.seperator)
            self.dim_headers = splited
            self.dim_first_row_headers = False
            for idx, column_header in enumerate(splited):
                if column_header in self.current_dim_id_column and '_id' not in column_header[-3:]:
                    splited[idx] = column_header + '_id'

        else:
            if self.dim_headers:
                splited = line.split(
                    self.seperator, maxsplit=len(self.dim_headers))
            else:
                # columns = self.current_dim_id_column
                splited = line.split(self.seperator)

            for idx, head in enumerate(self.dim_headers):
                transformed.update({head: splited[idx]})

        return transformed

    def transform_csv(self, kwargs):
        if self.dim_first_row_headers:
            for key in self.current_dim_id_column:
                if '_id' not in key:
                    kwargs[key + '_id'] = kwargs[key]
                    del kwargs[key]
        return kwargs

    def transform(self, *args, **kwargs):
        """

        :param table_type: facts | dimension
        :return:
        """
        if self.source_type.upper() == 'FILE':
            return self.transform_file(args)

        elif self.source_type.upper() == 'CSV':
            return self.transform_csv(kwargs)

    def extract(self, file, delimiter=';'):
        """

        :param file: file | csv | json | pickle
        :return:
        """
        # todo clean this
        if self.source_type.upper() == 'FILE':
            return getattr(bonobo, self.source_type.title() + "Reader")(file)
        elif self.source_type.upper() == 'CSV':
            return getattr(bonobo, self.source_type.title() + "Reader")(file, **{'delimiter': delimiter})

    def load(self, table_name, target='csv'):

        # todo target postgres, mysql ....
        if target.upper() == 'CSV':
            # todo headers if there is not headers
            # os.chdir(self.target_cube)
            if table_name == self.facts_table:
                table_name = 'Facts'
            return bonobo.CsvWriter(
                os.path.join(GEN_FOLDER, table_name + '.csv'), ioformat='arg0')

    def copy_2_olapy_dir(self):
        if not os.path.isdir(
                os.path.join(self.olapy_cube_path, self.target_cube)):
            os.makedirs(os.path.join(self.olapy_cube_path, self.target_cube))

        self.target_cube = os.path.join(self.olapy_cube_path, self.target_cube)

        for file in os.listdir(GEN_FOLDER):
            copyfile(
                os.path.join(GEN_FOLDER, file),
                os.path.join(self.target_cube, file))

    def get_source_extension(self):
        if self.source_type.upper() == 'FILE':
            return '.txt'
        elif self.source_type.upper() == 'CSV':
            return '.csv'


def run_olapy_etl(dims_infos, facts_table, facts_ids, source_folder='input_demos', source_type='csv', in_delimiter=','):
    """

    :param dims_infos: example : dims_infos = {
                                            'Geography': ['geography_key'],
                                            'Product': ['product_key']
                                             }
    :param facts_table: facts table name
    :param facts_ids: example : facts_ids = ['geography_key', 'product_key']
    :param source_folder: where to get your files
    :param source_type: file : .txt files in input || csv : .csv files in input
    :return: generate files to olapy dir
    """

    # source_type -> file : .txt files in input
    # source_type -> csv : .csv files in input
    etl = ETL(
        source_type=source_type,
        facts_table=facts_table,
        source_folder=source_folder)

    for table in list(dims_infos.keys()) + [etl.facts_table]:
        # for each new file
        etl.dim_first_row_headers = True
        if table == etl.facts_table:
            etl.current_dim_id_column = facts_ids
        else:
            etl.current_dim_id_column = dims_infos[table]

        graph = bonobo.Graph(
            etl.extract(os.path.join(etl.source_folder, table + etl.get_source_extension()), delimiter=in_delimiter),
            etl.transform, etl.load(table))

        bonobo.run(graph)

    # temp ( bonobo can't export (save) to path (bonobo bug)
    etl.copy_2_olapy_dir()