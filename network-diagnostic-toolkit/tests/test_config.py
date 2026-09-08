from pathlib import Path
from netdiag.config import deep_merge, load_config

def test_deep_merge_nested():
    out=deep_merge({'a':{'b':1,'c':2}},{'a':{'b':9}}); assert out=={'a':{'b':9,'c':2}}
def test_default_config_has_targets():
    cfg=load_config(); assert cfg['targets']['internet_ip']=='1.1.1.1'; assert cfg['execution']['ping_count']>=1
def test_load_override(tmp_path:Path):
    p=tmp_path/'c.yaml'; p.write_text('execution:\n  ping_count: 3\n',encoding='utf-8'); cfg=load_config(p); assert cfg['execution']['ping_count']==3 and cfg['targets']['internet_ip']=='1.1.1.1'
