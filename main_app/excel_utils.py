#!/usr/bin/python
# -*- coding: utf-8 -*-
from io import StringIO, BytesIO
import xlsxwriter
from django.utils.translation import ugettext
from django.db.models import Avg, Sum, Max, Min

from .models import ItemRank 


def WriteToExcel(rank, kwd=None):
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet_s = workbook.add_worksheet("Sheet1")

    # excel styles
    title = workbook.add_format({
        'bold': True,
        'font_size': 14,
        'align': 'center',
        'valign': 'vcenter'
    })
    header = workbook.add_format({
        'bg_color': '#F7F7F7',
        'color': 'black',
        'align': 'center',
        'valign': 'top',
        'border': 1
    })
    cell = workbook.add_format({
        'align': 'left',
        'valign': 'top',
        'text_wrap': True,
        'border': 1
    })
    cell_center = workbook.add_format({
        'align': 'center',
        'valign': 'top',
        'border': 1
    })

    # write title
    if kwd:
        title_text = kwd
    else:
        title_text = ugettext("export excel")
    title_text = u"{0}".format(title_text)
    # merge cells
    worksheet_s.merge_range('A2:G2', title_text)

    # write header
    worksheet_s.write(4, 0, ugettext("No"), header)
    worksheet_s.write(4, 1, ugettext("Date"), header)
    worksheet_s.write(4, 2, ugettext("Time"), header)
    worksheet_s.write(4, 3, ugettext("Keyword"), header)
    worksheet_s.write(4, 4, ugettext("Rank"), header)
    worksheet_s.write(4, 5, ugettext("Title"), header)
    worksheet_s.write(4, 6, ugettext("Price"), header)

    # column widths
    title_col_width = 100
    keyword_col_width = 10
    price_col_width = 10

    # add data to the table
    for idx, data in enumerate(rank):
        row = 5 + idx
        worksheet_s.write_number(row, 0, idx + 1, cell_center)
        
        worksheet_s.write_string(row, 1, data.stt_de, cell)
        worksheet_s.write_string(row, 2, data.stt_tm, cell)
            
        worksheet_s.write_string(row, 3, data.keyword, cell)
        if len(data.keyword) > keyword_col_width:
            keyword_col_width = len(data.keyword)
        

        #worksheet_s.write(row, 2, data.date.strftime('%d/%m/%Y'), cell_center)
        worksheet_s.write_number(row, 4, data.rk, cell_center)
        worksheet_s.write_string(row, 5, data.title, cell)
        if len(data.title) > title_col_width:
            title_col_width = len(data.title)

        worksheet_s.write_string(row, 6, str(data.price), cell_center)
     

    # change column widths
    worksheet_s.set_column('B:B', 11)  # Date column
    worksheet_s.set_column('C:C', 11)  # Time column
    worksheet_s.set_column('D:D', keyword_col_width)  # Keyword column
    worksheet_s.set_column('E:E', 10)  # Rank column
    worksheet_s.set_column('F:F', title_col_width)  # Title column
    worksheet_s.set_column('G:G', 10)  # Price column

    row = row + 1
    
    # close workbook
    workbook.close()
    xlsx_data = output.getvalue()
    return xlsx_data


def compute_rows(text, width):
    if len(text) < width:
        return 1
    phrases = text.replace('\r', '').split('\n')

    rows = 0
    for phrase in phrases:
        if len(phrase) < width:
            rows = rows + 1
        else:
            words = phrase.split(' ')
            temp = ''
            for idx, word in enumerate(words):
                temp = temp + word + ' '
                # check if column width exceeded
                if len(temp) > width:
                    rows = rows + 1
                    temp = '' + word + ' '
                # check if it is not the last word
                if idx == len(words) - 1 and len(temp) > 0:
                    rows = rows + 1
    return rows
