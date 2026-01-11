# Frontend Themes

This directory contains multiple frontend designs for the application.

## Structure

Each theme should have the following structure:
```
theme-name/
├── static/
│   ├── css/
│   ├── js/
│   └── images/
└── templates/
```

## Usage

Set the `FRONTEND_THEME` environment variable to the theme name:

```bash
# In .env file
FRONTEND_THEME=theme-name

# Or as environment variable
export FRONTEND_THEME=theme-name
```

If no theme is set, the application runs in API-only mode with no frontend.

## Available Themes

- (No themes created yet)

