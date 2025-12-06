# ADMST Framework v1.0 - RELEASE EXECUTION GUIDE

**Release Date:** December 6, 2025  
**Status:** ✅ **RELEASED** (Tag created and pushed)  
**Repository:** https://github.com/ambjeffreycareyjm3-cpu/ADMiST  
**Tag:** `v1.0`  
**Commit:** `6b1acc9`  

---

## 🎉 RELEASE MILESTONE ACHIEVED

The ADMST Framework v1.0 has been officially tagged and pushed to GitHub. This document provides step-by-step instructions to complete the publication process.

---

## ✅ Release Checklist Status

### Phase 1: Git Tagging ✅ COMPLETE
- [x] Run final validation (19/19 checks passing)
- [x] Create annotated git tag: `git tag -a v1.0 -m "..."`
- [x] Push tag to GitHub: `git push origin v1.0`
- [x] Verify tag on remote: https://github.com/ambjeffreycareyjm3-cpu/ADMiST/releases/tag/v1.0

**Result:** 
```
v1.0 tag created and pushed to origin
Tagger: ambjeffreycareyjm3-cpu <ambjeffreycareyjm3@gmail.com>
Date: Sat Dec 6 03:09:40 2025 +0000
```

---

## 📋 Remaining Publication Steps

### Phase 2: GitHub Release (5-10 minutes)

**Action:** Create a formal GitHub Release from the v1.0 tag

**Steps:**
1. Go to: https://github.com/ambjeffreycareyjm3-cpu/ADMiST/releases
2. Click **"Draft a new release"** (or GitHub may auto-suggest creating a release)
3. Fill in the following fields:

| Field | Value |
|-------|-------|
| **Tag version** | v1.0 (should auto-select) |
| **Release title** | ADMST Framework v1.0 |
| **Description** | See content below ↓ |
| **Set as latest release** | ☑ (check) |
| **Set as pre-release** | ☐ (uncheck) |

**Release Description Template:**
Copy and paste the content from `/workspaces/ADMiST/RELEASE_NOTES.md`:

```markdown
# ADMST Framework v1.0

**Release Date:** 2024-12-06

## Overview

Complete, reproducible computational framework for ADMST-SCBC cosmological analysis.

## Features

✅ **Physics Module** (`admst/cosmo.py`)
- Soliton gas background evolution
- Matter power spectrum modifications
- CMB damping modulation
- Gravitational wave spectrum
- Lab-scale predictions

✅ **CLASS Integration** 
- 3 complete physics patches (background, perturbations, thermodynamics)
- Automated build and test system
- Dummy fallback for development

✅ **MCMC Framework**
- Cobaya integration with Planck 2018 likelihoods
- Parameter constraints
- Results analysis tools

✅ **Reproducibility**
- Docker containerization
- GitHub Actions CI/CD
- Pre-commit hooks
- Unit tests (9 passing)

✅ **Documentation**
- User guides
- Physics implementation details
- Developer contributing guidelines
- Quick-start tutorials

[... continue with rest of RELEASE_NOTES.md content ...]
```

**After Publishing:**
- ✅ GitHub will automatically create the release page
- ✅ Release will be accessible at: https://github.com/ambjeffreycareyjm3-cpu/ADMiST/releases/tag/v1.0
- ✅ Zenodo can sync from this release

---

### Phase 3: Zenodo Integration (2-3 minutes)

**Objective:** Enable automatic Zenodo archival and DOI assignment

**Steps:**

1. **Visit Zenodo Settings:**
   - Go to: https://zenodo.org/account/settings/github/
   - Sign in to Zenodo (create free account if needed)

2. **Connect Your GitHub Account:**
   - Click "Connect with GitHub" if not already connected
   - Authorize Zenodo to access your GitHub repositories

3. **Enable Auto-Sync for ADMiST:**
   - Find "ambjeffreycareyjm3-cpu/ADMiST" in the list
   - Toggle the switch to **ON** (enable)
   - Zenodo will now automatically sync releases to Zenodo

4. **Wait for DOI Assignment:**
   - First sync may take 5-30 minutes
   - You'll receive an email when DOI is assigned
   - DOI will be in format: `10.5281/zenodo/XXXXXXX`

