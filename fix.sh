#!/bin/sh
# Celestial Electric - repo v2.1 one-shot fixer
# Does EVERYTHING: moves the 4 uploaded docs from root into their asset folders
# (fixing filenames/spaces), updates README doc-control table + build phase,
# prepends CHANGELOG v2.1, deletes itself, commits, pushes, prints verification.
# Run:  git pull   then   sh fix.sh

set -e
cd "$(git rev-parse --show-toplevel)"
mkdir -p docs/assets/pdfs docs/assets/drawings docs/assets/images

echo "== Moving docs into asset folders =="
for f in CEL-MPT-QA-001*; do
  [ -f "$f" ] && git mv -f "$f" docs/assets/pdfs/CEL-MPT-QA-001_commissioning_checklist.pdf && echo "moved: $f"
done
for f in CEL-MPT-RM-001*; do
  [ -f "$f" ] && git mv -f "$f" docs/assets/pdfs/CEL-MPT-RM-001_platform_roadmap.pdf && echo "moved: $f"
done
for f in DWG-003*; do
  [ -f "$f" ] && git mv -f "$f" docs/assets/drawings/DWG-003_isolated_sense_front_end.svg && echo "moved: $f"
done
for f in CEL-MPT-UX-001*; do
  [ -f "$f" ] && git mv -f "$f" docs/assets/images/CEL-MPT-UX-001_dashboard_mockup.svg && echo "moved: $f"
done

echo "== Updating README + CHANGELOG =="
python3 << 'PYEOF'
import re

DOCTABLE = """## Document control

| Doc | Title | Rev |
| --- | --- | --- |
| CEL-MPT-FW-002 | Cloud firmware (field-hardened) | 2.0 |
| CEL-MPT-DWG-001 | Bench wiring diagram | 1.0 |
| CEL-MPT-DWG-002 | Enclosure & home-run install diagram | 1.0 |
| CEL-MPT-DWG-003 | Isolated 12V sense front end (V2.5) | 1.0 |
| CEL-MPT-INS-001 | Install packet (BOM addendum + pull schedule) | 1.0 |
| CEL-MPT-QA-001 | Commissioning & QA sign-off checklist | 1.0 |
| CEL-MPT-RM-001 | Platform evolution roadmap (Sentinel Node) | 1.0 |
| CEL-MPT-UX-001 | Dashboard display mockup (V2.5) | 1.0 |

"""

BUILDPHASE = """## Build phase

- [x] Concept documentation
- [x] Arduino Project Hub submission
- [x] Bench test sketch
- [x] Parts list
- [x] Cloud sketch (REV 2.0, field-hardened)
- [x] Enclosure + home-run install package (CEL-MPT-INS-001)
- [x] Commissioning checklist authored (CEL-MPT-QA-001)
- [x] Platform evolution roadmap adopted (CEL-MPT-RM-001)
- [x] V2.5 isolated sense front end designed (CEL-MPT-DWG-003)
- [ ] Purchase parts (V2.0 baseline)
- [ ] Build bench prototype
- [ ] Install monitoring enclosure
- [ ] Commissioning per QA-001 (incl. closed-lid RF test)
- [ ] Add real trailer photos
- [ ] Update Project Hub page after first field test
- [ ] V2.5 Power Sense build (gated on QA-001 Phases 1-2 pass)

"""

CHANGE = """## v2.1 - 2026-07-03

### Documentation
- Added CEL-MPT-QA-001 commissioning & QA sign-off checklist (docs/assets/pdfs).
- Added CEL-MPT-RM-001 platform evolution roadmap - Sentinel Node (docs/assets/pdfs).
- Added CEL-MPT-DWG-003 isolated 12V bank sense front-end drawing (docs/assets/drawings).
- Added CEL-MPT-UX-001 V2.5 dashboard display mockup (docs/assets/images).
- README: doc-control table and build-phase checklist updated to v2.1 doc family.

"""

r = open("README.md").read()
r = re.sub(r"## Build phase\n.*?(?=## )", BUILDPHASE, r, flags=re.S)
r = re.sub(r"## Document control\n.*?(?=## )", DOCTABLE, r, flags=re.S)
open("README.md","w").write(r)
print("README updated")

c = open("CHANGELOG.md").read()
if "v2.1" not in c:
    c = c.replace("# Changelog\n", "# Changelog\n\n" + CHANGE, 1)
    open("CHANGELOG.md","w").write(c)
    print("CHANGELOG updated")
else:
    print("CHANGELOG already has v2.1 - skipped")
PYEOF

echo "== Commit + push =="
rm -f fix.sh
git add -A
git commit -m "v2.1: doc family filed, README + changelog updated" || echo "(nothing to commit)"
git push

echo "=================================="
echo "VERIFICATION"
echo "PDFs (target 8):";     ls docs/assets/pdfs | wc -l
echo "Drawings (target 3):"; ls docs/assets/drawings | wc -l
echo "Images (target 5):";   ls docs/assets/images | wc -l
echo "Total tracked (target 41):"; git ls-files | wc -l
echo "=================================="
