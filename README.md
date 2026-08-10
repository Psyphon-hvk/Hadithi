# HADITHI Toolkit

A digital toolkit supporting frontline healthcare workers through learning,
storytelling, peer support and wellbeing — built with **Django** and
**Tailwind CSS**, following the 4-phase roadmap:

- **Phase 1 — Foundation & Core Platform**: custom user model with healthcare
  cadre roles, authentication, dashboard, profile management, admin portal.
  (`accounts`, `core`)
- **Phase 2 — Learning & Wellness Hub**: resource categories, articles,
  videos, podcasts, PDF guides, FAQs, search/filter, bookmarks.
  (`resources`)
- **Phase 3 — Community & Wellbeing**: HADITHI Stories (anonymous or named),
  peer support discussions, self-assessments (PHQ-9, GAD-7, burnout),
  personal results/recommendations, wellness toolkit (journaling, breathing,
  mindfulness). (`community`, `wellness`)
- **Phase 4 — Deployment, Administration & Growth**: events/webinars,
  engagement analytics snapshots, admin management for all content types.
  (`events`)

## Project layout

```
hadithi_toolkit/
├── accounts/          # Phase 1: custom User model, auth, profile
├── core/               # Phase 1: home page, dashboard, seed_demo_data command
├── resources/          # Phase 2: learning & wellness hub
├── community/          # Phase 3: stories, peer discussions, assessments
├── wellness/           # Phase 3: journaling, breathing, mindfulness
├── events/             # Phase 4: events/webinars, analytics snapshots
├── templates/base.html # Shared layout (Tailwind via CDN)
└── manage.py
```

## Getting started

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py seed_demo_data   # optional: creates demo admin + sample content
python manage.py runserver
```

Visit http://127.0.0.1:8000/

Demo accounts created by `seed_demo_data` (change these before any real deployment):

- Superuser: `admin` / `hadithi-demo-2026`
- Demo user: `demo_nurse` / `hadithi-demo-2026`

## Notes on this scaffold

- Tailwind is loaded via CDN in `templates/base.html` for zero-build simplicity.
  For a production build, swap this for `django-tailwind` or a proper
  Tailwind CLI/PostCSS pipeline (per the roadmap's VS Code + Tailwind setup).
- SQLite is used by default; swap `DATABASES` in `settings.py` for
  Postgres/MySQL in production.
- `SECRET_KEY` and `DEBUG` in `settings.py` must be changed/hardened before
  deployment (Phase 4: Production deployment).
- Self-assessment scoring in `community/views.py` uses simple threshold
  bands as a starting point — replace with clinically validated PHQ-9/GAD-7
  scoring logic before real-world use.
- Analytics/aggregated dashboards (`events.PlatformEngagementSnapshot`) are
  modeled but not yet populated by a scheduled job — add a management
  command or Celery task to compute daily snapshots.
- Suggested build order from the roadmap doc is preserved: finish Phase 1
  hardening, then iterate through Phases 2–4 module by module.