**After Zenodo Sync Completes:**
- ✅ Release snapshot preserved on Zenodo
- ✅ DOI assigned automatically
- ✅ Entry created with full metadata
- ✅ Citable reference ready for papers

---

### Phase 4: Update Citation Metadata (5 minutes)

**Once Zenodo assigns DOI:**

Update `CITATION.cff` with the actual Zenodo DOI:

```bash
cd /workspaces/ADMiST

# Edit CITATION.cff and replace placeholder with actual DOI
# For example, if you receive DOI: 10.5281/zenodo/12345678
# Replace: 10.5281/zenodo.XXXXXXX
# With: 10.5281/zenodo.12345678

# After editing:
git add CITATION.cff
git commit -m "docs: Update CITATION.cff with Zenodo DOI v1.0"
git push origin feat/ci-precommit
```

---

### Phase 5: Docker Build Verification (Optional, 15 minutes)

**Objective:** Verify reproducibility with Docker containerization

**Steps:**
```bash
cd /workspaces/ADMiST

# Full Docker build + test
./tools/docker_build_and_test.sh

# Expected output:
# ✓ Docker image built successfully
# ✓ Container verification passed
# ✓ LCDM baseline computed
# ✓ All checks passed (reproducible)
```

**Result:** Confirms framework works identically across different systems

---

### Phase 6: arXiv Submission (Optional, 30 minutes - 2 hours)

**For academic visibility and peer review:**

**Prepare:**
1. Create or update `MANUSCRIPT.tex` with your research
   - Use physics details from `CLASS_INTEGRATION_README.md`
   - Include results plots from `run_analysis.py`
   - Reference code at: https://github.com/ambjeffreycareyjm3-cpu/ADMiST

2. Gather submission files:
   ```bash
   mkdir -p arxiv_submission
   cp MANUSCRIPT.pdf arxiv_submission/
   cp results/*.pdf arxiv_submission/
   zip -r arxiv_submission/sources.zip admst/ tests/ tools/ patches/ \
       requirements.txt CITATION.cff LICENSE README.md
   ```

**Submit to arXiv:**
1. Go to: https://arxiv.org/submit
2. Create account or sign in
3. Select category: **astro-ph.CO** (Cosmology and Nongalactic Astrophysics)
4. Fill in metadata:
   - **Title:** "ADMST-CLASS: Asymmetric Dark Matter Soliton Theory Framework"
   - **Authors:** Your name(s)
   - **Abstract:** [Your abstract]
   - **Comments:** "Code available at https://github.com/ambjeffreycareyjm3-cpu/ADMiST (v1.0, https://zenodo.org/record/XXXXX)"

5. Upload PDF and sources.zip
6. Review and submit

**After Publication:**
- arXiv ID will be assigned (e.g., `2412.12345`)
- Update README.md with arXiv link
- Share on social media with preprint URL

---

## 📊 Current Status Dashboard

| Component | Status | Details |
|-----------|--------|---------|
| **Git Tag** | ✅ Done | v1.0 created and pushed |
| **Framework Tests** | ✅ Passing | 9/9 tests, 19/19 validation |
| **Documentation** | ✅ Complete | 8 comprehensive guides |
| **GitHub Release** | 📋 Pending | Create from v1.0 tag |
| **Zenodo DOI** | 📋 Pending | Enable auto-sync (email-triggered) |
| **Docker Verification** | 🔄 Optional | Run when needed |
| **arXiv Preprint** | 🔄 Optional | Prepare manuscript as desired |

---

## 🔗 Key Links

| Resource | URL |
|----------|-----|
| **GitHub Repository** | https://github.com/ambjeffreycareyjm3-cpu/ADMiST |
| **GitHub v1.0 Tag** | https://github.com/ambjeffreycareyjm3-cpu/ADMiST/releases/tag/v1.0 |
| **GitHub Releases Page** | https://github.com/ambjeffreycareyjm3-cpu/ADMiST/releases |
| **Zenodo Settings** | https://zenodo.org/account/settings/github/ |
| **arXiv Submission** | https://arxiv.org/submit |
| **CITATION.cff File** | /workspaces/ADMiST/CITATION.cff |
| **RELEASE_NOTES** | /workspaces/ADMiST/RELEASE_NOTES.md |

