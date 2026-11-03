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

workflow=obj('workflow','route-plan')
assert workflow['status']['phase']=='Succeeded', 'Workflow has not completed successfully'
nodes=list(workflow['status']['nodes'].values())
by={n.get('displayName'):n for n in nodes}
assert by['proceed']['phase']=='Succeeded' and by['hold']['phase']=='Skipped', 'Exactly the proceed branch must run'
loop=[n for n in nodes if n.get('displayName','').startswith('survey(') and n.get('type')=='Pod']
assert len(loop)==3 and all(n['phase']=='Succeeded' for n in loop), 'The survey task must run three times'
report=by['report']
assert report['phase']=='Succeeded', 'The report task must succeed'
assert all(n['finishedAt']<=report['startedAt'] for n in loop), 'The report task must wait for the whole loop'
tasks={t['name']:t for t in workflow['spec']['templates'][0]['dag']['tasks']}
assert len(tasks['survey'].get('withItems',[]))==3, 'The survey task must loop over three items'
