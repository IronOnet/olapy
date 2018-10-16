"""
Managing all `DISCOVER <https://technet.microsoft.com/fr-fr/library/ms186653(v=sql.110).aspx>`_ requests and responses
"""
# -*- encoding: utf8 -*-

from __future__ import absolute_import, division, print_function, \
    unicode_literals

import os
from .xmla_discover_tools import XmlaTools
from ..services.xmla_discover_tools_utils import discover_literals_response_rows, \
    discover_schema_rowsets_response_rows


# noinspection PyPep8Naming


class DictXmlaTools(XmlaTools):
    """DictXmlaTools for generating xmla discover responses."""

    def __init__(self, mdx_engine):
        """

        :param mdx_engine: mdx_engine engine instance

        """
        super().__init__(mdx_engine)

    @staticmethod
    def discover_datasources_response():
        return {
            'DataSourceName': 'sales',
            'DataSourceDescription': "sales Sample Data",
            'URL': "http://127.0.0.1:8000/xmla",
            'DataSourceInfo': "-",
            'ProviderName': "olapy",
            'ProviderType': "MDP",
            'AuthenticationMode': "Unauthenticated",
        }

    @staticmethod
    def _get_props(
        xsd,
        PropertyName,
        PropertyDescription,
        PropertyType,
        PropertyAccessType,
        IsRequired,
        Value,
    ):

        if PropertyName is not "":
            response = [{
                'PropertyName': PropertyName,
                'PropertyDescription': PropertyDescription,
                'PropertyType': PropertyType,
                'PropertyAccessType': PropertyAccessType,
                'IsRequired': IsRequired,
                'Value': Value
            }]

        else:
            properties_names_n_description = [
                "ServerName",
                "ProviderVersion",
                "MdpropMdxSubqueries",
                "MdpropMdxDrillFunctions",
                "MdpropMdxNamedSets",
            ]
            properties_types = ["string", "string", "int", "int", "int"]
            values = [
                os.getenv("USERNAME", "default"),
                "0.0.3  25-Nov-2016 07:20:28 GMT",
                "15",
                "3",
                "15",
            ]

            response = []
            for idx, prop_desc in enumerate(
                properties_names_n_description, ):
                response += {
                    'PropertyName': prop_desc,
                    'PropertyDescription': prop_desc,
                    'PropertyType': properties_types[idx],
                    'PropertyAccessType': "Read",
                    'IsRequired': "false",
                    'Value': values[idx]
                }

        return response

    def discover_schema_rowsets_response(self, request):

        rows = discover_schema_rowsets_response_rows

        def generate_resp(rows):
            responses = []
            for resp_row in rows:
                response = {
                    'SchemaName': resp_row["SchemaName"],
                    'SchemaGuid': resp_row["SchemaGuid"],
                }
                restrictions = []
                for idx, restriction in enumerate(
                    resp_row["restrictions"][
                        "restriction_names"], ):
                    restrictions += {
                        'Name': restriction,
                        'Type': resp_row["restrictions"][
                            "restriction_types"][idx]
                    }
                response['Restrictions'] = restrictions
                response['RestrictionsMask'] = resp_row["RestrictionsMask"]
                responses += response

            return responses

        restriction_list = request.Restrictions.RestrictionList
        if (restriction_list.SchemaName == "MDSCHEMA_HIERARCHIES" and
            request.Properties.PropertyList.Catalog is not None):
            self.change_catalogue(request.Properties.PropertyList.Catalog)

            restriction_names = [
                "CATALOG_NAME",
                "SCHEMA_NAME",
                "CUBE_NAME",
                "DIMENSION_UNIQUE_NAME",
                "HIERARCHY_NAME",
                "HIERARCHY_UNIQUE_NAME",
                "HIERARCHY_ORIGIN",
                "CUBE_SOURCE",
                "HIERARCHY_VISIBILITY",
            ]
            restriction_types = [
                "string",
                "string",
                "string",
                "string",
                "string",
                "string",
                "unsignedShort",
                "unsignedShort",
                "unsignedShort",
            ]

            rows = [
                {
                    "SchemaName": "MDSCHEMA_HIERARCHIES",
                    "SchemaGuid": "C8B522DA-5CF3-11CE-ADE5-00AA0044773D",
                    "restrictions": {
                        "restriction_names": restriction_names,
                        "restriction_types": restriction_types,
                    },
                    "RestrictionsMask": "511",
                },
            ]

            return generate_resp(rows)

        if (restriction_list.SchemaName == "MDSCHEMA_MEASURES" and
            request.Properties.PropertyList.Catalog is not None):
            self.change_catalogue(request.Properties.PropertyList.Catalog)

            restriction_names = [
                "CATALOG_NAME",
                "SCHEMA_NAME",
                "CUBE_NAME",
                "MEASURE_NAME",
                "MEASURE_UNIQUE_NAME",
                "MEASUREGROUP_NAME",
                "CUBE_SOURCE",
                "MEASURE_VISIBILITY",
            ]
            restriction_types = [
                "string",
                "string",
                "string",
                "string",
                "string",
                "string",
                "unsignedShort",
                "unsignedShort",
            ]

            rows = [
                {
                    "SchemaName": "MDSCHEMA_MEASURES",
                    "SchemaGuid": "C8B522DC-5CF3-11CE-ADE5-00AA0044773D",
                    "restrictions": {
                        "restriction_names": restriction_names,
                        "restriction_types": restriction_types,
                    },
                    "RestrictionsMask": "255",
                },
            ]

            return generate_resp(rows)

        ext = [
            {
                "SchemaName": "DBSCHEMA_TABLES",
                "SchemaGuid": "C8B52229-5CF3-11CE-ADE5-00AA0044773D",
                "restrictions": {
                    "restriction_names": [
                        "TABLE_CATALOG",
                        "TABLE_SCHEMA",
                        "TABLE_NAME",
                        "TABLE_TYPE",
                        "TABLE_OLAP_TYPE",
                    ],
                    "restriction_types": [
                        "string",
                        "string",
                        "string",
                        "string",
                        "string",
                    ],
                },
                "RestrictionsMask": "31",
            },
            {
                "SchemaName": "DISCOVER_DATASOURCES",
                "SchemaGuid": "06C03D41-F66D-49F3-B1B8-987F7AF4CF18",
                "restrictions": {
                    "restriction_names": [
                        "DataSourceName",
                        "URL",
                        "ProviderName",
                        "ProviderType",
                        "AuthenticationMode",
                    ],
                    "restriction_types": [
                        "string",
                        "string",
                        "string",
                        "string",
                        "string",
                    ],
                },
                "RestrictionsMask": "31",
            },
            {
                "SchemaName": "DISCOVER_INSTANCES",
                "SchemaGuid": "20518699-2474-4C15-9885-0E947EC7A7E3",
                "restrictions": {
                    "restriction_names": ["INSTANCE_NAME"],
                    "restriction_types": ["string"],
                },
                "RestrictionsMask": "1",
            },
            {
                "SchemaName": "DISCOVER_KEYWORDS",
                "SchemaGuid": "1426C443-4CDD-4A40-8F45-572FAB9BBAA1",
                "restrictions": {
                    "restriction_names": ["Keyword"],
                    "restriction_types": ["string"],
                },
                "RestrictionsMask": "1",
            },
        ]

        ext.extend(rows)

        return generate_resp(ext)

    @staticmethod
    def discover_literals_response(request):
        if (request.Properties.PropertyList.Content == "SchemaData" and
            request.Properties.PropertyList.Format == "Tabular"):

            rows = discover_literals_response_rows

            response = {}
            for resp_row in rows:
                for att_name, value in resp_row.items():
                    response[att_name] = value

            return response

    def dbschema_catalogs_response(self, request):

        return {
            'CATALOG_NAME': [catalogue for catalogue in self.catalogues]
        }

    def mdschema_cubes_response(self, request):
        if (request.Restrictions.RestrictionList.CUBE_NAME ==
            self.selected_catalogue or
            request.Properties.PropertyList.Catalog is not None):
            self.change_catalogue(request.Properties.PropertyList.Catalog)

            return {
                'CATALOG_NAME': self.selected_catalogue,
                'CUBE_NAME': self.selected_catalogue,
                'CUBE_TYPE': "CUBE",
                'LAST_SCHEMA_UPDATE': "2016-07-22T10:41:38",
                'LAST_DATA_UPDATE': "2016-07-22T10:41:38",
                'DESCRIPTION':
                    "MDX " + self.selected_catalogue + " results",
                'IS_DRILLTHROUGH_ENABLED': "true",
                'IS_LINKABLE': "false",
                'IS_WRITE_ENABLED': "false",
                'IS_SQL_ENABLED': "false",
                'CUBE_CAPTION': self.selected_catalogue,
                'CUBE_SOURCE': "1"
            }

    def dbschema_tables_response(self, request):
        if request.Properties.PropertyList.Catalog is not None:
            self.change_catalogue(request.Properties.PropertyList.Catalog)
            return ''

    def mdschema_measures_response(self, request):
        if (request.Restrictions.RestrictionList.CUBE_NAME ==
            self.selected_catalogue and
            request.Properties.PropertyList.Catalog is not None):
            self.change_catalogue(request.Properties.PropertyList.Catalog)

            return [{
                'CATALOG_NAME': self.selected_catalogue,
                'CUBE_NAME': self.selected_catalogue,
                'MEASURE_NAME': mes,
                'MEASURE_UNIQUE_NAME': "[Measures].[" + mes + "]",
                'MEASURE_CAPTION': mes,
                'MEASURE_AGGREGATOR': "1",
                'DATA_TYPE': "5",
                'NUMERIC_PRECISION': "16",
                'NUMERIC_SCALE': "-1",
                'MEASURE_IS_VISIBLE': "true",
                'MEASURE_NAME_SQL_COLUMN_NAME': mes,
                'MEASURE_UNQUALIFIED_CAPTION': mes,
                'MEASUREGROUP_NAME': "default",
            } for mes in self.executor.measures]

    def mdschema_dimensions_response(self, request):
        if (request.Restrictions.RestrictionList.CUBE_NAME ==
            self.selected_catalogue and
            request.Restrictions.RestrictionList.CATALOG_NAME ==
            self.selected_catalogue and
            request.Properties.PropertyList.Catalog is not None):

            self.change_catalogue(request.Properties.PropertyList.Catalog)
            ord = 1

            rows = []
            for tables in self.executor.get_all_tables_names(
                ignore_fact=True, ):
                rows += {
                    "CATALOG_NAME": self.selected_catalogue,
                    "CUBE_NAME": self.selected_catalogue,
                    "DIMENSION_NAME": tables,
                    "DIMENSION_UNIQUE_NAME": "[" + tables + "]",
                    "DIMENSION_CAPTION": tables,
                    "DIMENSION_ORDINAL": str(ord),
                    "DIMENSION_TYPE": "3",
                    "DIMENSION_CARDINALITY": "23",
                    "DEFAULT_HIERARCHY":
                        "[" + tables + "].[" + tables + "]",
                    "IS_VIRTUAL": "false",
                    "IS_READWRITE": "false",
                    "DIMENSION_UNIQUE_SETTINGS": "1",
                    "DIMENSION_IS_VISIBLE": "true",
                }

                ord += 1

            # for measure
            rows += {
                "CATALOG_NAME": self.selected_catalogue,
                "CUBE_NAME": self.selected_catalogue,
                "DIMENSION_NAME": "Measures",
                "DIMENSION_UNIQUE_NAME": "[Measures]",
                "DIMENSION_CAPTION": "Measures",
                "DIMENSION_ORDINAL": str(ord),
                "DIMENSION_TYPE": "2",
                "DIMENSION_CARDINALITY": "0",
                "DEFAULT_HIERARCHY": "[Measures]",
                "IS_VIRTUAL": "false",
                "IS_READWRITE": "false",
                "DIMENSION_UNIQUE_SETTINGS": "1",
                "DIMENSION_IS_VISIBLE": "true",
            }

            return rows

    def mdschema_hierarchies_response(self, request):
        # Enumeration of hierarchies in all dimensions
        restriction_list = request.Restrictions.RestrictionList
        rows = []
        if (restriction_list.CUBE_NAME == self.selected_catalogue and
            request.Properties.PropertyList.Catalog is not None):

            self.change_catalogue(request.Properties.PropertyList.Catalog)
            if (restriction_list.HIERARCHY_VISIBILITY == 3 or
                restriction_list.CATALOG_NAME ==
                self.selected_catalogue):

                for table_name, df in self.executor.tables_loaded.items():
                    if table_name == self.executor.facts:
                        continue

                    column_attribut = df.iloc[0][0]
                    rows += {
                        "CATALOG_NAME": self.selected_catalogue,
                        "CUBE_NAME": self.selected_catalogue,
                        "DIMENSION_UNIQUE_NAME":
                            "[" + table_name + "]",
                        "HIERARCHY_NAME": table_name,
                        "HIERARCHY_UNIQUE_NAME":
                            "[{0}].[{0}]".format(table_name),
                        "HIERARCHY_CAPTION": table_name,
                        "DIMENSION_TYPE": "3",
                        "HIERARCHY_CARDINALITY": "6",
                        "DEFAULT_MEMBER":
                            "[{0}].[{0}].[{1}].[{2}]".format(
                                table_name,
                                df.columns[0],
                                column_attribut,
                            ),
                        "STRUCTURE": "0",
                        "IS_VIRTUAL": "false",
                        "IS_READWRITE": "false",
                        "DIMENSION_UNIQUE_SETTINGS": "1",
                        "DIMENSION_IS_VISIBLE": "true",
                        "HIERARCHY_ORDINAL": "1",
                        "DIMENSION_IS_SHARED": "true",
                        "HIERARCHY_IS_VISIBLE": "true",
                        "HIERARCHY_ORIGIN": "1",
                        "INSTANCE_SELECTION": "0",
                    }

                rows += {
                    "CATALOG_NAME": self.selected_catalogue,
                    "CUBE_NAME": self.selected_catalogue,
                    "DIMENSION_UNIQUE_NAME": "[Measures]",
                    "HIERARCHY_NAME": "Measures",
                    "HIERARCHY_UNIQUE_NAME": "[Measures]",
                    "HIERARCHY_CAPTION": "Measures",
                    "DIMENSION_TYPE": "2",
                    "HIERARCHY_CARDINALITY": "0",
                    "DEFAULT_MEMBER": "[Measures].[{}]".format(
                        self.executor.measures[0], ),
                    "STRUCTURE": "0",
                    "IS_VIRTUAL": "false",
                    "IS_READWRITE": "false",
                    "DIMENSION_UNIQUE_SETTINGS": "1",
                    "DIMENSION_IS_VISIBLE": "true",
                    "HIERARCHY_ORDINAL": "1",
                    "DIMENSION_IS_SHARED": "true",
                    "HIERARCHY_IS_VISIBLE": "true",
                    "HIERARCHY_ORIGIN": "1",
                    "INSTANCE_SELECTION": "0",
                }

            return rows

    def mdschema_levels_response(self, request):
        rows = []
        if (request.Restrictions.RestrictionList.CUBE_NAME ==
            self.selected_catalogue and
            request.Properties.PropertyList.Catalog is not None):

            self.change_catalogue(request.Properties.PropertyList.Catalog)

            for tables in self.executor.get_all_tables_names(
                ignore_fact=True, ):
                l_nb = 0
                for col in self.executor.tables_loaded[tables].columns:
                    rows.append({
                        "CATALOG_NAME": self.selected_catalogue,
                        "CUBE_NAME": self.selected_catalogue,
                        "DIMENSION_UNIQUE_NAME": "[" + tables + "]",
                        "HIERARCHY_UNIQUE_NAME": "[{0}].[{0}]".format(tables),
                        "LEVEL_NAME": str(col),
                        "LEVEL_UNIQUE_NAME": "[{0}].[{0}].[{1}]".format(tables, col),
                        "LEVEL_CAPTION": str(col),
                        "LEVEL_NUMBER": str(l_nb),
                        "LEVEL_CARDINALITY": "0",
                        "LEVEL_TYPE": "0",
                        "CUSTOM_ROLLUP_SETTINGS": "0",
                        "LEVEL_UNIQUE_SETTINGS": "0",
                        "LEVEL_IS_VISIBLE": "true",
                        "LEVEL_DBTYPE": "130",
                        "LEVEL_KEY_CARDINALITY": "1",
                        "LEVEL_ORIGIN": "2"
                    })
                    l_nb += 1

            rows += {
                "CATALOG_NAME": self.selected_catalogue,
                "CUBE_NAME": self.selected_catalogue,
                "DIMENSION_UNIQUE_NAME": "[Measures]",
                "HIERARCHY_UNIQUE_NAME": "[Measures]",
                "LEVEL_NAME": "MeasuresLevel",
                "LEVEL_UNIQUE_NAME": "[Measures]",
                "LEVEL_CAPTION": "MeasuresLevel",
                "LEVEL_NUMBER": "0",
                "LEVEL_CARDINALITY": "0",
                "LEVEL_TYPE": "0",
                "CUSTOM_ROLLUP_SETTINGS": "0",
                "LEVEL_UNIQUE_SETTINGS": "0",
                "LEVEL_IS_VISIBLE": "true",
                "LEVEL_DBTYPE": "130",
                "LEVEL_KEY_CARDINALITY": "1",
                "LEVEL_ORIGIN": "2", }

            return rows

    def mdschema_measuregroups_response(self, request):
        if (request.Restrictions.RestrictionList.CUBE_NAME ==
            self.selected_catalogue and
            request.Properties.PropertyList.Catalog is not None):
            self.change_catalogue(request.Properties.PropertyList.Catalog)

            return {
                "CATALOG_NAME": self.selected_catalogue,
                "CUBE_NAME": self.selected_catalogue,
                "MEASUREGROUP_NAME": "default",
                "DESCRIPTION": "-",
                "IS_WRITE_ENABLED": "true",
                "MEASUREGROUP_CAPTION": "default",
            }

    def mdschema_measuregroup_dimensions_response(self, request):
        if (request.Restrictions.RestrictionList.CUBE_NAME ==
            self.selected_catalogue and
            request.Properties.PropertyList.Catalog is not None):
            self.change_catalogue(request.Properties.PropertyList.Catalog)

            return [{"CATALOG_NAME": self.selected_catalogue,
                     "CUBE_NAME": self.selected_catalogue,
                     "MEASUREGROUP_NAME": "default",
                     "MEASUREGROUP_CARDINALITY": "ONE",
                     "DIMENSION_UNIQUE_NAME": "[" + tables + "]",
                     "DIMENSION_CARDINALITY": "MANY",
                     "DIMENSION_IS_VISIBLE": "true",
                     "DIMENSION_IS_FACT_DIMENSION": "false",
                     "DIMENSION_GRANULARITY": "[{0}].[{0}]".format(tables),
                     } for tables in self.executor.get_all_tables_names(ignore_fact=True)]

    def mdschema_properties_response(self, request):
        if (request.Restrictions.RestrictionList.PROPERTY_TYPE == 2 and
            request.Properties.PropertyList.Catalog is not None):
            properties_names = [
                "FONT_FLAGS",
                "LANGUAGE",
                "style",
                "ACTION_TYPE",
                "FONT_SIZE",
                "FORMAT_STRING",
                "className",
                "UPDATEABLE",
                "BACK_COLOR",
                "CELL_ORDINAL",
                "FONT_NAME",
                "VALUE",
                "FORMATTED_VALUE",
                "FORE_COLOR",
            ]
            properties_captions = [
                "FONT_FLAGS",
                "LANGUAGE",
                "style",
                "ACTION_TYPE",
                "FONT_SIZE",
                "FORMAT_STRING",
                "className",
                "UPDATEABLE",
                "BACK_COLOR",
                "CELL_ORDINAL",
                "FONT_NAME",
                "VALUE",
                "FORMATTED_VALUE",
                "FORE_COLOR",
            ]
            properties_datas = [
                "3",
                "19",
                "130",
                "19",
                "18",
                "130",
                "130",
                "19",
                "19",
                "19",
                "130",
                "12",
                "130",
                "19",
            ]

            self.change_catalogue(request.Properties.PropertyList.Catalog)

            return [{"CATALOG_NAME": self.selected_catalogue,
                     "PROPERTY_TYPE": "2",
                     "PROPERTY_NAME": prop_name,
                     "PROPERTY_CAPTION": properties_captions[idx],
                     "DATA_TYPE": properties_datas[idx]} for idx, prop_name in enumerate(properties_names)
                    ]

        elif request.Restrictions.RestrictionList.PROPERTY_TYPE == 1:
            return ""

    def mdschema_members_response(self, request):
        # Enumeration of hierarchies in all dimensions
        if (request.Restrictions.RestrictionList.CUBE_NAME ==
            self.selected_catalogue and
            request.Properties.PropertyList.Catalog is not None and
            request.Restrictions.RestrictionList.TREE_OP == 8):
            self.change_catalogue(request.Properties.PropertyList.Catalog)
            separed_tuple = self.executor.parser.split_tuple(
                request.Restrictions.RestrictionList.MEMBER_UNIQUE_NAME, )
            joined = ".".join(separed_tuple[:-1])
            # exple
            # separed_tuple -> [Product].[Product].[Company].[Crazy Development]
            # joined -> [Product].[Product].[Company]

            last_attribut = "".join(
                att for att in separed_tuple[-1] if att not in "[]").replace(
                "&",
                "&amp;",
            )

            return {"CATALOG_NAME": self.selected_catalogue,
                    "CUBE_NAME": self.selected_catalogue,
                    "DIMENSION_UNIQUE_NAME": separed_tuple[0],
                    "HIERARCHY_UNIQUE_NAME": "{0}.{0}".format(
                        separed_tuple[0], ),
                    "LEVEL_UNIQUE_NAME": joined,
                    "LEVEL_NUMBER": "0",
                    "MEMBER_ORDINAL": "0",
                    "MEMBER_NAME": last_attribut,
                    "MEMBER_UNIQUE_NAME": request.Restrictions.RestrictionList.
                        MEMBER_UNIQUE_NAME,
                    "MEMBER_TYPE": "1",
                    "MEMBER_CAPTION": last_attribut,
                    "CHILDREN_CARDINALITY": "1",
                    "PARENT_LEVEL": "0",
                    "PARENT_COUNT": "0",
                    "MEMBER_KEY": last_attribut,
                    "IS_PLACEHOLDERMEMBER": "false",
                    "IS_DATAMEMBER": "false"
                    }