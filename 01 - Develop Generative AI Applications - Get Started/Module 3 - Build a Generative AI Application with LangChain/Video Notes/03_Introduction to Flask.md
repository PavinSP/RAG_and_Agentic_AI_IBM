# Video Note: Introduction to Flask

**Video length:** 7 min

## Overview

Defines Flask as a Python micro-framework, covers its origin, its main and additional features, the popular community extensions, how to install it (with a note on version pinning), its five built-in dependencies, and how it compares to Django.

## Learning Objectives

- Define the Flask web framework and describe its main features.
- Explain how to install Flask on your machine.
- Describe the main dependencies of Flask.
- Explain the main differences between Flask and Django.

## What Flask Is

Flask is a **micro-framework** for creating web applications. It is **not opinionated** like some larger frameworks and **does not bind you to a specific set of tools**.

Its one significant dependency is **Python** itself — Flask 2.2.2 requires a minimum of **Python 3.7**.

### Origin

**Armin Ronacher created Flask in 2004 as an April Fool's joke.** It quickly gained popularity for its ease of use and extensibility.

Flask ships with the minimal dependencies you need to build a web application, but it's extensible — many community extensions add further features.

## Main Features

- **Development web server** — runs applications in development mode.
- **Debugger** — shows interactive traceback and stack trace **in the browser**.
- **Logging** — uses standard Python logging for application logs; the same logger works for your own custom messages.
- **Testing** — provides a way to test different parts of your application, enabling a test-driven approach. Works with frameworks like **PyTest** and **coverage**.
- **Request and response objects** — accessible so you can pull arguments out of requests and customize responses.

## Additional Features

- **Static assets** — supports CSS files, JavaScript files, and images, with tags to load static files in templates.
- **Jinja templating** — build dynamic pages that display information which may change per request, or check whether a user is logged in.
- **Routing and dynamic URLs** — extremely useful for RESTful services. You can create routes for different HTTP methods and provide redirection.
- **Global error handlers** — written at the application level.
- **User session management**.

## Popular Community Extensions

- **Flask-SQLAlchemy** — adds the SQLAlchemy ORM, letting you work with database objects in Python.
- **Flask-Mail** — set up an SMTP mail server.
- **Flask-Admin** — add admin interfaces easily.
- **Flask-Uploads** — customized file uploading.
- **Flask-CORS** — handle cross-origin resource sharing, making cross-origin JavaScript requests possible.
- **Flask-Migrate** — adds database migrations to the SQLAlchemy ORM.
- **Flask-User** — user authentication, authorization, and other user management.
- **Marshmallow** — extensive object serialization and deserialization.
- **Celery** — a powerful task queue for simple background tasks through to complex multi-stage programs and schedules.

## Installation

Flask is available via **pip**. When installing on your own machine, it's recommended to **first create a virtual environment** using the `venv` or `pipenv` module.

### Pin your versions

The video emphasizes **pinning the version number** of your dependencies, for two reasons:

1. The application can be **reproduced from scratch** across different environments — development, staging, production.
2. It prevents new issues and bugs being introduced by mistake when packages update automatically.

## Built-in Dependencies

Flask ships with five dependencies that enable its various features:

- **Werkzeug** — implements **WSGI** (Web Server Gateway Interface), the standard Python interface between applications and servers.
- **Jinja** — the template language that renders your application's pages.
- **MarkupSafe** — comes with Jinja; **escapes untrusted input** when rendering templates to avoid injection attacks.
- **ItsDangerous** — signs data securely, so you can tell whether data has been tampered with. Used to protect Flask's **session cookie**.
- **Click** — a framework for writing command-line applications; provides the `flask` command and allows adding custom management commands.

You can see all of these with `pip freeze` inside the virtual environment.

## Flask vs. Django

| | Flask | Django |
|---|---|---|
| **Scope** | Very light framework | Full-stack framework |
| **Dependencies** | Only the basics needed to create a web app; add extensions for more | Includes everything needed for a full-stack application |
| **Flexibility** | Very flexible — add and remove pieces plug-and-play | Opinionated; makes most decisions for you so you can focus on application logic |

## Recap

- Flask is a micro-framework that ships with minimal dependencies.
- Its features include a debugging server, routing, templates, and error handling.
- It can be extended with community extensions.
- It installs as a Python package.
- Django is a full-stack framework by comparison.

## Why This Matters

This video supplies the web-framework half of the module — the LangChain material covers talking to a model, and this covers exposing that to actual users. Several features named here are used directly in the module's lab: the **development server** (`app.run(debug=True)`), **routing** (`@app.route('/generate', methods=['POST'])`), **Jinja templating** (`render_template('index.html')`), **static assets** (`static/script.js` and `static/styles.css`), and **error handling** (returning 400/500 with a JSON body).

The **routing + dynamic URLs for RESTful services** feature is what makes the lab's architecture possible: the browser page never reloads, it just POSTs JSON to `/generate` and gets JSON back. That split — a Jinja-rendered page for humans, a REST endpoint for the JavaScript — is the standard shape for putting an LLM behind a web UI.

Two things worth flagging honestly. The **development server is explicitly for development**, which is exactly what Flask warns about at startup in the lab and why the "From Idea to AI" video's MLOps section (containers, Kubernetes, vLLM) describes the production step this course doesn't take. And **MarkupSafe's auto-escaping** matters more than it sounds when LLM output is being rendered: model-generated text is untrusted input, so escaping it before it reaches the page is what stops generated content from becoming an injection vector.
