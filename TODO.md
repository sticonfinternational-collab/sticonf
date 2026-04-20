# Render Deployment TODO

## Planning Steps (Approved)
- [x] Create TODO.md

## Implementation Steps
- [x] 1. Create Procfile
- [x] 2. Create runtime.txt  
- [x] 3. Update requirements.txt (add gunicorn, whitenoise, psycopg2-binary, dj-database-url)
- [x] 4. Create .env.example
- [x] 5. Create/update .gitignore
- [x] 6. Update sticonf/settings.py (SECRET_KEY, DEBUG, ALLOWED_HOSTS, Whitenoise middleware, DATABASES with dj-database-url, STATICFILES_STORAGE)
- [ ] 7. Test locally: pip install -r requirements.txt, collectstatic, runserver
- [x] 8. Git commit/push instructions (in TODO)
- [x] 9. Render deployment instructions (in TODO)

## Post-deployment
- [ ] Set env vars on Render
- [ ] Run migrations
