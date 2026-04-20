# Sponsors Integration Plan - TODO

## Information Gathered:
- static/images/Sponsors/: 24 JPGs (IMG-20260416-WA0002.jpg to WA0025.jpg).
- main/templates/index.html: Sponsors marquee with 24 placeholders matching names: NASENI, NOTAP, FUTA, UNILAG, ABU, NITDA, BUA, DANGOTE, MTN, SHELL, NNPC, CBN (row1); BOI, AFDB, UNESCO, WORLDBANK, GIZ, UKAID, FCMB, ACCESSBANK, FLUTTERWAVE, PAYSTACK, CCHUB, VENTURESPLATFORM (row2).
- User confirmed names match images sequentially.

## Plan:
1. [x] Rename images:
   - cd static/images/Sponsors && ren "IMG-20260416-WA0002.jpg" "naseni.jpg"
   - ... ren "IMG-20260416-WA0025.jpg" "venturesplatform.jpg"
2. [x] Update main/templates/index.html: Replace all 48 .logo-icon divs with <img src="{% static 'images/Sponsors/naseni.jpg' %}" alt="NASENI Logo" class="w-9 h-9 object-contain rounded"> (24 unique + 24 duplicates).
3. [x] Ensure {% load static %} present (yes).

## Dependent Files:
- static/images/Sponsors/*.jpg (rename).
- main/templates/index.html (replace placeholders).

## Followup:
- Execute rename commands.
- Edit HTML.
- Test: python manage.py collectstatic && python manage.py runserver

Current: Planning confirmed, ready for execution.

