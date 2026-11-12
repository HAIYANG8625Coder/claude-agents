import json, subprocess, sys, os
proj = sys.argv[1]
ff = os.path.join(proj, "../../node_modules/@ffmpeg-installer/darwin-arm64/ffmpeg")
fp = os.path.join(proj, "../../node_modules/@ffprobe-installer/darwin-arm64/ffprobe")
lines = json.load(open(os.path.join(proj, "script.json")))
tmp = os.path.join(proj, ".voice"); os.makedirs(tmp, exist_ok=True)
GAP = 0.22
t = 0.15; parts = []; out = []
sil = lambda d, n: subprocess.run([ff,"-v","error","-y","-f","lavfi","-i","anullsrc=r=44100:cl=mono","-t",str(d),n],check=True)
lead = os.path.join(tmp,"lead.wav"); sil(0.15, lead); parts.append(lead)
for i, l in enumerate(lines):
    aiff = os.path.join(tmp, "s%02d.aiff" % i); wav = os.path.join(tmp, "s%02d.wav" % i)
    subprocess.run(["say","-v","Tingting","-r",str(l.get("rate",215)),"-o",aiff,l["say"]],check=True)
    subprocess.run([ff,"-v","error","-y","-i",aiff,"-ar","44100","-ac","1",wav],check=True)
    d = float(subprocess.run([fp,"-v","error","-show_entries","format=duration","-of","csv=p=0",wav],capture_output=True,text=True).stdout)
    out.append({"i":i,"start":round(t,3),"end":round(t+d,3),"text":l["say"]})
    parts.append(wav); t += d
    pause = l.get("pause", GAP); g = os.path.join(tmp,"g%02d.wav"%i); sil(pause, g); parts.append(g); t += pause
lst = os.path.join(tmp,"list.txt"); open(lst,"w").write("".join("file '%s'\n" % p for p in parts))
os.makedirs(os.path.join(proj,"assets"),exist_ok=True)
subprocess.run([ff,"-v","error","-y","-f","concat","-safe","0","-i",lst,"-c:a","pcm_s16le",os.path.join(proj,"assets/vo.wav")],check=True)
json.dump({"total":round(t,3),"lines":out}, open(os.path.join(proj,"timing.json"),"w"), ensure_ascii=False, indent=1)
print("total %.2fs" % t)
for o in out: print("%5.2f-%5.2f %s" % (o["start"], o["end"], o["text"]))
