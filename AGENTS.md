# Project guidance

Build this AI personal assistant incrementally for a teaching cohort.

- Keep email/calendar provider details behind `app/services/nylas_service.py`.
- Keep one-time Nylas setup scripts under `app/config/`.
- Keep webhook handling, schemas, service operations, and UI templates separate.
- Use canonical schemas instead of passing provider payloads throughout the app.
- Store raw events before asynchronous processing when that behavior is implemented.
- Require user confirmation before consequential actions such as sending email or changing a calendar.
- Never commit credentials or personal email content.
