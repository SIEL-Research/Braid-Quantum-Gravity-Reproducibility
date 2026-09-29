#!/usr/bin/env python3
from hashlib import sha256
import json
from pathlib import Path
H=Path(__file__).resolve().parent
d=lambda n: sha256((H/n).read_bytes()).hexdigest()
raw=json.loads((H/'RAW_OUTPUT.json').read_text()); result=json.loads((H/'RESULT.json').read_text()); status=json.loads((H/'STATUS.json').read_text()); freeze=json.loads((H/'SCOUT_FREEZE.json').read_text())
for n,e in freeze['artifacts'].items():
    if n!='ITERATION_LEDGER.md': assert d(n)==e
assert 'PASS_SCOPED' in (H/'ITERATION_LEDGER.md').read_text()
assert d('RAW_OUTPUT.json')==status['raw_output_sha256'] and d('RESULT.json')==status['result_sha256'] and d('REPORT.md')==status['report_sha256']
assert raw['all_sectors_connected_within_each_grading'] is True
assert raw['grading_complex_dimensions']=={'-1':18,'1':18}
assert raw['global_generated_dagger_algebra_complex_dimension']==648
assert raw['within_sector_commutant_complex_dimensions']==[1,1]
assert len(raw['sector_records'])==8 and all(x['component_count']==2 and x['component_complex_dimensions']==[18,18] and x['cross_grading_edges']==0 for x in raw['sector_records'])
assert result['decision']==status['decision']=='CLOSED_SCOPED'
print(json.dumps({'status':'PASS','scout_id':raw['scout_id'],'algebra':'M18(C)+M18(C)'},indent=2,sort_keys=True))
