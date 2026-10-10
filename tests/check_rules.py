#!/usr/bin/env python3
"""Simple source-level checks; not a substitute for live Apache tests."""
from pathlib import Path
p = Path(__file__).resolve().parents[1] / 'rules' / 'bot-blocker.conf'
s = p.read_text()
assert 'RewriteCond %{HTTP_USER_AGENT}' in s
assert 'RewriteRule ^ - [F,L]' in s
assert 'Order Allow,Deny' not in s
assert 'RewriteCond %{HTTP_USER_AGENT} crawl' not in s
assert not any(line.strip() == '# BEGIN WordPress' for line in s.splitlines())
print('Static checks passed. Test with a configured Apache instance before deployment.')
