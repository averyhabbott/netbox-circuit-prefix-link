# netbox-circuit-prefix-link

A NetBox plugin that links Circuits to Prefixes.

- One Circuit can have many linked Prefixes.
- Each Prefix can be linked to at most one Circuit.
- The link is surfaced as a panel on Circuit, Prefix, and IPAddress detail pages.

Compatible with **NetBox 4.5.x** and **NetBox 4.6.x**.

## Install

```bash
pip install netbox-circuit-prefix-link
```

Then in your NetBox `configuration.py`:

```python
PLUGINS = [
    'netbox_circuit_prefix_link',
]
```

Run migrations:

```bash
python manage.py migrate netbox_circuit_prefix_link
```

## REST API

Endpoint: `/api/plugins/circuit-prefix-link/circuit-prefixes/`

Supports the standard NetBox CRUD plus filtering by `circuit_id` and `prefix_id`.

## UI

- **Circuit detail page** — "Linked Prefixes" panel with an Add Prefix button.
- **Prefix detail page** — "Circuit Link" panel showing the associated Circuit (if any), with Link / Edit / Unlink buttons.
- **IPAddress detail page** — Read-only panel showing the Circuit of any parent Prefix that has a link.

## Permissions

Standard Django/NetBox model permissions:

- `netbox_circuit_prefix_link.view_circuitprefix`
- `netbox_circuit_prefix_link.add_circuitprefix`
- `netbox_circuit_prefix_link.change_circuitprefix`
- `netbox_circuit_prefix_link.delete_circuitprefix`

Panel content is filtered with NetBox's object-permission `restrict()` — users only see Circuits and Prefixes they have view permission on.
