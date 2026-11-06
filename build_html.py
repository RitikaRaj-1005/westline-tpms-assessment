# build_html.py — builds Westline_Findings_Full.html
# Run in Colab after Sections 1 to 7 (uses df, morning2 and fills from memory), with notes.json
# (the Assessment Notes exported as structured text) in the same folder as the output.
import json, io, base64, html as H
import numpy as np, pandas as pd, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def build(df, morning2, fills, notes_path, out_path):
    BLUE, ORANGE, GREY, INK, MUTED = '#2a78d6', '#eb6834', '#8a8984', '#0b0b0b', '#52514e'
    SPEC = {1: 115, 2: 105, 3: 105, 4: 100, 5: 100}
    SLOTS = ['1LO','1RO','2LO','2RO','3LO','3RO','4LI','4LO','4RI','4RO','5LI','5LO','5RI','5RO']
    NAME = {'KA25AB4471': 'T1 Goa', 'KA25AC1182': 'T2 Karwar', 'KA22AG3391': 'T6 Vijayapura',
            'KA22AD7730': 'T3 Gadag', 'KA25AE2016': 'T4 City', 'KA48AF9054': 'T5 Shivamogga'}
    DEPOT = {'KA25AB4471': 'Belagavi', 'KA25AC1182': 'Belagavi', 'KA22AG3391': 'Belagavi',
             'KA22AD7730': 'Hubballi', 'KA25AE2016': 'Hubballi', 'KA48AF9054': 'Hubballi'}
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10, 'axes.edgecolor': '#c9c8c2', 'axes.labelcolor': MUTED,
                         'xtick.color': MUTED, 'ytick.color': MUTED, 'axes.spines.top': False, 'axes.spines.right': False,
                         'axes.grid': True, 'grid.color': '#ecebe7', 'grid.linewidth': 0.8, 'axes.titlesize': 11,
                         'axes.titleweight': 'bold', 'axes.titlecolor': INK, 'axes.titlelocation': 'left'})
    def png(fig):
        b = io.BytesIO(); fig.savefig(b, format='png', dpi=160, bbox_inches='tight', facecolor='white'); plt.close(fig)
        return 'data:image/png;base64,' + base64.b64encode(b.getvalue()).decode()
    def med10(tr, cols, t0, t1):
        g = df[(df.truck == tr) & (df.Time >= t0) & (df.Time <= t1)].set_index('Time')[cols].astype(float)
        return g.resample('10min').median()
    figs = {}

    # Chart 1: Karwar 5RI vs its twin 5RO, 10 July 18:00 to 11 July 16:00
    k = med10('KA25AC1182', ['5RI PSI', '5RO PSI'], '2026-07-10 18:00', '2026-07-11 16:00')
    fig, ax = plt.subplots(2, 1, figsize=(10, 6.2), sharex=True, gridspec_kw={'height_ratios': [3, 2]})
    for a in ax:
        for s0, s1, lab in [('05:10', '06:20', 'Stop 1'), ('09:10', '10:20', 'Stop 2 (Hubballi)'), ('12:20', '16:00', 'Stop 3 (near Kittur)')]:
            a.axvspan(pd.Timestamp('2026-07-11 ' + s0), pd.Timestamp('2026-07-11 ' + s1), color='#f1f0ec', zorder=0)
    ax[0].plot(k.index, k['5RO PSI'], color=BLUE, lw=2); ax[0].plot(k.index, k['5RI PSI'], color=ORANGE, lw=2)
    ax[0].text(pd.Timestamp('2026-07-11 10:40'), 112, '5RO (twin)', color=INK, fontsize=9)
    ax[0].text(pd.Timestamp('2026-07-11 10:40'), 52, '5RI (failed)', color=INK, fontsize=9)
    ax[0].axhline(100, color=GREY, lw=0.8, ls='--'); ax[0].text(pd.Timestamp('2026-07-10 18:10'), 94, 'spec 100 PSI', color=MUTED, fontsize=8)
    ax[0].set_ylabel('PSI'); ax[0].set_title('Karwar truck, 10–11 July: the failed tyre against its twin (10-minute medians; shaded = truck stopped)')
    for lab, t in [('Stop 1', '05:10'), ('Stop 2', '09:10'), ('Stop 3', '12:20')]:
        ax[0].text(pd.Timestamp('2026-07-11 ' + t), 125, lab, color=MUTED, fontsize=8)
    ax[0].axvline(pd.Timestamp('2026-07-11 03:00'), color=GREY, lw=0.8); ax[0].text(pd.Timestamp('2026-07-11 03:05'), 20, 'departs 03:00', color=MUTED, fontsize=8)
    dif = k['5RI PSI'] - k['5RO PSI']
    ax[1].plot(dif.index, dif, color=INK, lw=2)
    for th, lab in [(-10, 'inspect: 10 PSI (first bin 03:40)'), (-20, 'urgent: 20 PSI (first bin 06:10)')]:
        ax[1].axhline(th, color=ORANGE, lw=1, ls='--'); ax[1].text(pd.Timestamp('2026-07-10 18:10'), th + 2, lab, color=MUTED, fontsize=8)
    ax[1].set_ylabel('5RI − 5RO (PSI)'); ax[1].set_title('Twin difference with the candidate two-level warning')
    plt.tight_layout(); figs['karwar'] = png(fig)

    # Chart 2: morning cold pressure vs spec by truck
    order = ['KA25AB4471', 'KA25AC1182', 'KA22AG3391', 'KA22AD7730', 'KA25AE2016', 'KA48AF9054']
    fig, ax = plt.subplots(figsize=(10, 3.6))
    for i, tr in enumerate(order):
        x = morning2[morning2.truck == tr].dev
        c = BLUE if DEPOT[tr] == 'Belagavi' else ORANGE
        ax.plot([x.quantile(.25), x.quantile(.75)], [i, i], color=c, lw=6, solid_capstyle='round', alpha=.45)
        ax.plot([x.median()], [i], 'o', color=c, ms=9, markeredgecolor='white', markeredgewidth=2)
        ax.text(x.median(), i - 0.22, f'{x.median():+.1f}', ha='center', color=INK, fontsize=8)
    ax.axvline(0, color=GREY, lw=1); ax.set_yticks(range(6)); ax.set_yticklabels([f'{NAME[t]} ({DEPOT[t]})' for t in order])
    ax.invert_yaxis(); ax.set_ylim(5.5, -0.7); ax.set_xlabel('Morning cold pressure minus spec (PSI); dot = median, bar = middle 50% of readings')
    ax.set_title('Every Hubballi truck starts the day 10 to 12 PSI under spec; every Belagavi truck starts on spec')
    plt.tight_layout(); figs['morning'] = png(fig)

    # Chart 3: when and how hot each depot's detected pressure adjustments happen
    fl = fills.copy(); fl['depot'] = fl.truck.map(DEPOT); fl['hour'] = fl.bin.dt.hour + fl.bin.dt.minute / 60
    fig, ax = plt.subplots(figsize=(10, 3.6))
    for dep, c in [('Belagavi', BLUE), ('Hubballi', ORANGE)]:
        x = fl[fl.depot == dep]
        ax.scatter(x.hour, x.temp, s=42, color=c, edgecolor='white', linewidth=1.2, label=f'{dep} ({len(x)} tyre adjustments)')
    ax.set_xlim(0, 24); ax.set_xticks(range(0, 25, 3)); ax.set_xlabel('Time of day of the detected adjustment')
    ax.set_ylabel('Tyre temperature (°C)'); ax.legend(frameon=False, loc='upper left')
    ax.set_title('Belagavi adjusts early, at low tyre temperatures; Hubballi adjusts hot in the afternoon, both to the card values')
    plt.tight_layout(); figs['fills'] = png(fig)

    # Chart 4: Goa truck, pre-8 June trip day vs a post-8 June event day (small multiples, no dual axis)
    goa = df[df.truck == 'KA25AB4471'].set_index('Time')
    P = goa[[f'{s} PSI' for s in SLOTS]].astype(float).resample('10min').median()
    dev = pd.concat([P[f'{s} PSI'] - SPEC[int(s[0])] for s in SLOTS], axis=1).median(axis=1)
    tmp = goa[[f'{s} TEMP' for s in SLOTS]].astype(float).resample('10min').median().median(axis=1)
    days = [('2026-06-02', 'Pre-8 June comparison trip day (2 June)', None), ('2026-06-27', 'Post-8 June event trip day (27 June)', ('15:20', '16:10'))]
    fig, ax = plt.subplots(2, 2, figsize=(10, 5.4), sharey='row')
    for j, (d, lab, evw) in enumerate(days):
        sl = slice(f'{d} 05:00', f'{d} 21:00')
        ax[0, j].plot(dev.loc[sl].index, dev.loc[sl], color=BLUE, lw=2); ax[0, j].axhline(0, color=GREY, lw=0.8)
        ax[1, j].plot(tmp.loc[sl].index, tmp.loc[sl], color=ORANGE, lw=2)
        ax[0, j].set_title(lab); ax[0, j].set_ylabel('Median PSI vs spec' if j == 0 else '')
        ax[1, j].set_ylabel('Median tyre temp (°C)' if j == 0 else '')
        if evw:
            for a in ax[:, j]: a.axvspan(pd.Timestamp(f'{d} {evw[0]}'), pd.Timestamp(f'{d} {evw[1]}'), color='#e4e3de', zorder=0)
            ax[0, j].text(pd.Timestamp(f'{d} {evw[1]}'), ax[0, j].get_ylim()[1] * 0.85, '  detected cooling event', color=MUTED, fontsize=8)
        for a in ax[:, j]:
            a.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%H:%M'))
    plt.tight_layout(); figs['goa'] = png(fig)

    # Text from the notes
    B = json.load(open(notes_path, encoding='utf-8'))
    def runs(rs): return ''.join(f'<strong>{H.escape(t)}</strong>' if b else H.escape(t) for t, b in rs)
    sections, cur = [], None
    for b in B:
        if b['type'] == 'p' and b['style'] == 'TITLE': continue
        if b['type'] == 'p' and b['style'] == 'HEADING_1':
            cur = {'title': ''.join(t for t, _ in b['runs']), 'items': []}; sections.append(cur); continue
        if cur is None: continue
        cur['items'].append(b)
    def render(items):
        out, in_list = [], False
        for b in items:
            if b['type'] == 'table':
                if in_list: out.append('</ul>'); in_list = False
                rows = b['rows']
                out.append('<div class="tw"><table><thead><tr>' + ''.join(f'<th>{H.escape(c)}</th>' for c in rows[0]) + '</tr></thead><tbody>' +
                           ''.join('<tr>' + ''.join(f'<td>{H.escape(c)}</td>' for c in r) + '</tr>' for r in rows[1:]) + '</tbody></table></div>')
                continue
            t = runs(b['runs'])
            if b['style'] == 'HEADING_2':
                if in_list: out.append('</ul>'); in_list = False
                plain = ''.join(x for x, _ in b['runs']); fid = plain.split('.')[0] if plain[:1] == 'F' and plain[1:2].isdigit() else ''
                out.append(f'<h3 id="{fid}">{t}</h3>' if fid else f'<h3>{t}</h3>')
            elif b['bullet']:
                if not in_list: out.append('<ul>'); in_list = True
                out.append(f'<li>{t}</li>')
            else:
                if in_list: out.append('</ul>'); in_list = False
                out.append(f'<p>{t}</p>')
        if in_list: out.append('</ul>')
        return '\n'.join(out)
    keep = [s for s in sections if not s['title'].startswith('AI working log')]
    sid = lambda s: ''.join(ch for ch in s.lower().split(':')[0] if ch.isalnum() or ch == ' ').strip().replace(' ', '-')
    toc = ''.join(f'<a href="#{sid(s["title"])}">{H.escape(s["title"].split(":")[0])}</a>' for s in keep)
    body = '\n'.join(f'<section id="{sid(s["title"])}"><h2>{H.escape(s["title"])}</h2>\n{render(s["items"])}</section>' for s in keep)
    ftitles = [''.join(t for t, _ in b['runs']) for s in sections if s['title'] == 'Detailed findings' for b in s['items'] if b['type'] == 'p' and b['style'] == 'HEADING_2']
    findex = ''.join(f'<li><a href="#{t.split(".")[0]}">{H.escape(t)}</a></li>' for t in ftitles)

    summary = f'''
<section id="answers"><h2>What is happening with the tyres: the short answers</h2>
<div class="cards">
<div class="card"><div class="q">The "nothing but alarms" on the Goa truck</div>
<p>The afternoon drops are the whole truck cooling, not tyres leaking. In all 13 Goa events every one of the 14 tyres lost pressure together, at 0.66 to 0.73 PSI per °C as tyre temperature fell 12 to 18 °C, and pressure largely came back as the tyres warmed. They start on 9 June, which fits Ramesh's afternoon rain, but there is no weather data to prove it, and the same pattern appears on all six trucks. Whether these set off TyreSense alarms needs the alert log. <a href="#F17">F17</a></p></div>
<div class="card"><div class="q">Are the Hubballi roads eating the tyres?</div>
<p>Not mainly. Hubballi tops up in the hot afternoon to the cold card value, so its trucks start every morning 10 to 12 PSI under spec; Belagavi adjusts early in the morning, at much lower tyre temperatures, and starts on spec. Between fills Hubballi tyres lose only 1 to 2 PSI per 30 days more than Belagavi's, far too little to explain the gap, though a small road effect is not ruled out. <a href="#F14">F14</a>–<a href="#F16">F16</a></p></div>
<div class="card"><div class="q">Could the Karwar failure on 11 July have been foreseen?</div>
<p>Not a day ahead: the tyre was at spec the night before and no earlier day showed any warning. On the day, yes: it pulled away from its twin from about 03:15, passed 10 PSI at 03:40 and 20 PSI at 06:10, well before it fell below 70 PSI at 09:03 and before the truck stopped in Hubballi. Whether anyone could have acted depends on who sees alerts. <a href="#F12">F12</a></p></div>
<div class="card"><div class="q">One alarm, on one tyre</div>
<p>A twin comparison (inner against outer on the same hub) is a candidate: a 10 PSI difference sustained 20 minutes to inspect, 20 PSI as urgent, with a reset band. Over six weeks it would have flagged two real conditions and nothing else, and it stays silent through the afternoon cooling. It is tested on one failure only and does not cover the single tyres on axles 1 to 3. <a href="#F13">F13</a></p></div>
</div>
<div class="act"><strong>Worth acting on now:</strong> fill tyres cold at both depots (or use a hot-fill allowance); inspect Goa 4LI, Karwar 3LO, Gadag 5RO and City 5RI, which lose air several times faster than the spec's 3 PSI a month (<a href="#F16">F16</a>); replace the Shivamogga 2RO sensor, at 1% battery (<a href="#F18">F18</a>); fix the data issues before the next export: a duplicated 12-hour overlap, a wrong registration on the Goa truck's July file and the mislabelled C/D side codes (<a href="#F1">F1</a>–<a href="#F3">F3</a>).</div>
</section>
<section id="charts"><h2>Key charts</h2>
<figure><img src="{figs['karwar']}" alt="Karwar 5RI against its twin 5RO on 10 and 11 July, with the twin difference crossing 10 PSI at 03:40 and 20 PSI at 06:10"><figcaption>The failed Karwar 5RI against its twin. The difference passed the inspection level at 03:40 and the urgent level at 06:10, hours before the tyre fell below 70 PSI. Source: Section 4; <a href="#F12">F12</a>.</figcaption></figure>
<figure><img src="{figs['morning']}" alt="Median morning cold pressure minus spec by truck: about -1 PSI for the Belagavi trucks and -10 to -12 PSI for the Hubballi trucks"><figcaption>Morning cold readings (truck parked at least 3 hours). Source: Section 5; <a href="#F14">F14</a>.</figcaption></figure>
<figure><img src="{figs['fills']}" alt="Detected pressure adjustments: Belagavi at 06:00 to 07:00 with tyres at 22 to 28 °C; Hubballi at 15:00 to 16:00 with tyres at 32 to 52 °C"><figcaption>Each dot is one tyre adjusted while the truck was parked. Source: Section 5; <a href="#F15">F15</a>.</figcaption></figure>
<figure><img src="{figs['goa']}" alt="Goa truck median pressure versus spec and median tyre temperature on 2 June and on 27 June, showing pressure falling with temperature during the afternoon event"><figcaption>Pressure follows tyre temperature on the Goa truck; the grey band is a detected common cooling event. Source: Section 6; <a href="#F17">F17</a>.</figcaption></figure>
</section>
<section id="index"><h2>Findings index</h2><ol class="fi">{findex}</ol></section>'''

    css = '''
:root{--bg:#fcfcfb;--card:#ffffff;--ink:#0b0b0b;--ink2:#52514e;--line:#e4e3de;--accent:#2a78d6;--accent2:#eb6834;--soft:#f4f3ef}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#1a1a19;--card:#232321;--ink:#f0efec;--ink2:#c3c2b7;--line:#3a3936;--accent:#5c9eea;--accent2:#e07a4f;--soft:#2a2a28}}
:root[data-theme="dark"]{--bg:#1a1a19;--card:#232321;--ink:#f0efec;--ink2:#c3c2b7;--line:#3a3936;--accent:#5c9eea;--accent2:#e07a4f;--soft:#2a2a28}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15.5px/1.6 "Source Serif 4",Georgia,serif}
header{padding:48px 16px 28px;border-bottom:1px solid var(--line)}header .w,main{max-width:980px;margin:0 auto}
.kicker{font:600 12px/1 system-ui,sans-serif;letter-spacing:.12em;text-transform:uppercase;color:var(--accent2)}
h1{font:700 34px/1.15 system-ui,sans-serif;margin:10px 0 8px;letter-spacing:-.01em}.sub{color:var(--ink2);margin:0;max-width:720px}
nav{position:sticky;top:0;background:var(--bg);border-bottom:1px solid var(--line);z-index:2;overflow-x:auto;white-space:nowrap;padding:10px 16px;font:500 13px system-ui,sans-serif}
nav a{color:var(--ink2);text-decoration:none;margin-right:18px}nav a:hover{color:var(--accent)}
main{padding:0 16px 80px}section{padding-top:36px}h2{font:700 23px/1.25 system-ui,sans-serif;margin:0 0 14px;padding-top:6px;border-top:2px solid var(--ink)}
h3{font:650 17px/1.35 system-ui,sans-serif;margin:30px 0 8px;scroll-margin-top:56px}p{margin:0 0 12px}a{color:var(--accent)}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px}.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px 18px}
.card .q{font:650 15px/1.3 system-ui,sans-serif;margin-bottom:8px}.card p{margin:0;font-size:14.5px}
.act{margin-top:14px;background:var(--soft);border-left:3px solid var(--accent2);padding:12px 16px;border-radius:6px;font-size:14.5px}
figure{margin:0 0 28px;background:#fff;border:1px solid var(--line);border-radius:10px;padding:12px}figure img{width:100%;height:auto;display:block}
figcaption{font:13px/1.45 system-ui,sans-serif;color:#52514e;margin-top:8px}
.tw{overflow-x:auto;margin:6px 0 18px}table{border-collapse:collapse;width:100%;font:13px/1.45 system-ui,sans-serif}
th{text-align:left;font-weight:650;border-bottom:2px solid var(--ink);padding:7px 10px 6px 0;vertical-align:bottom}td{border-bottom:1px solid var(--line);padding:7px 10px 7px 0;vertical-align:top}
ul{padding-left:20px;margin:0 0 12px}li{margin-bottom:6px}.fi{padding-left:22px;font:14px/1.5 system-ui,sans-serif}.fi li{margin-bottom:4px}
footer{max-width:980px;margin:0 auto;padding:24px 16px 48px;color:var(--ink2);font:13px system-ui,sans-serif;border-top:1px solid var(--line)}
@media (max-width:600px){h1{font-size:27px}body{font-size:15px}}
'''
    doc = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Westline Tyre Findings</title><style>{css}</style></head><body>
<header><div class="w"><div class="kicker">Westline Carriers · TPMS assessment · 1 June – 15 July 2026</div>
<h1>What is happening with the fleet's tyres</h1>
<p class="sub">All findings from six weeks of TyreSense data on six trucks, cross-checked against the tyre register, inspection sheets, km log, spec sheet and the fleet manager's account. Prepared by Ritika Raj Parekh, 6 November 2026.</p></div></header>
<nav><a href="#answers">Answers</a><a href="#charts">Charts</a><a href="#index">Findings index</a>{toc}</nav>
<main>{summary}
{body}</main>
<footer>Built from the Assessment Notes with build_html.py. All figures come from the Colab notebook in 04_Code; every finding lists the checks behind it, its confidence and what could change it.</footer>
</body></html>'''
    open(out_path, 'w', encoding='utf-8').write(doc)
    return out_path

if __name__ == '__main__':
    # In Colab: build(df, morning2, fills, DATA + 'notes.json', DATA + 'Westline_Findings_Full.html')
    pass
