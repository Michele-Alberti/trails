## v1.0.0 (2022-05-22)

### Feat

- **README.md**: force major version change

## v0.5.0 (2022-05-22)

### Feat

- **models.py**: add cascade deletion on database

### Fix

- **server/development.yaml**: fix error on host address

## v0.4.1 (2022-05-21)

### Fix

- **server/production.yaml**: fix error on host address

## v0.4.0 (2022-05-21)

### Fix

- **models.py**: change username uniqueness to false

### Feat

- add favicon
- add credits modal window
- **trails_cli.py**: add example user during database initialization
- improve graphics and responsive design

### Refactor

- **main.py**: improve how icons names are displayed

## v0.3.0 (2022-05-15)

### Feat

- change the existing web app theme

### Refactor

- update web app style

## v0.2.1 (2022-05-12)

### Fix

- **__init__.py**: fix an error caused by old postgres uri

## v0.2.0 (2022-05-12)

### Feat

- update flask configurations for supporting both sqlite and postgresql
- **trails_cli.py**: add support for postgres
- add support for postgresql and improve configuration handling

### Fix

- **__main__.py**: fix error on server configuration
- change method of delete actions from GET to POST

### Refactor

- **import-click**: change 'db init' and 'db delete' to be database agnostic
- **flash_message_modal_window.html**: renamed to flash-message-modal-window.html
- **flash_message_modal_window.html**: renamed to flash-message-modal-window.html

## v0.1.0 (2022-05-08)

### Feat

- add modal window for flash messages
- add interface for adding items to trails
- **style.css**: update style.css
- add loggers to backend
- add support for hydra framework
- add features to html templates
- **main.py**: add routes to main pages
- **__init__.py**: add CSRF protection

### Fix

- **main.py**: add check for trail existence in trail function
- fix error in links for post url and stylesheets
- fix the cli used for interaction with debug database
- fix bug on login and signup forms
- **models.py**: add non-empty constrain to several columns in database tables

### Refactor

- **navbar**: move javascript from base.html to a dedicated file
- **auth.py**: add log
- add x symbol to delete button in profile page
- change folder name from trails-bulma to bulma

## v0.0.1 (2022-05-08)
