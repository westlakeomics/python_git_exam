# NOTE: This file is intentionally written with poor style for the exam.
# Your task: refactor to be PEP 8-friendly while keeping behavior unchanged.

import math,os,sys


def calc(Arr,mode="mean",round_to=2, allow_negative=False):
    """
    do calculation for mean/median/std of list.
    mode can be: mean,median,std.  round_to means rounding digits.
    allow_negative False means raise if negative number in Arr
    """
    if Arr==None or len(Arr)==0: return None
    for x in Arr:
        if (not allow_negative) and x<0:
            raise Exception("negative not allowed: "+str(x))

    if mode=="mean":
        s=0
        for x in Arr: s+=x
        v=s/len(Arr)
    elif mode=="median":
        B=sorted(Arr)
        n=len(B)
        mid=n//2
        if n%2==1: v=B[mid]
        else: v=(B[mid-1]+B[mid])/2
    elif mode=="std":
        m=calc(Arr,"mean",round_to,allow_negative)
        s=0
        for x in Arr:
            s+=(x-m)**2
        v=math.sqrt(s/len(Arr))
    else:
        raise ValueError("Unknown mode:"+mode)

    return round(v,round_to)


def parse_numbers(text):
    # expects "1,2,3" or "1 2 3" but does it badly
    if text is None: return []
    t=text.replace(","," ").replace("\t"," ")
    parts=t.split(" ")
    out=[]
    for p in parts:
        if p.strip()=="":
            continue
        out.append(float(p))
    return out


def read_file(path):
    # reads first line
    f=open(path,"r")
    line=f.readline()
    f.close()
    return line


def main(argv=None):
    if argv is None: argv=sys.argv
    if len(argv)<3:
        print("Usage: python -m src.bad_style <mode> <numbers_or_file_path> [--file]")
        return 2

    mode=argv[1]
    value=argv[2]
    is_file=False
    if len(argv)>3 and argv[3]=="--file":
        is_file=True

    if is_file:
        if not os.path.exists(value):
            print("file not found:"+value)
            return 2
        value=read_file(value)

    nums=parse_numbers(value)
    r=calc(nums,mode=mode)
    print(r)
    return 0


if __name__=="__main__":
    raise SystemExit(main())