---

## ⏱️ Timeline Summary

| Phase | Timeline | Status |
|-------|----------|--------|
| **Git Tagging** | 5 min | ✅ Done |
| **GitHub Release** | 5-10 min | 📋 Next |
| **Zenodo Sync** | 5 min + 5-30 min wait | 📋 After release |
| **Update Citation** | 5 min | 🔄 After Zenodo DOI |
| **Docker Verify** | 15 min | 🔄 Optional |
| **arXiv Submit** | 2 hours | 🔄 Optional |
| **Total Time** | ~30 min (essential) | - |

---

## 🚀 Quick Reference: Immediate Next Step

**Right Now:**
```bash
# Navigate to releases
https://github.com/ambjeffreycareyjm3-cpu/ADMiST/releases

# Click: "Draft a new release"
# - Tag: v1.0 (pre-selected)
# - Title: "ADMST Framework v1.0"
# - Description: [paste RELEASE_NOTES.md]
# - Publish release
```

**Then:**
```bash
# Enable Zenodo auto-sync
https://zenodo.org/account/settings/github/
# Toggle: ambjeffreycareyjm3-cpu/ADMiST ON
```

**Result:** Public release with automatic DOI ✅

---

## 📝 Frequently Asked Questions

**Q: Is the framework ready to release?**  
A: ✅ Yes. All 19 validation checks pass, all 9 tests pass, documentation is complete.

**Q: Do I need to create all optional steps?**  
A: No. GitHub Release + Zenodo DOI are essential (30 min). Docker verification and arXiv are optional but recommended for full publication chain.

**Q: Can I edit the release after publishing?**  
A: ✅ Yes. GitHub releases can be edited after publication. Click the pencil icon on any release.

**Q: What if the Docker build fails?**  
A: Framework is still publishable. Docker is for reproducibility verification. See `DOCKER_QUICKSTART.md` for troubleshooting.

**Q: When do I submit to a journal?**  
A: After arXiv preprint (optional). Journals typically want 24+ hour arXiv posting before submission. See `PUBLICATION_TIMELINE.md` for details.

**Q: How long until Zenodo assigns a DOI?**  
A: Usually 5-30 minutes after enabling GitHub sync. You'll receive an email confirmation.

---

## ✨ Success Indicators

You'll know the release is successful when:

1. ✅ v1.0 tag appears at: https://github.com/ambjeffreycareyjm3-cpu/ADMiST/releases/tag/v1.0
2. ✅ Release page displays with title "ADMST Framework v1.0"
3. ✅ Email from Zenodo with subject "New version v1.0 of ...ADMiST"
4. ✅ DOI appears in email (format: 10.5281/zenodo/XXXXXXX)
5. ✅ Framework becomes citable in academic papers

---

## 📞 Support & Resources

| Need | Resource |
|------|----------|
| **Release procedure** | This guide (RELEASE_EXECUTION_GUIDE.md) |
| **Publication timeline** | PUBLICATION_TIMELINE.md |
| **Framework overview** | FINAL_SUMMARY.md |
| **Quick start** | QUICK_START_PUBLICATION.sh |
| **Physics details** | CLASS_INTEGRATION_README.md |
| **Docker setup** | DOCKER_QUICKSTART.md |

---

## 🎯 Summary

**Current Status:** ✅ v1.0 tagged and pushed to GitHub

**Next Step:** Create GitHub Release (5 minutes)

**Then:** Enable Zenodo auto-sync (2 minutes)

**Result:** Public, citable, reproducible ADMST Framework v1.0 🎉

**Timeline to completion:** ~30 minutes (essential steps)

---

**Document:** Release Execution Guide  
**Version:** 1.0  
**Date:** 2025-12-06  
**Status:** ✅ v1.0 TAGGED AND PUSHED  

See `PUBLICATION_TIMELINE.md` for extended publication roadmap (arXiv, journals, etc.)
