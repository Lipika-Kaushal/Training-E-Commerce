# Training E-Commerce

## Run the web storefront

Install the web dependencies, then start the local storefront from the project folder:

```powershell
python -m pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000 in your browser. The demo accounts are `u1` through
`u5`; each uses the password `p123`.

The storefront includes sign-in, product browsing, a session-based shopping bag,
quantity updates, checkout, and order confirmation. The existing console
application is still available with `python main.py`.

The SQLite database is `ecommerce.db` in the project folder. Startup creates the
required tables and adds any missing demo accounts and products without deleting
existing records. For a deployment beyond local development, set a persistent,
random `FLASK_SECRET_KEY` environment variable before starting the app.

## Deploy to Azure App Service (Linux)

Use a Python App Service and deploy the repository root. Set these **App
Settings** in the Azure portal:

- `SCM_DO_BUILD_DURING_DEPLOYMENT` = `true`
- `FLASK_SECRET_KEY` = a long, random value kept private
- `DATABASE_PATH` = `/home/data/ecommerce.db`

In **Configuration → General settings → Startup Command**, set:

```text
gunicorn --bind=0.0.0.0 --timeout 600 app:app
```

The WSGI app initializes the database when it is loaded by Gunicorn. The
database path setting keeps SQLite data under App Service's persistent `/home`
storage rather than the deployed application files. SQLite is suitable for a
small, single-instance demo; use a managed database for multi-instance
production deployments.
