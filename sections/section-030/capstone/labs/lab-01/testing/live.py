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

template=obj('workflowtemplate','crew-library')
assert template['spec']['arguments']['parameters'][0]['value']=='apollo', 'The template must keep its default crew value'
assert any('container' in t for t in template['spec']['templates']), 'The template must hold a container template'
workflow=obj('workflow','launch-crew')
assert workflow['status']['phase']=='Succeeded', 'Workflow has not completed successfully'
ref=workflow['spec']['templates'][0]['steps'][0][0].get('templateRef',{})
assert ref.get('name')=='crew-library' and ref.get('template')=='announce', 'The step must call the announce template with templateRef'
nodes=list(workflow['status']['nodes'].values())
assert any(p.get('name')=='result' and p.get('value')=='orion' for n in nodes for p in n.get('outputs',{}).get('parameters',[])), 'The overridden crew value must reach the output parameter'
