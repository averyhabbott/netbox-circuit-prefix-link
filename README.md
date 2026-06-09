# netbox-circuit-prefix-link

A NetBox plugin that links Circuits to Prefixes.

- One Circuit can have many linked Prefixes.
- Each Prefix can be linked to at most one Circuit.
- The link is surfaced as a panel on Circuit, Prefix, and IPAddress detail pages.

Compatible with **NetBox 4.5.x** and **NetBox 4.6.x**. Requires **Python 3.12+**.

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

## Configuration

You can control which columns appear in the **Circuit** and **Prefix** detail-page panels via
`PLUGINS_CONFIG` in your NetBox `configuration.py`. Each panel takes a flat, ordered list of
field names:

```python
PLUGINS_CONFIG = {
    'netbox_circuit_prefix_link': {
        'circuit_panel': ['description', 'utilization'],   # columns in the "Linked Prefixes" table
        'prefix_panel':  ['provider', 'type'],             # rows in the "Circuit Link" panel
    },
}
```

Notes:

- **Defaults** (used when a key is omitted): `circuit_panel` → `['description', 'utilization']`;
  `prefix_panel` → `['provider', 'type']`.
- The identifying link is **always shown first**: the prefix on the Circuit panel, the Circuit
  on the Prefix panel — you do not list it.
- On the Circuit panel, the per-row **edit/unlink actions** are always shown last and are
  automatically hidden for users without change/delete permission.
- **Unknown field names are ignored** (and a warning is logged), so a typo won't break the page.
- Columns render in the order listed.

### Available columns — Circuit panel (`circuit_panel`)

Each resolves from the linked Prefix:

| Name | Renders |
|------|---------|
| `description` | The prefix's description |
| `utilization` | Colored usage bar (`get_utilization()`) |
| `status` | Colored status badge |
| `vlan` | Assigned VLAN (linkified) |
| `vrf` | VRF (linkified) |
| `tenant` | Tenant (linkified) |
| `role` | Prefix role (linkified) |

### Available columns — Prefix panel (`prefix_panel`)

Each resolves from the linked Circuit:

| Name | Renders |
|------|---------|
| `provider` | Circuit provider (linkified) |
| `provider_account` | Provider account (linkified) |
| `type` | Circuit type (linkified) |
| `status` | Colored status badge |
| `tenant` | Tenant (linkified) |
| `install_date` | Install date |
| `termination_date` | Termination date |
| `commit_rate` | Commit rate (Kbps) |
| `description` | Circuit description |

## REST API

Endpoint: `/api/plugins/circuit-prefix-link/circuit-prefixes/`

Supports the standard NetBox CRUD plus filtering by `circuit_id` and `prefix_id`.

## UI

- **Circuit detail page** — "Linked Prefixes" panel with an Add Prefix button.
- **Prefix detail page** — "Circuit Link" panel showing the associated Circuit (if any), with Link / Edit / Unlink buttons.
- **IPAddress detail page** — Read-only panel showing the Circuit of any parent Prefix that has a link.
- **Circuits list view** — opt-in "Linked Prefixes" column showing the linked prefixes as a comma-separated list of links. Enable it via the table configuration (gear icon) → add **Linked Prefixes** under Selected Columns.

## Permissions

Standard Django/NetBox model permissions:

- `netbox_circuit_prefix_link.view_circuitprefix`
- `netbox_circuit_prefix_link.add_circuitprefix`
- `netbox_circuit_prefix_link.change_circuitprefix`
- `netbox_circuit_prefix_link.delete_circuitprefix`

Panel content is filtered with NetBox's object-permission `restrict()` — users only see Circuits and Prefixes they have view permission on.
