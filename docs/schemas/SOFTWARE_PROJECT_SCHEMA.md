# Software Project Schema for AMG (Graphiti)

This document defines a comprehensive schema for tracking software projects within the AMG (Agent Memory Graph) system. The schema is optimized for AI agents that need to understand, navigate, and reason about software codebases.

## Overview

The Software Project Schema extends Graphiti's entity and relationship model to support:
- **Project Structure**: Components, modules, features, and their hierarchies
- **Development Lifecycle**: Issues, releases, commits, and pull requests
- **Team Dynamics**: Contributors, roles, and responsibilities
- **Technical Details**: APIs, data models, integrations, and configurations

---

## Entity Types

### Core Project Entities

#### `software_project`
The root entity representing a software application or repository.

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `name` | string | Project name | Yes |
| `repo_url` | string | Repository URL (GitHub, GitLab, etc.) | No |
| `language` | string | Primary programming language | No |
| `framework` | string | Main framework (React, Django, etc.) | No |
| `version` | string | Current version | No |
| `status` | enum | `active`, `maintenance`, `deprecated`, `archived` | No |
| `description` | string | Brief project description | No |
| `license` | string | License type (MIT, Apache, etc.) | No |

**Example:**
```json
{
  "name": "AgentForge",
  "entity_type": "software_project",
  "metadata": {
    "repo_url": "https://github.com/example/agent-forge",
    "language": "TypeScript",
    "framework": "Next.js",
    "version": "0.5.0",
    "status": "active"
  }
}
```

---

#### `feature`
A major capability or functional area of the project.

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `name` | string | Feature name | Yes |
| `status` | enum | `planned`, `in_progress`, `completed`, `deprecated` | No |
| `priority` | enum | `critical`, `high`, `medium`, `low` | No |
| `release_version` | string | Version where feature was/will be released | No |
| `description` | string | Feature description | No |

**Example:**
```json
{
  "name": "Workflow Builder",
  "entity_type": "feature",
  "metadata": {
    "status": "completed",
    "priority": "high",
    "release_version": "0.3.0",
    "description": "Visual drag-and-drop workflow creation interface"
  }
}
```

---

#### `component`
An architectural component, service, or module within the project.

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `name` | string | Component name | Yes |
| `type` | enum | `service`, `module`, `library`, `package`, `plugin` | No |
| `path` | string | File system path | No |
| `language` | string | Implementation language | No |
| `dependencies` | array | List of dependency names | No |
| `description` | string | Component purpose | No |

**Example:**
```json
{
  "name": "MCP Server",
  "entity_type": "component",
  "metadata": {
    "type": "service",
    "path": "mcp_server/",
    "language": "Python",
    "dependencies": ["graphiti_core", "fastapi"]
  }
}
```

---

#### `api_endpoint`
A REST, GraphQL, or other API endpoint.

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `name` | string | Endpoint identifier | Yes |
| `method` | enum | `GET`, `POST`, `PUT`, `PATCH`, `DELETE` | No |
| `path` | string | URL path (e.g., `/api/v1/users`) | Yes |
| `auth_required` | boolean | Whether authentication is required | No |
| `request_schema` | object | Expected request body structure | No |
| `response_schema` | object | Response body structure | No |
| `description` | string | Endpoint purpose | No |

**Example:**
```json
{
  "name": "Create Episode",
  "entity_type": "api_endpoint",
  "metadata": {
    "method": "POST",
    "path": "/api/v1/episodes",
    "auth_required": true,
    "description": "Add a new episode to the knowledge graph"
  }
}
```

---

#### `data_model`
A database table, schema, or data structure.

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `name` | string | Model/table name | Yes |
| `storage_type` | enum | `sql`, `nosql`, `graph`, `file`, `memory` | No |
| `fields` | object | Field definitions | No |
| `indexes` | array | Index definitions | No |
| `description` | string | Model purpose | No |

