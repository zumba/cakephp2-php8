#!/usr/bin/env python3
"""Turn PHPUnit JUnit results into GitHub Actions annotations.

GitHub shows at most 10 annotations per step, so the first failures and errors are
annotated individually and the rest are summarised in the step summary.
"""
import html
import os
import sys
import xml.etree.ElementTree as ET

path = sys.argv[1] if len(sys.argv) > 1 else 'junit.xml'
problems = []
cases = []
if not os.path.exists(path) or os.path.getsize(path) == 0:
    print('::error::PHPUnit did not write %s (the run probably aborted before the summary)' % path)
else:
    cases = list(ET.parse(path).getroot().iter('testcase'))
for case in cases:
    for kind in ('error', 'failure'):
        node = case.find(kind)
        if node is None:
            continue
        if (node.get('type') or '').endswith('RiskyTestError'):
            continue  # risky tests do not fail the build
        text = (node.text or '').strip()
        lines = [line for line in text.splitlines() if line.strip()]
        # PHPUnit writes "Class::test" on the first line, then the message
        message = node.get('message') or (lines[1] if len(lines) > 1 else (lines[0] if lines else kind))
        location = next((line for line in lines if line.startswith('/')), '')
        problems.append((kind, case.get('class') or '', case.get('name') or '', message, location, text))

summary = ['## PHPUnit: %d problem(s)' % len(problems), '']
for i, (kind, cls, name, message, location, text) in enumerate(problems):
    file_hint = ''
    if ':' in location:
        file_part, _, line_part = location.rpartition(':')
        if line_part.isdigit():
            file_hint = 'file=%s,line=%s,' % (file_part.split('/cakephp2-php8/', 1)[-1], line_part)
    if i < 10:
        print('::%s %stitle=%s::%s' % (kind, file_hint, '%s::%s' % (cls, name), message.replace('\n', ' ')[:900]))
    summary.append('### %s %s::%s' % (kind, cls, name))
    summary.append('```')
    summary.append(text[:1500])
    summary.append('```')

# Also publish PHPUnit's own console summary (errors and failures, without the warnings
# section), so the reason is visible even when the JUnit log has nothing to say.
output_path = sys.argv[2] if len(sys.argv) > 2 else None
if output_path and os.path.exists(output_path):
    lines = open(output_path, errors='replace').read().splitlines()
    starts = [i for i, line in enumerate(lines) if line.startswith('There w')]
    if starts:
        kept = []
        skipping = False
        for line in lines[starts[0]:]:
            if line.startswith('There w'):
                skipping = 'warning' in line or 'risky' in line
            if not skipping:
                kept.append(line)
        tail = kept
    else:
        tail = lines[-40:]
    text = '\n'.join(tail).strip()
    chunk = 900
    pieces = [text[i:i + chunk] for i in range(0, len(text), chunk)][:8]
    for n, piece in enumerate(pieces, 1):
        print('::error title=PHPUnit output %d/%d::%s' % (n, len(pieces), piece.replace('\n', '%0A')))
    summary.append('## PHPUnit console summary')
    summary.append('```')
    summary.append(text[:6000])
    summary.append('```')

step_summary = os.environ.get('GITHUB_STEP_SUMMARY')
if step_summary:
    with open(step_summary, 'a') as fh:
        fh.write('\n'.join(summary) + '\n')
print('%d problem(s) annotated' % len(problems))
