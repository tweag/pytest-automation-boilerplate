import structlog
import re

from pytest_bdd import parsers, then
from assertpy import assert_that
from bp_core.frontend.common.helpers.selenium_generics import SeleniumGenerics
from bp_core.frontend.common.utils.locator_parser import Locators
from bp_core.utils.exceptions import DataTableException
from bp_core.utils.gherkin_utils import data_table_horizontal_converter
from bp_core.utils import data_manager

logger = structlog.get_logger(__name__)


@then(parsers.re("I expect table '(?P<locator_path>.*)' headers ('(?P<header_tag_path>.*)' )?to match:(?P<data_table>.*)",
                 flags=re.S, ), converters=dict(data_table=data_table_horizontal_converter),)
def verify_table_headers_match_exactly(selenium_generics: SeleniumGenerics, locators: Locators, locator_path, data_table, header_tag_path):
    header_tag = locators.parse_and_get(header_tag_path, selenium_generics) if header_tag_path else "//th"
    table_headers = selenium_generics.get_elements(f"{locators.parse_and_get(locator_path, selenium_generics)}{header_tag}")
    expected_columns = data_table[list(data_table.keys())[0]]
    columns_present = list()
    for table_header in table_headers:
            columns_present.append(table_header.text)
    assert_that(columns_present).is_equal_to(expected_columns)


@then(parsers.re("I expect table '(?P<locator_path>.*)' headers ('(?P<header_tag_path>.*)' )?to contain:(?P<data_table>.*)",
                 flags=re.S, ), converters=dict(data_table=data_table_horizontal_converter), )
def verify_table_headers_contain_columns(selenium_generics: SeleniumGenerics, locators: Locators, locator_path, data_table, header_tag_path):
    header_tag = locators.parse_and_get(header_tag_path, selenium_generics) if header_tag_path else "//th"
    table_headers = selenium_generics.get_elements(f"{locators.parse_and_get(locator_path, selenium_generics)}{header_tag}")
    expected_columns = data_table[list(data_table.keys())[0]]
    columns_present = list()
    for table_header in table_headers:
            columns_present.append(table_header.text)
    assert_that(columns_present).contains(*expected_columns)


@then(parsers.re("I expect the column in table '(?P<locator_path>.*)' has the values:(?P<data_table>.*)",
                 flags=re.S, ), converters=dict(data_table=data_table_horizontal_converter), )
def verify_table_column_contain_values(selenium_generics: SeleniumGenerics, locators: Locators, locator_path, data_table):
    table_locator = locators.parse_and_get(locator_path, selenium_generics)
    table_header_locator = f"{table_locator}//th | {table_locator}//th//*"
    table_headers = selenium_generics.get_elements(table_header_locator)
    column_names = list(data_table.keys())
    column_index_dict = dict()
    td_index = 0
    for table_header in table_headers:
        if table_header.tag_name.lower() == 'th':
            td_index += 1
        if table_header.text in column_names:
            column_index_dict[table_header.text] = td_index

    for column in column_names:
        for value in data_table[column]:
            cell_locator = f"{table_locator}//tr//td[{column_index_dict[column]}][text()='{value}'] | " \
                           f"{table_locator}//tr//td[{column_index_dict[column]}]//*[text()='{value}']"
            assert len(selenium_generics.get_elements(cell_locator)) > 0


@then(parsers.re("I expect that '(?P<row>.*)' row has the value '(?P<expected_text>.*)' in column '(?P<column>.*)' of table '(?P<locator_path>.*)'"),
    converters=dict(expected_text=data_manager.text_formatted), )
def verify_column_contain_value(selenium_generics: SeleniumGenerics, locators: Locators, locator_path, row, column, expected_text: str):
    table_locator = locators.parse_and_get(locator_path, selenium_generics)
    table_header_locator = f"{table_locator}//th | {table_locator}//th//*"
    table_headers = selenium_generics.get_elements(table_header_locator)
    td_index = 0
    row_number = ''
    row_number = [row_number+i for i in row if i.isdigit()][0]
    for table_header in table_headers:
        if table_header.tag_name.lower() == 'th':
            td_index += 1
        if table_header.text == column:
            break

    cell_locator = f"{table_locator}//tr[{row_number}]//td[{td_index}][text()='{expected_text}'] | " \
                   f"{table_locator}//tr[{row_number}]//td[{td_index}]//*[text()='{expected_text}']"
    assert len(selenium_generics.get_elements(cell_locator)) > 0


@then(parsers.re("I expect that '(?P<row>.*)' row in table '(?P<locator_path>.*)' has the following values:(?P<data_table>.*)",
                 flags=re.S, ), converters=dict(data_table=data_table_horizontal_converter), )
def verify_table_row_contain_values(selenium_generics: SeleniumGenerics, locators: Locators, row, locator_path, data_table):
    table_locator = locators.parse_and_get(locator_path, selenium_generics)
    table_header_locator = f"{table_locator}//th | {table_locator}//th//*"
    table_headers = selenium_generics.get_elements(table_header_locator)
    column_names = list(data_table.keys())
    column_index_dict = dict()
    td_index = 0
    row_number = ''
    row_number = [row_number+i for i in row if i.isdigit()][0]
    for table_header in table_headers:
        if table_header.tag_name.lower() == 'th':
            td_index += 1
        if table_header.text in column_names:
            column_index_dict[table_header.text] = td_index

    if len(data_table[column_names[0]]) > 1:
        raise DataTableException(f"This step can only validate data in one specific row. Data Table from BDD has {len(data_table[column_names[0]]) } rows.")

    for column in column_names:
        cell_locator = f"{table_locator}//tr[{row_number}]//td[{column_index_dict[column]}][text()='{data_table[column][0]}'] | " \
                       f"{table_locator}//tr[{row_number}]//td[{column_index_dict[column]}]//*[text()='{data_table[column][0]}']"
        assert len(selenium_generics.get_elements(cell_locator)) > 0


@then(parsers.re("I expect that table '(?P<locator_path>.*)' has '(?P<value>.*)' rows"),
      converters=dict(value=data_manager.text_formatted), )
def verify_column_contain_value(selenium_generics: SeleniumGenerics, locators: Locators, locator_path, value: int):
    table_row_locator = f"{locators.parse_and_get(locator_path, selenium_generics)}//tr"
    assert_that(len(selenium_generics.get_elements(table_row_locator))).is_equal_to(int(value))
