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

workflow=obj('workflow','compose')
assert workflow['status']['phase']=='Succeeded', 'Workflow has not completed successfully'
nodes=list(workflow['status']['nodes'].values())
assert any(p.get('name')=='result' and p.get('value')=='BRIDGE' for n in nodes for p in n.get('outputs',{}).get('parameters',[])), 'The upper case script text must reach the output parameter'
templates={t['name']:t for t in workflow['spec']['templates']}
assert 'script' in templates['shout'], 'The shout template must be a script template'
assert 'steps' in templates['pipeline'], 'The pipeline template must be a steps template'
shout=next(n for n in nodes if n.get('displayName')=='shout')
assert shout.get('outputs',{}).get('result','').strip()=='BRIDGE', 'The script node must expose its standard output as result'
