# TODO: Setup Aiven MySQL and Deploy to Render

## Steps to Complete:
- [ ] Sign up for Aiven account and create a free MySQL service
- [ ] Obtain database connection details (host, port, database name, username, password)
- [ ] Update requirements.txt to include mysqlclient (already done)
- [ ] Modify exam_form_system/settings.py to use MySQL with environment variables (prepared)
- [ ] Update render.yaml to include MySQL environment variables (prepared)
- [ ] Test database connection locally
- [ ] Run migrations to transfer data from SQLite to MySQL
- [ ] Deploy to Render and verify connection
- [ ] Test application functionality on Render

## Notes:
- Aiven free tier: 1GB storage, 5GB traffic/month, may require card verification.
- Use environment variables for security.
- Ensure SSL connection for Aiven.
- Backup SQLite data before migration.
- Data backed up to backup.json
