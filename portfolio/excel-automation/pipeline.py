"""Validate a sales CSV and export a three-sheet Excel workbook."""
import argparse,csv,datetime,logging
from collections import defaultdict
from pathlib import Path
from openpyxl import Workbook
from openpyxl.chart import BarChart,Reference
BASE=Path(__file__).parent
def run(input_path,output_path):
    output_path.parent.mkdir(parents=True,exist_ok=True)
    logging.basicConfig(filename=output_path.parent/'pipeline.log',level=logging.INFO,force=True)
    valid=[];errors=[];seen=set()
    with input_path.open(newline='',encoding='utf-8-sig') as f:
        reader=csv.DictReader(f)
        missing={'order_id','date','region','revenue'}-set(reader.fieldnames or [])
        if missing: raise ValueError('Missing columns: '+str(missing))
        for n,r in enumerate(reader,2):
            try:
                oid=r['order_id'].strip();region=r['region'].strip()
                if not oid or not region: raise ValueError('Empty key')
                if oid in seen: raise ValueError('Duplicate order ID')
                datetime.date.fromisoformat(r['date'])
                amount=float(r['revenue'])
                if amount<0: raise ValueError('Negative revenue')
                seen.add(oid);valid.append([oid,r['date'],region,amount])
            except (ValueError,TypeError,KeyError) as exc:
                logging.warning('Row %s: %s',n,exc);errors.append([n,str(exc),str(r)])
    wb=Workbook();ws=wb.active;ws.title='Clean Data';ws.append(['order_id','date','region','revenue'])
    for r in valid:ws.append(r)
    summary=wb.create_sheet('Summary');summary.append(['region','revenue'])
    totals=defaultdict(float)
    for r in valid:totals[r[2]]+=r[3]
    for k,v in sorted(totals.items()):summary.append([k,v])
    if totals:
        chart=BarChart();chart.title='Revenue by region'
        chart.add_data(Reference(summary,min_col=2,min_row=1,max_row=summary.max_row),titles_from_data=True)
        chart.set_categories(Reference(summary,min_col=1,min_row=2,max_row=summary.max_row))
        summary.add_chart(chart,'D2')
    errors_sheet=wb.create_sheet('Validation Errors');errors_sheet.append(['csv_row','error','raw_record'])
    for r in errors:errors_sheet.append(r)
    wb.save(output_path);logging.info('valid=%s invalid=%s',len(valid),len(errors))
    print('Valid:',len(valid),'Invalid:',len(errors))
    return len(valid),len(errors)
if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--input',type=Path,default=BASE/'data'/'sales.csv')
    p.add_argument('--output',type=Path,default=BASE/'output'/'sales_report.xlsx')
    a=p.parse_args();run(a.input,a.output)
