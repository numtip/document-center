#!/usr/bin/env python3
"""RAE Document Registry upsert — DocumentID idempotency key."""
import json
import re

SITE_HOST = 'https://maejo365.sharepoint.com'
OWNER_ID = 9  # pilot placeholder — not authoritative Category Owner

LIB_CATEGORY = {
    'Administration': 'admin',
    'FinanceProcurement': 'finance-procurement',
    'Research': 'research',
    'AcademicServices': 'academic-service',
    'PlanningPolicy': 'policy-planning',
    'SOPManuals': 'manuals',
}

LIBS = list(LIB_CATEGORY.keys())


def storage_url(file_ref):
    if not file_ref:
        return ''
    if file_ref.startswith('http'):
        return file_ref
    return SITE_HOST + file_ref if file_ref.startswith('/') else f'{SITE_HOST}/{file_ref}'


def build_record_from_lib_item(lib, item):
    doc_id = (item.get('DocumentID') or '').strip()
    if not doc_id:
        return None
    title = (item.get('Title') or doc_id).strip()
    cat = (item.get('Category1') or LIB_CATEGORY.get(lib, '')).strip() or LIB_CATEGORY[lib]
    file_ref = item.get('FileRef') or ''
    legacy = (item.get('LegacySourceURL') or '')
    if isinstance(legacy, dict):
        legacy = legacy.get('Url', '') or ''
    return {
        'document_id': doc_id,
        'title': title,
        'category': cat,
        'status': 'draft',
        'visibility': 'internal',
        'source_system': 'WTMS Migration',
        'storage_url': storage_url(file_ref),
        'legacy_url': legacy,
        'library': lib,
        'updated': item.get('Modified') or '',
    }


def build_upsert_js(record):
    """Upsert one Registry record by DocumentID."""
    rec = json.dumps(record, ensure_ascii=True)
    return f"""(async function(){{
var rec={rec};
var ctx=_spPageContextInfo,d=ctx.formDigestValue,s=ctx.webServerRelativeUrl;
var doc=rec.document_id;
try{{
var q="Document_x0020_ID eq '"+doc.replace(/'/g,"''")+"'";
var fr=await fetch(s+"/_api/web/lists/getbytitle('RAE%20Document%20Registry')/items?$select=Id,Title&$filter="+encodeURIComponent(q),{{
headers:{{'accept':'application/json;odata=verbose'}}}});
if(!fr.ok) throw new Error('FIND_HTTP_'+fr.status);
var fj=await fr.json(),existing=(fj.d.results||[])[0];
var storageFv=rec.storage_url+', '+doc;
var fields=[
{{FieldName:'Title',FieldValue:rec.title}},
{{FieldName:'Document_x0020_ID',FieldValue:doc}},
{{FieldName:'Category',FieldValue:rec.category}},
{{FieldName:'Status',FieldValue:rec.status}},
{{FieldName:'Visibility',FieldValue:rec.visibility}},
{{FieldName:'Source_x0020_System',FieldValue:rec.source_system}},
{{FieldName:'Storage_x0020_URL',FieldValue:storageFv}}
];
if(rec.legacy_url) fields.push({{FieldName:'Legacy_x0020_Source_x0020_URL',FieldValue:rec.legacy_url}});
if(existing){{
var ur=await fetch(s+'/_api/web/lists/getbytitle(%27RAE%20Document%20Registry%27)/items('+existing.Id+')/ValidateUpdateListItem',{{method:'POST',headers:{{'X-RequestDigest':d,'accept':'application/json;odata=verbose','content-type':'application/json;odata=verbose'}},body:JSON.stringify({{formValues:fields,bNewDocumentUpdate:false}})}});
if(!ur.ok) throw new Error((await ur.text()).substring(0,200));
var uj=await ur.json(),errs=(uj.d.ValidateUpdateListItem.results||[]).filter(r=>r.HasException);
if(errs.length) return {{action:'FAILED',doc:doc,id:existing.Id,error:JSON.stringify(errs).substring(0,200)}};
return {{action:'UPDATED',doc:doc,id:existing.Id}};
}}
var body={{__metadata:{{type:'SP.Data.RAE_x0020_Document_x0020_RegistryListItem'}},Title:rec.title,Document_x0020_ID:doc,Category:rec.category,OwnerId:{OWNER_ID},Status:rec.status,Visibility:rec.visibility,Updated_x0020_Date:new Date().toISOString(),Source_x0020_System:rec.source_system,Storage_x0020_URL:{{Url:rec.storage_url,Description:doc}}}};
var cr=await fetch(s+'/_api/web/lists/getbytitle(%27RAE%20Document%20Registry%27)/items',{{method:'POST',headers:{{'X-RequestDigest':d,'accept':'application/json;odata=verbose','content-type':'application/json;odata=verbose'}},body:JSON.stringify(body)}});
if(!cr.ok) throw new Error((await cr.text()).substring(0,200));
var cj=await cr.json(),nid=cj.d.ID;
if(rec.legacy_url){{
await fetch(s+'/_api/web/lists/getbytitle(%27RAE%20Document%20Registry%27)/items('+nid+')/ValidateUpdateListItem',{{method:'POST',headers:{{'X-RequestDigest':d,'accept':'application/json;odata=verbose','content-type':'application/json;odata=verbose'}},body:JSON.stringify({{formValues:[{{FieldName:'Legacy_x0020_Source_x0020_URL',FieldValue:rec.legacy_url}}],bNewDocumentUpdate:false}})}});
}}
return {{action:'CREATED',doc:doc,id:nid}};
}}catch(e){{return {{action:'FAILED',doc:doc,error:e.message}}}}
}})()"""


