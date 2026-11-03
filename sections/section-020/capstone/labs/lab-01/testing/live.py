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

workflow=obj('workflow','data-flow')
assert workflow['status']['phase']=='Succeeded', 'Workflow has not completed successfully'
nodes=list(workflow['status']['nodes'].values())
assert any(p.get('name')=='result' and p.get('value')=='PROBE DATA' for n in nodes for p in n.get('outputs',{}).get('parameters',[])), 'The transformed text must reach the final parameter'
final=[a for n in nodes for a in n.get('outputs',{}).get('artifacts',[]) if a.get('name')=='final']
assert final and final[0].get('s3',{}).get('key')=='data-flow/final.txt', 'The final artifact must use the key data-flow/final.txt'
transform=next(t for t in workflow['spec']['templates'] if t['name']=='transform')
out=transform['outputs']['artifacts'][0]
assert 'none' in out.get('archive',{}), 'The final artifact must use archive none'
assert out.get('artifactGC',{}).get('strategy')=='Never', 'The final artifact must be kept with strategy Never'
