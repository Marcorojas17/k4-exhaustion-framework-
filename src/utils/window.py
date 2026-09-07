def evaluate_crib_window(plaintext: str, cribs=None):
    best_score=0; found_crib="NONE"; found_pos=-1
    if cribs is None: cribs=["BERLIN","CLOCK","PALIMPSEST"]
    for crib in cribs:
        cu=crib.upper(); cl=len(cu)
        if len(plaintext)<cl: continue
        for pos in range(len(plaintext)-cl+1):
            wt=plaintext[pos:pos+cl].upper()
            m=sum(1 for a,b in zip(wt,cu) if a==b)
            if m>best_score: best_score=m; found_crib=cu; found_pos=pos
    return (best_score,found_crib,found_pos) if best_score>=4 else (0,"NONE",-1)

def check_berlin_clock_window(plaintext, crib="BERLINCLOCK", start=63, end=74, *a, **k):
    cs=str(crib).upper(); s=int(start); e=int(end)
    if len(plaintext)>=e:
        w=plaintext[s:e].upper()
        if cs in w: return True
        if sum(1 for x,y in zip(w,cs) if x==y)>=8: return True
    return cs in plaintext.upper()
