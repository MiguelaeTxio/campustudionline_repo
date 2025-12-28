import json, requests, re, io, time, pdfplumber

def extract_sections_uco(text):
    sections = {"objectives": [], "outline": [], "bibliography": {"fundamental": []}}
    prog = re.search(r'1\. Contenidos teóricos(.*?)2\. Contenidos prácticos|Bibliografía', text, re.S | re.I)
    if prog:
        items = re.findall(r'(?:BLOQUE|Tema|LECCIÓN)\s?\d+[:\.]?\s*(.*?)(?=BLOQUE|Tema|LECCIÓN|$)', prog.group(1), re.S | re.I)
        sections["outline"] = [re.sub(r'\s+', ' ', i).strip() for i in items if len(i) > 5]
    comp = re.findall(r'\b([A-Z]+\d{2,})\s+(.*?)(?=[A-Z]+\d{2,}|$)', text, re.S)
    if comp:
        sections["objectives"] = [f"{c[0]}: {re.sub(r'\s+', ' ', c[1]).strip()}" for c in comp]
    bib = re.search(r'Bibliografía(.*?)Metodología', text, re.S | re.I)
    if bib:
        sections["bibliography"]["fundamental"] = [re.sub(r'\s+', ' ', l).strip() for l in bib.group(1).split('\n') if len(l) > 15]
    return sections

def process():
    with open("uco_master_map.json", 'r', encoding='utf-8') as f:
        subjects = json.load(f).get('subjects', [])
    processed = []
    session = requests.Session()
    for idx, sub in enumerate(subjects):
        try:
            r = session.get(sub['pdf'], timeout=12)
            if r.status_code == 200 and b'%PDF' in r.content[:10]:
                with pdfplumber.open(io.BytesIO(r.content)) as pdf:
                    full_text = "\n".join([p.extract_text() or "" for p in pdf.pages])
                if full_text.strip():
                    struct = extract_sections_uco(full_text)
                    sub.update({"learning_objectives": struct["objectives"], "course_content_outline": struct["outline"], "bibliography": struct["bibliography"]})
                    processed.append(sub)
        except: pass
        time.sleep(0.3)
    with open("uco_data_final.json", 'w', encoding='utf-8') as f:
        json.dump(processed, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    process()