**Example:**
```json
{
  "name": "EntityNode",
  "entity_type": "data_model",
  "metadata": {
    "storage_type": "graph",
    "fields": {
      "uuid": "string",
      "name": "string",
      "entity_type": "string",
      "summary": "string",
      "created_at": "datetime"
    }
  }
}
```

---

#### `integration`
An external service or API integration.

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `name` | string | Integration name | Yes |
| `service_name` | string | External service (e.g., "OpenAI", "Neo4j") | Yes |
| `auth_type` | enum | `api_key`, `oauth2`, `basic`, `none` | No |
| `status` | enum | `active`, `deprecated`, `planned` | No |
| `config_keys` | array | Required environment variables | No |
| `description` | string | Integration purpose | No |

**Example:**
```json
{
  "name": "OpenAI LLM Provider",
  "entity_type": "integration",
  "metadata": {
    "service_name": "OpenAI",
    "auth_type": "api_key",
    "status": "active",
    "config_keys": ["OPENAI_API_KEY"]
  }
}
```

---

#### `configuration`
A configuration option or environment variable.

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `name` | string | Config key name | Yes |
| `default_value` | any | Default value if not set | No |
| `required` | boolean | Whether the config is required | No |
| `scope` | enum | `global`, `component`, `environment` | No |
| `sensitive` | boolean | Whether value should be treated as secret | No |
| `description` | string | Config purpose | No |

**Example:**
```json
{
  "name": "SEMAPHORE_LIMIT",
  "entity_type": "configuration",
  "metadata": {
    "default_value": 10,
    "required": false,
    "scope": "global",
    "sensitive": false,
    "description": "Controls concurrency for LLM operations"
  }
}
```

---

### Development Lifecycle Entities

#### `release`
A version release of the project.

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `name` | string | Release name/tag | Yes |
| `version` | string | Semantic version | Yes |
| `date` | datetime | Release date | No |
| `changelog` | string | Release notes | No |
| `breaking_changes` | boolean | Contains breaking changes | No |

---

#### `issue`
A bug report, feature request, or task.

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `name` | string | Issue title | Yes |
| `issue_number` | integer | Issue ID/number | No |
| `status` | enum | `open`, `in_progress`, `closed`, `wontfix` | No |
| `priority` | enum | `critical`, `high`, `medium`, `low` | No |
| `labels` | array | Issue labels/tags | No |
| `assignee` | string | Assigned developer | No |

---

#### `pull_request`
A code change request.

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `name` | string | PR title | Yes |
| `pr_number` | integer | PR ID/number | No |
| `status` | enum | `draft`, `open`, `merged`, `closed` | No |
| `source_branch` | string | Source branch name | No |
| `target_branch` | string | Target branch name | No |
| `author` | string | PR author | No |

---

### Team Entities

#### `developer`
A project contributor.

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `name` | string | Developer name | Yes |
| `github_handle` | string | GitHub username | No |
| `role` | enum | `maintainer`, `contributor`, `reviewer` | No |
| `expertise` | array | Areas of expertise | No |
| `email` | string | Contact email | No |

---

#### `team`
A group of developers.

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `name` | string | Team name | Yes |
| `focus_area` | string | Team's primary focus | No |
| `lead` | string | Team lead name | No |

---

## Relationship Types

Relationships connect entities and carry semantic meaning with temporal awareness.

### Project Structure Relationships

| Relationship | Source | Target | Description |
|--------------|--------|--------|-------------|
| `has_feature` | software_project | feature | Project contains feature |
| `has_component` | software_project | component | Project contains component |
| `contains` | component | component | Component contains sub-component |
| `depends_on` | component | component | Component depends on another |
| `implements` | component | feature | Component implements feature |

### API & Data Relationships

| Relationship | Source | Target | Description |
|--------------|--------|--------|-------------|
| `exposes` | component | api_endpoint | Component exposes endpoint |
| `uses_model` | component | data_model | Component uses data model |
| `calls` | api_endpoint | api_endpoint | Endpoint calls another |
| `stores_in` | data_model | integration | Model stored in service |

