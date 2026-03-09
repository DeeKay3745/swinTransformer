"""
Dysarthric Speech Audio Trimmer v7
==================================

Features
--------
• Whisper transcription
• Word timestamps
• Character / Word / Sentence / Paragraph detection
• Confidence score per segment
• Custom file names
• Excel report with MM:SS.mmm timestamps
• Audio trimming

Install
-------
pip install openai-whisper pydub openpyxl
"""

import argparse
import os
import re
import whisper


# =====================================================
# CONTENT
# =====================================================

ALPHABETS=list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

WORDS=[
"Time","Has","Look","People","Number","Water","Now","Find",
"Giggled","Hypothesis","Supervision","Download","Paragraph",
"Shift","Control","November","Bravo","Oscar","Alpha",
"Mike","India","Charlie","Uniform","Backspace","Escape","Upward",
"One","Three","Four","Five","Seven","Twelve","Fifteen","Twenty nine",
"Their","If","Beta","Delta","Could","Adapt","Circular","Composure",
"Footwork","Journalism","Python","Advice","Choice","Employment",
"Immovable","Massage","Moisten","Tree","Knife","Spoon","Banana","Monkey"
]

SENTENCES=[
("S1","Each untimely income loss coincided with the breakdown of a heating system part."),
("S2","Alice's ability to work without supervision is noteworthy."),
("S3","Special task forces rescue hostages from kidnappers."),
("S4","Laugh, dance, and sing if fortune smiles upon you."),
("S5","The same shelter could be built into an embankment or below ground level.")
]

PARAGRAPH="""
When the sunlight strikes raindrops in the air they act as a prism and form a rainbow
The rainbow is a division of white light into many beautiful colors
These take the shape of a long round arch with its path high above
"""


# =====================================================
# HELPERS
# =====================================================

def norm(s):
    return re.sub(r"[^a-z]","",s.lower())


def norm_words(text):
    return [norm(w) for w in text.split() if norm(w)]


def fuzzy_match(a,b):

    if a==b:
        return 1.0

    if a[:4]==b[:4]:
        return 0.8

    if a in b or b in a:
        return 0.6

    if a[:3]==b[:3]:
        return 0.5

    return 0


