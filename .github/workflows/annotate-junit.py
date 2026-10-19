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
if not os.path.exists(path):
    print('::error::PHPUnit did not write %s (the run probably aborted before the summary)' % path)
    sys.exit(0)

root = ET.parse(path).getroot()
problems = []
for case in root.iter('testcase'):
    for kind in ('error', 'failure'):
        node = case.find(kind)
        if node is None:
            continue
        if 'Risky' in (node.get('type') or '') or 'Warning' in (node.get('type') or ''):
            continue  # risky tests and PHPUnit warnings do not fail the build
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

step_summary = os.environ.get('GITHUB_STEP_SUMMARY')
if step_summary:
    with open(step_summary, 'a') as fh:
        fh.write('\n'.join(summary) + '\n')
print('%d problem(s) annotated' % len(problems))
