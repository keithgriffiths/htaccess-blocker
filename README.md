# htaccess-blocker

Optional **Apache 2.4** `.htaccess` snippets for basic bot user-agent filtering and targeted file protection, maintained by Keith Griffiths.

> **Use cautiously:** user-agent strings can be spoofed. Blocking by name does not stop sophisticated bots. A CDN/WAF and rate limiting are more effective for substantial abuse.

## What changed in v2.0

- Removed legacy Apache 2.2 `Order`, `Allow` and `Deny` directives.
- Removed duplicate `SetEnvIf` and rewrite lists and dangerously broad matches (such as `crawl`, `collect`, `wget`).
- Stopped explicitly blocking legitimate search engines and SEO crawlers by default.
- Removed the bundled WordPress rewrite block. Existing WordPress rules must remain intact.
- Split optional hardening from bot filtering.

## Requirements

- Apache 2.4 with `.htaccess` processing permitted (`AllowOverride` appropriately configured).
- `mod_rewrite` for bot filtering. `mod_authz_core` for optional secret-file protections.
- Does **not** work as-is on Nginx or on Cloudflare's edge. Your host may have restrictions on `.htaccess` directives.

## Installation

1. Make a **verified backup** of your existing `.htaccess` and have hosting file-manager/SFTP access ready if a mistake causes HTTP 500.
2. Open `rules/bot-blocker.conf`. Copy its text into your site's root `.htaccess`, **above** the `# BEGIN WordPress` / `# END WordPress` section. **Do not overwrite the full file.**
3. Keep the WordPress-managed section intact. Do not edit within it because WordPress can regenerate that section.
4. Start on a staging website. Load your home page, a permalink, `/wp-admin/`, and the login screen (if relevant).
5. Try the commands below; expect HTTP 403 for the test user agent, while a normal request should not be blocked by these rules.
6. Only after testing, deploy and monitor access/error logs. Roll back immediately if legitimate requests fail.

```bash
curl -I -A 'Mozilla/5.0' https://example.com/
curl -I -A 'WebBandit' https://example.com/
```

**Cloudflare note:** Cloudflare may challenge/block requests or cache content before Apache sees them. For origin-specific testing, use a staging origin and review its logs; do not weaken production security to perform the test.

## Optional hardening

See `rules/optional-hardening.conf`. This is **not installed automatically**. It shows how to restrict direct access to common sensitive files. The commented `Options -Indexes` directive requires permission from your host to enable. Review all file patterns for compatibility with your application before using them.

## Customising bots

Edit the alternation in the `RewriteCond` regular expression; use **specific product identifiers**, never a broad word such as `bot`, `crawl`, or `spider`. Avoid default blocking of search engines or legitimate audit tools. Consider a WAF rule for abusive traffic instead. Each additional rule should have a documented reason and be tested.

## Rollback

Remove only the added snippet (or restore the backed-up `.htaccess`) through SFTP/hosting file manager. Confirm that standard pages and WordPress permalinks still work. If you encounter HTTP 500, inspect Apache's error log and check whether `AllowOverride` permits the used directives.

## Limitations

- This is not an IP reputation database or an anti-DDoS solution.
- This repository does not claim to identify or verify real crawlers. UA filtering is easy to bypass.
- Apache `RewriteRule [F]` responds with HTTP 403; other server/WAF rules may alter observable responses.

## Licence

GPL-2.0, as in the original repository. See `LICENSE`.