### Integration Relationships

| Relationship | Source | Target | Description |
|--------------|--------|--------|-------------|
| `integrates_with` | software_project | integration | Project uses integration |
| `requires_config` | integration | configuration | Integration needs config |
| `provides` | integration | feature | Integration enables feature |

### Development Lifecycle Relationships

| Relationship | Source | Target | Description |
|--------------|--------|--------|-------------|
| `implemented_in` | feature | release | Feature released in version |
| `fixes` | pull_request | issue | PR fixes issue |
| `addresses` | release | issue | Release addresses issue |
| `blocks` | issue | issue | Issue blocks another |
| `related_to` | issue | issue | Issues are related |

### Team Relationships

| Relationship | Source | Target | Description |
|--------------|--------|--------|-------------|
| `contributed_by` | component | developer | Developer built component |
| `maintains` | developer | component | Developer maintains component |
| `member_of` | developer | team | Developer belongs to team |
| `owns` | team | component | Team owns component |
| `reviewed_by` | pull_request | developer | Developer reviewed PR |
| `authored_by` | pull_request | developer | Developer authored PR |

---

## Usage Examples

### Adding a Software Project

```python
from graphiti_core import Graphiti

# Initialize Graphiti
graphiti = Graphiti(neo4j_uri, neo4j_user, neo4j_password)

# Add project entity
await graphiti.add_entity(
    name="AgentForge",
    entity_type="software_project",
    summary="AI agent workflow automation platform",
    metadata={
        "repo_url": "https://github.com/example/agent-forge",
        "language": "TypeScript",
        "framework": "Next.js",
        "status": "active"
    }
)
```

### Adding Components with Relationships

```python
# Add component
await graphiti.add_entity(
    name="Workflow Engine",
    entity_type="component",
    summary="Core execution engine for agent workflows",
    metadata={
        "type": "module",
        "path": "src/engine/",
        "language": "TypeScript"
    }
)

# Add relationship
await graphiti.add_relationship(
    source_entity="AgentForge",
    target_entity="Workflow Engine",
    relationship_type="has_component",
    fact="AgentForge contains the Workflow Engine as a core component"
)
```

### Querying Project Structure

```python
# Search for all components
results = await graphiti.search(
    query="components of AgentForge",
    search_type="hybrid"
)

# Get full context
context = await graphiti.get_context(
    query="AgentForge architecture",
    depth=2
)
```

---

## Best Practices

### 1. Hierarchical Organization
Structure entities from general to specific:
```
software_project → component → api_endpoint
                 → feature → release
```

### 2. Temporal Tracking
Use episodes for time-sensitive events:
- Commits and merges
- Deployments
- Incident responses

### 3. Relationship Granularity
Create relationships at the right level:
- **Too broad**: "AgentForge uses databases"
- **Just right**: "UserService stores data in PostgreSQL users table"

### 4. Metadata Consistency
Use consistent values for enum fields across all entities.

### 5. Regular Updates
Keep the graph current with:
- New releases
- Dependency changes
- Team membership changes

---

## Schema Validation (Optional)

For strict validation, use Pydantic models:

```python
from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

class ProjectStatus(str, Enum):
    ACTIVE = "active"
    MAINTENANCE = "maintenance"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"

class SoftwareProject(BaseModel):
    name: str
    repo_url: Optional[str] = None
    language: Optional[str] = None
    framework: Optional[str] = None
    version: Optional[str] = None
    status: Optional[ProjectStatus] = ProjectStatus.ACTIVE
    description: Optional[str] = None
    license: Optional[str] = None
```

---

## Next Steps

1. **Implement custom entity types** in your Graphiti instance
2. **Create ingestion pipelines** for your repository data
3. **Build search templates** for common queries
4. **Set up automated updates** via CI/CD webhooks

For more information, see the main [Graphiti documentation](../README.md).
