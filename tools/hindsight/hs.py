#!/usr/bin/env python3
"""Hindsight Cloud REST helper for a Commander's Intent fleet (standard library only).
Bank from $HINDSIGHT_BANK (or --bank). Key from $HINDSIGHT_API_KEY. Never echoes the key.
Source: https://github.com/shagghiesuperstar/commanders-intent (MIT).
Usage:
  hs.py recall "query" [--tags canon] [--max 2048]
  hs.py reflect "question" [--tags canon]
  hs.py retain "fact" --context "why/where" [--tags a,b] [--doc ID] [--by AGENT]
  hs.py mm list | hs.py mm get <id>
  hs.py kb tree | hs.py kb search "query" | hs.py kb page <id>
  hs.py op <operation_id>
"""
import os,sys,json,argparse,urllib.request,urllib.error,urllib.parse,datetime
API="https://api.hindsight.vectorize.io/v1/default/banks/"
def call(method,path,body=None,bank=None):
    k=os.environ.get("HINDSIGHT_API_KEY")
    if not k: sys.exit("BLOCKED: HINDSIGHT_API_KEY not set")
    if not bank: sys.exit("BLOCKED: HINDSIGHT_BANK not set (export HINDSIGHT_BANK=<MEMORY_BANK_ID> or pass --bank)")
    req=urllib.request.Request(API+bank+path,method=method,data=json.dumps(body).encode() if body is not None else None,
        headers={"Authorization":"Bearer "+k,"Content-Type":"application/json"})
    try:
        with urllib.request.urlopen(req,timeout=180) as r: return json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e: sys.exit(f"BLOCKED: HTTP {e.code} {e.read().decode()[:600]}")
p=argparse.ArgumentParser(); p.add_argument("cmd"); p.add_argument("args",nargs="*")
p.add_argument("--tags"); p.add_argument("--max",type=int,default=2048); p.add_argument("--context")
p.add_argument("--doc"); p.add_argument("--by",default=os.environ.get("AGENT_NAME","grok-bot")); p.add_argument("--bank",default=os.environ.get("HINDSIGHT_BANK"))
a=p.parse_args(); tags=a.tags.split(",") if a.tags else None; B=a.bank
if a.cmd=="recall":
    body={"query":a.args[0],"max_tokens":a.max}
    if tags: body.update(tags=tags,tags_match="any")
    r=call("POST","/memories/recall",body,B)
    for m in r.get("results",[]): print(f"- [{m.get('type')}] {m.get('text')}  (id {m.get('id')}, {m.get('mentioned_at','')[:10]})")
elif a.cmd=="reflect":
    body={"query":a.args[0],"include":{"facts":{}}}
    if tags: body.update(tags=tags,tags_match="any")
    r=call("POST","/reflect",body,B); print(r.get("text") or json.dumps(r)[:4000])
elif a.cmd=="retain":
    if not a.context: sys.exit("BLOCKED: --context is required (say where this came from and why it matters)")
    ts=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    it={"content":a.args[0],"context":a.context,"timestamp":ts,"metadata":{"written_by":a.by,"written_at":ts},"tags":tags or []}
    if a.doc: it["document_id"]=a.doc
    print(json.dumps(call("POST","/memories",{"items":[it],"async":True},B)))
elif a.cmd=="mm":
    if a.args[0]=="list":
        for m in call("GET","/mental-models",None,B).get("items",[]): print(f"- {m['id']}: {m.get('name')} (refreshed {m.get('last_refreshed_at','')[:16]})")
    else: print(call("GET","/mental-models/"+a.args[1],None,B).get("content"))
elif a.cmd=="kb":
    if a.args[0]=="tree": print(json.dumps(call("GET","/knowledge-base/tree",None,B),indent=1)[:6000])
    elif a.args[0]=="search": print(json.dumps(call("GET","/knowledge-base/search?"+urllib.parse.urlencode({"query":a.args[1]}),None,B),indent=1)[:6000])
    else: print(json.dumps(call("GET","/knowledge-base/pages/"+a.args[1],None,B),indent=1)[:8000])
elif a.cmd=="op": print(json.dumps(call("GET","/operations/"+a.args[0],None,B),indent=1))
else: print(__doc__)
