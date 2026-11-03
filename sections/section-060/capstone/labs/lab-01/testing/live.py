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

workflow=obj('workflow','batch-run')
assert workflow['status']['phase']=='Succeeded', 'Workflow has not completed successfully'
nodes=list(workflow['status']['nodes'].values())
parts=[n for n in nodes if n.get('templateName')=='produce' and n.get('type')=='Pod']
assert len(parts)==3 and all(n['phase']=='Succeeded' for n in parts), 'Three parts must be processed'
assert {json.loads(n['outputs']['result'])['part'] for n in parts}=={'ALPHA','BETA','GAMMA'}, 'Each part must print its upper case name as JSON'
combine=next(n for n in nodes if n.get('templateName')=='combine' and n.get('type')=='Pod')
assert combine['phase']=='Succeeded' and combine['outputs']['result'].strip()=='parts: 3', 'The join must receive three parts'
assert all(n['finishedAt']<=combine['startedAt'] for n in parts), 'The join must wait for every part'
retry=next(t for t in workflow['spec']['templates'] if t['name']=='produce')['retryStrategy']
assert str(retry['limit'])=='1', 'The produce template needs one retry'
