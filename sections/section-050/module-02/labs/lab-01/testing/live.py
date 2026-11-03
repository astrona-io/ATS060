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

workflow=obj('workflow','gate')
assert workflow['status']['phase']=='Succeeded', 'Workflow has not completed successfully'
nodes={n.get('displayName'):n for n in workflow['status']['nodes'].values()}
assert nodes['launch']['phase']=='Succeeded', 'The launch branch must run when the check prints green'
assert nodes['abort']['phase']=='Skipped', 'The abort branch must be skipped by its when condition'
assert nodes['report']['phase']=='Succeeded', 'The report task must run after either branch'
tasks={t['name']:t for t in workflow['spec']['templates'][0]['dag']['tasks']}
assert tasks['launch'].get('when') and tasks['abort'].get('when'), 'Both branches need a when condition'
assert 'depends' in tasks['report'] and 'dependencies' not in tasks['report'], 'The report task must use a depends expression'
