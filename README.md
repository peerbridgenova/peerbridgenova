# PeerBridge

Static site. Plain HTML, CSS, and one JS file. No build step, no dependencies.

Live at **peerbridgenova.vercel.app**

---

## Files

| File | What it is |
|---|---|
| `index.html` | Home |
| `about.html` | Our Mission |
| `team.html` | Our Team |
| `articles.html` | Articles |
| `glossary.html` | Glossary of mental health terms (searchable) |
| `stories.html` | Share Your Story |
| `get-involved.html` | Join the Team / upcoming roles |
| `donate.html` | Ways to support |
| `contact.html` | Contact form |
| `thanks.html` | Post-submit confirmation |
| `styles.css` | All styling |
| `script.js` | Nav, glossary filter, anti-spam check |
| `_build.py` | Optional generator + all the SVG illustrations (see below) |

Files beginning with `_` other than `_build.py` are scratch renders from designing the illustrations. `.gitignore` already excludes them; delete them whenever.

## Design notes

- Palette matches the Instagram: teal `#1198B8`, deep teal `#0C6D86`, gold `#D4B14D`. Backgrounds are light blue `#EAF5F9` and cream `#FDF9F1` — deliberately never plain white, which is what made the earlier version feel like a business site.
- Corners are large (22–44px) and every button is a full pill. Sections are separated by curved SVG edges rather than straight rules.
- Type stays restrained (Plus Jakarta Sans, with Fraunces for pull quotes) so the soft shapes carry the warmth without the whole thing turning childish.

---

## Deploying your changes

Vercel is watching the GitHub repo. **Anything you push to the `main` branch goes live in about 30 seconds.** You don't need to touch Vercel at all.

### Option A — GitHub in the browser (easiest)

1. Go to the repo on github.com.
2. Click a file → pencil icon → paste the new contents.
3. Scroll down, write a short message like "update glossary", click **Commit changes**.
4. Open vercel.com → your project → **Deployments**. You'll see a new one building.

For adding a *new* file: repo home → **Add file** → **Upload files** → drag it in → Commit.

### Option B — Command line

```bash
git clone https://github.com/<owner>/<repo>.git
cd <repo>

# copy the new files in, overwriting the old ones, then:
git add -A
git commit -m "Redesign site, add glossary/stories/donate pages"
git push origin main
```

If `git push` is rejected because someone else pushed first:

```bash
git pull --rebase origin main
git push origin main
```

### If a deploy fails

Vercel → project → **Deployments** → click the failed one → **Build Logs**. For a static site the usual cause is a wrong **Output Directory** setting. It should be:

- Framework Preset: **Other**
- Build Command: *(empty)*
- Output Directory: *(empty, or `.`)*

### Rolling back

Vercel → **Deployments** → find a working one → **⋯** → **Promote to Production**. Instant, no git needed.

---

## Things you still need to do

### 1. Add the logo

Every page expects `assets/img/peerbridge-logo.png`. Create the folder and drop it in, or the header logo won't load.

### 2. Swap illustrations for real photos, as you get them

Every illustration is hand-coded SVG, drawn in your teal/gold. Nothing is loaded from an external site, so nothing can break or slow the page down. But real photos will beat them once you have any.

**Swapping one for a photo.** Each illustration sits inside a `<div class="illus illus-plain">`. Replace the whole `<svg>…</svg>` with an image tag and drop `illus-plain` (that class removes the white card the photo wants):

```html
<!-- before -->
<div class="illus illus-plain"><svg viewBox="0 0 640 470">…</svg></div>

<!-- after -->
<div class="illus"><img src="assets/img/our-first-event.jpg" alt="Students at our first event"></div>
```

The `.illus` wrapper already rounds the corners, crops to 4:3, and adds the soft shadow. You don't need to resize anything.

**Team photos** work the same way, inside `<div class="face">`:

```html
<div class="face"><img src="assets/img/michael.jpg" alt=""></div>
```

Then delete the "Those are illustrations, not photos" note near the bottom of `team.html`.

If you'd rather change every page at once, edit the SVG constants at the top of `_build.py` and re-run it — see the last section.

### 3. Fix the contact form email

`contact.html` currently posts to `formsubmit.co/anwarkiyar8@gmail.com` — a personal address. Switch it to the org address:

```html
<form ... action="https://formsubmit.co/peerbridgenova@gmail.com" method="POST">
```

FormSubmit sends a one-time confirmation email to the new address; click the link in it or submissions won't deliver.

Also update the email in the footer and on `contact.html` / `stories.html` if `peerbridgenova@gmail.com` isn't the real address.

### 4. Decide your legal structure

`donate.html` currently states — accurately — that PeerBridge isn't accepting donations because it isn't registered. Do not replace that with a Cash App link. Soliciting donations to a personal payment account while presenting as an organization makes that income taxable to the account holder and, in Virginia, publicly soliciting charitable contributions generally requires registration with the Department of Agriculture and Consumer Services first.

The two realistic paths:

- **Fiscal sponsorship** — an existing 501(c)(3) holds funds for you and donations are tax-deductible through them. Weeks, not months. Usually the right move for a first-year student org.
- **Your own 501(c)(3)** — IRS Form 1023-EZ, ~$275, plus state registration. More control, more paperwork, and you need adult signatories.

The roadmap on `donate.html` lays out the steps. Update it as you complete them.

---

## The anti-spam check

Three layers on the contact form, in `script.js`:

1. **Honeypot** — a hidden `_honey` field. Bots fill in every field they find; people never see it. FormSubmit also drops these server-side automatically.
2. **Time trap** — submissions under 4 seconds after page load are rejected.
3. **Arithmetic question** — e.g. "seven + 3 = ?". One operand is spelled out in words so a bot can't just regex the digits.

**Be honest about the limits:** layers 2 and 3 run in the browser, so anyone who POSTs directly to FormSubmit bypasses them. They stop automated form-scrapers, which is the actual threat for a site this size. The honeypot is the only one enforced server-side.

If real spam ever gets through, the one-line fix is in `contact.html`:

```html
<input type="hidden" name="_captcha" value="true">
```

That turns on FormSubmit's own reCAPTCHA. It adds an interstitial page after submit, which is why it's off by default.

---

## Editing the glossary

Terms live in `glossary.html` as a list of blocks:

```html
<div class="term" data-term="Burnout">
  <dt>Burnout</dt>
  <dd>Definition text here.<span class="also">Optional secondary note.</span></dd>
</div>
```

Copy a block, edit it, keep the list **alphabetical** (`data-term` must match the `<dt>`). The A–Z filter builds itself from the entries and automatically greys out letters with no terms — no other file needs touching.

---

## About `_build.py`

The header, nav, and footer are identical on all ten pages. `_build.py` generates every page from one template so those blocks can't drift out of sync.

You do **not** need it. Editing the `.html` files directly works fine. But if you're changing the nav or footer, edit `_build.py` and run `python3 _build.py` — otherwise you have to make the same edit ten times and will inevitably miss one.

**Warning:** running it overwrites all ten HTML files. Any edits you made directly to the HTML will be lost unless you've also made them in `_build.py`.