def format_time(seconds):

    if seconds is None:
        return ""

    minutes=int(seconds//60)
    sec=seconds%60

    return f"{minutes:02d}:{sec:06.3f}"


# =====================================================
# TRANSCRIPTION
# =====================================================

def transcribe(audio_path,model_size="medium"):

    print("Loading Whisper model:",model_size)

    model=whisper.load_model(model_size)

    result=model.transcribe(
        audio_path,
        language="en",
        word_timestamps=True
    )

    words=[]

    for seg in result["segments"]:

        for w in seg["words"]:

            token=norm(w["word"])

            if token:

                words.append({
                    "word":token,
                    "start":w["start"],
                    "end":w["end"]
                })

    print("Detected words:",len(words))

    return words


# =====================================================
# MATCH SINGLE
# =====================================================

def match_single(expected,detected,used):

    best_idx=None
    best_score=0

    for i,w in enumerate(detected):

        if i in used:
            continue

        score=fuzzy_match(expected,w["word"])

        if score>best_score:

            best_score=score
            best_idx=i

    if best_idx is not None and best_score>=0.4:

        w=detected[best_idx]

        return best_idx,w["start"],w["end"],best_score

    return None


# =====================================================
# MATCH SENTENCE
# =====================================================

def match_sentence(sentence,detected,used):

    expected=norm_words(sentence)

    matched=[]
    idxs=[]

    for ew in expected:

        for i,w in enumerate(detected):

            if i in used:
                continue

            if fuzzy_match(ew,w["word"])>=0.5:

                matched.append(w)
                idxs.append(i)

                break

    if not matched:
        return None

    start=min(w["start"] for w in matched)
    end=max(w["end"] for w in matched)

    confidence=len(matched)/len(expected)

    return start,end,idxs,confidence


# =====================================================
# SEGMENT OBJECT
# =====================================================

def make_seg(id,type_,content,start,end,conf,note):

    return {
        "id":id,
        "type":type_,
        "content":content,
        "start":start,
        "end":end,
        "confidence":conf,
        "note":note,
        "file":"-"
    }


# =====================================================
# BUILD SEGMENTS
# =====================================================

def build_segments(words):

    used=set()
    segments=[]
    sid=1

    print("Matching segments...")

    # CHARACTERS
    for ch in ALPHABETS:

        r=match_single(norm(ch),words,used)

        if r:

            idx,s,e,conf=r
            used.add(idx)

            segments.append(make_seg(sid,"Alphabet",ch,s,e,conf,""))

        else:

            segments.append(make_seg(sid,"Alphabet",ch,None,None,0,"Not detected"))

        sid+=1


    # WORDS
    for word in WORDS:

        r=match_single(norm(word),words,used)

        if r:

            idx,s,e,conf=r
            used.add(idx)

            segments.append(make_seg(sid,"Word",word,s,e,conf,""))

        else:

            segments.append(make_seg(sid,"Word",word,None,None,0,"Not detected"))

        sid+=1


    # SENTENCES
    for label,text in SENTENCES:

        r=match_sentence(text,words,used)

        if r:

            s,e,idxs,conf=r

            for i in idxs:
                used.add(i)

            segments.append(make_seg(sid,"Sentence "+label,text,s,e,conf,""))

        else:

            segments.append(make_seg(sid,"Sentence "+label,text,None,None,0,"Not detected"))

        sid+=1


    # PARAGRAPH
    r=match_sentence(PARAGRAPH,words,used)

    if r:

        s,e,idxs,conf=r

        segments.append(make_seg(sid,"Paragraph",PARAGRAPH[:80],s,e,conf,""))

    else:

        segments.append(make_seg(sid,"Paragraph",PARAGRAPH[:80],None,None,0,"Not detected"))

    return segments


# =====================================================
# TRIM AUDIO WITH CUSTOM FILENAMES
# =====================================================

def trim_audio(audio_path,segments,outdir):

    from pydub import AudioSegment

    audio=AudioSegment.from_wav(audio_path)

    os.makedirs(outdir,exist_ok=True)

    for seg in segments:

        if seg["start"] is None:
            continue

        s=int(seg["start"]*1000)
        e=int(seg["end"]*1000)

        clip=audio[s:e]

        if seg["type"]=="Alphabet":

            fname=f"Char_{seg['content'].upper()}.wav"

        elif seg["type"]=="Word":

            word=seg["content"].upper().replace(" ","_")
            fname=f"Word_{word}.wav"

        elif seg["type"].startswith("Sentence"):

            sid=seg["type"].split()[-1]
            fname=f"Sent_{sid}.wav"

        elif seg["type"]=="Paragraph":

            fname="Para.wav"

        else:

            fname=f"Seg_{seg['id']}.wav"

        path=os.path.join(outdir,fname)

        clip.export(path,format="wav")

        seg["file"]=path


# =====================================================
# EXPORT EXCEL
# =====================================================

def export_excel(segments,outfile):

    from openpyxl import Workbook

    wb=Workbook()
    ws=wb.active

    ws.append([
        "ID",
        "Type",
        "Content",
        "From (MM:SS.mmm)",
        "To (MM:SS.mmm)",
        "Start(s)",
        "End(s)",
        "Duration(s)",
        "Confidence",
        "Audio File",
        "Note"
    ])

    for seg in segments:

        start=seg["start"]
        end=seg["end"]

        duration=None

        if start and end:
            duration=end-start

        ws.append([
            seg["id"],
            seg["type"],
            seg["content"],
            format_time(start),
            format_time(end),
            start,
            end,
            duration,
            seg["confidence"],
            seg["file"],
            seg["note"]
        ])

    wb.save(outfile)


# =====================================================
# MAIN
# =====================================================

def main():

    parser=argparse.ArgumentParser()

    parser.add_argument("--audio",required=True)
    parser.add_argument("--model",default="medium")
    parser.add_argument("--output_dir",default="segments")
    parser.add_argument("--excel",default="timestamps.xlsx")

    args=parser.parse_args()

    words=transcribe(args.audio,args.model)

    segments=build_segments(words)

    trim_audio(args.audio,segments,args.output_dir)

    export_excel(segments,args.excel)

    print("\nProcessing complete")
    print("Segments folder:",args.output_dir)
    print("Excel file:",args.excel)


if __name__=="__main__":
    main()