def build_scan_libs_js():
    libs_json = json.dumps(LIBS)
    return f"""(async function(){{
var ctx=_spPageContextInfo,s=ctx.webServerRelativeUrl;
var libs={libs_json},out=[];
for(var i=0;i<libs.length;i++){{
var lib=libs[i];
var skip=0,top=500,more=true;
while(more){{
var r=await fetch(s+"/_api/web/lists/getbytitle('"+lib+"')/items?$select=Id,Title,DocumentID,Category1,LegacySourceURL,FileRef,Modified&$top="+top+"&$skip="+skip,{{
headers:{{'accept':'application/json;odata=verbose'}}}});
if(!r.ok){{out.push({{lib:lib,error:'HTTP_'+r.status}});break;}}
var j=await r.json(),rows=j.d.results||[];
for(var k=0;k<rows.length;k++){{
var it=rows[k];
if(!it.DocumentID) continue;
var leg=it.LegacySourceURL;
out.push({{
lib:lib,id:it.ID,document_id:it.DocumentID,title:it.Title||it.DocumentID,
category1:it.Category1||'',file_ref:it.FileRef||'',modified:it.Modified||'',
legacy_url:(leg&&leg.Url)?leg.Url:(typeof leg==='string'?leg:'')
}});
}}
more=rows.length===top; skip+=top;
}}
}}
return out;
}})()"""


def build_delete_registry_js(doc_id):
    doc_esc = doc_id.replace("'", "''")
    return f"""(async function(){{
var ctx=_spPageContextInfo,d=ctx.formDigestValue,s=ctx.webServerRelativeUrl;
var q="Document_x0020_ID eq '{doc_esc}'";
var fr=await fetch(s+"/_api/web/lists/getbytitle('RAE%20Document%20Registry')/items?$select=Id&$filter="+encodeURIComponent(q),{{
headers:{{'accept':'application/json;odata=verbose'}}}});
var fj=await fr.json(),rows=fj.d.results||[];
if(rows.length!==1) return {{error:'COUNT_'+rows.length}};
var id=rows[0].Id;
var dr=await fetch(s+'/_api/web/lists/getbytitle(%27RAE%20Document%20Registry%27)/items('+id+')',{{method:'POST',headers:{{'X-RequestDigest':d,'IF-MATCH':'*','X-HTTP-Method':'DELETE','accept':'application/json;odata=verbose'}}}});
return {{deleted:id,status:dr.status}};
}})()"""


def build_count_duplicates_js():
    return """(async function(){
var s=_spPageContextInfo.webServerRelativeUrl;
var r=await fetch(s+"/_api/web/lists/getbytitle('RAE%20Document%20Registry')/items?$select=Document_x0020_ID&$top=500",{
headers:{'accept':'application/json;odata=verbose'}});
var j=await r.json(),counts={},dups=[];
(j.d.results||[]).forEach(x=>{
var d=x.Document_x0020_ID||'';
counts[d]=(counts[d]||0)+1;
if(counts[d]===2)dups.push(d);
});
return {total:j.d.results.length,duplicates:dups};
})()"""


def parse_action(result):
    if not isinstance(result, dict):
        return 'FAILED', str(result)[:100]
    return result.get('action', 'FAILED'), result
