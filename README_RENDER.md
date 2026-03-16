# HOL Optical ERP - GitHub + Render Package

This cleaned package is prepared for online deployment only.

## What was removed
- Python cache folders (`__pycache__`)
- compiled `.pyc` files
- local virtual environment files
- offline/PWA service worker files
- manifest route usage
- public `/seed` route
- local upload leftovers

## GitHub upload steps
1. Extract the ZIP.
2. Open the `hol_v8_offline_appointments` folder.
3. Upload all contents of that folder to a new GitHub repository.

## Render deployment steps
1. In Render, choose **New > Blueprint**.
2. Connect the GitHub repository.
3. Render will read `render.yaml` and create:
   - one web service
   - one PostgreSQL database
4. Deploy.

## Default login after database setup
You still need to create tables and seed initial data.
Use the Render shell or local terminal:

```bash
python seed.py
```

## Notes
- `render.yaml` uses `gunicorn run:app`
- `DATABASE_URL` is supplied automatically by Render
- `runtime.txt` pins Python 3.11.9 for cleaner builds
