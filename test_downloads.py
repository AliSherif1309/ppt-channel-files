from pathlib import Path
import os
import re
import unittest
from playwright.sync_api import sync_playwright


class ArchiveTests(unittest.TestCase):
    def test_archive_paths_errors_and_duplicates(self):
        source = (Path(__file__).parent / 'index.html').read_text(encoding='utf-8')
        script = re.findall(r'<script>([\s\S]*?)</script>', source)[-1]
        with sync_playwright() as runner:
            browser = runner.chromium.launch(channel=os.environ.get('BROWSER_CHANNEL') or None)
            page = browser.new_page()
            page.set_content('<input id="searchInput"><button id="clearSearch"></button><button id="download">Download</button>')
            page.evaluate('''() => {
                window.archived = [];
                window.notices = [];
                window.alert = message => notices.push(message);
                window.JSZip = class {
                    file(name, data) { archived.push(name); }
                    async generateAsync() { return new Blob(['zip']); }
                };
                window.fetch = async url => {
                    if (url.includes('missing')) return new Response('', {status: 404});
                    if (url.includes('pointer')) return new Response('version https://git-lfs.github.com/spec/v1\\noid sha256:dummy');
                    return new Response('presentation');
                };
                HTMLAnchorElement.prototype.click = function() {};
                ['one/report.pptx', 'two/report.pptx', 'two/report.pptx', 'missing.pptx', 'pointer.pptx'].forEach(path => {
                    const card = document.createElement('div'); card.className = 'file-card';
                    card.setAttribute('data-relpath', path);
                    const link = document.createElement('a'); link.href = 'https://example.org/' + path;
                    card.appendChild(link); document.body.appendChild(card);
                });
            }''')
            page.add_script_tag(content=script)
            page.evaluate("downloadLinksAsZip(document.querySelectorAll('.file-card a'), 'folder', document.querySelector('#download'))")
            self.assertEqual(page.evaluate('archived'), ['one/report.pptx', 'two/report.pptx'])
            self.assertIn('2 file(s) were not included', page.evaluate('notices[0]'))
            self.assertFalse(page.locator('#download').is_disabled())
            self.assertEqual(page.locator('#download').inner_text(), 'Download')
            browser.close()


if __name__ == '__main__':
    unittest.main()
