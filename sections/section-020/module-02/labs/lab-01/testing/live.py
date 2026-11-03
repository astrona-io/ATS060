import json,subprocess,time,sys,tempfile,os

def call(*args):
 r=subprocess.run(list(args),text=True,capture_output=True,timeout=20)
 assert r.returncode==0, 'Observation command failed: '+args[0]
 return r.stdout.strip()
def obj(kind,name,ns='starfleet'):
 return json.loads(call('kubectl',*(['-n',ns] if ns else []),'get',kind,name,'-o','json'))
def api(path):
 script='import urllib.request; print(urllib.request.urlopen('+repr('http://prometheus:9090'+path)+',timeout=8).read().decode())'
 return json.loads(call('kubectl','-n','starfleet','exec','shuttle','--','python','-c',script))
def save(data):
 resource={'apiVersion':'v1','kind':'ConfigMap','metadata':{'name':'evidence','namespace':'starfleet'},'data':{'report.json':json.dumps(data,sort_keys=True)}}
 with tempfile.NamedTemporaryFile(mode='w',suffix='.json',delete=False) as f:json.dump(resource,f);path=f.name
 try:call('kubectl','apply','-f',path)
 finally:os.unlink(path)

workflow=obj('workflow','staging')
assert workflow['status']['phase']=='Succeeded', 'Workflow has not completed successfully'
nodes=list(workflow['status']['nodes'].values())
assert any(p.get('name')=='result' and p.get('value')=='crew-roster' for n in nodes for p in n.get('outputs',{}).get('parameters',[])), 'The raw input must reach the final output parameter'
staged=[a for n in nodes for a in n.get('outputs',{}).get('artifacts',[]) if a.get('name')=='staged']
assert staged and staged[0].get('s3',{}).get('key')=='staging/staged.txt', 'The staged artifact must use the key staging/staged.txt'
stage=next(t for t in workflow['spec']['templates'] if t['name']=='stage')
assert 'none' in stage['outputs']['artifacts'][0].get('archive',{}), 'The staged artifact must use archive none'
assert stage['inputs']['artifacts'][0].get('raw',{}).get('data')=='crew-roster', 'The note must be a raw input with the roster text'
