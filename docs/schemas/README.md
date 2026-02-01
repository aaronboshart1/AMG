# AMG Schema Extensions

This directory contains schema definitions and documentation for extending AMG (Graphiti) to support various domain-specific use cases.

## Available Schemas

### Software Project Schema

A comprehensive schema for tracking software projects, their components, features, and development lifecycle.

**Files:**
- [`SOFTWARE_PROJECT_SCHEMA.md`](./SOFTWARE_PROJECT_SCHEMA.md) - Full documentation with entity types, relationships, and usage examples
- [`software_project_schema.json`](./software_project_schema.json) - JSON Schema definition for validation
- [`examples/agentforge_example.py`](./examples/agentforge_example.py) - Python example showing how to populate AMG with project data

**Use Cases:**
- AI agents that need to understand codebases
- Development tracking and project management
- Automated documentation generation
- Code archaeology and knowledge management

## Schema Design Principles

### 1. Entity Types

Each schema defines custom entity types that extend Graphiti's base `EntityNode`. Entity types include:
- A unique type identifier (e.g., `software_project`, `feature`)
- Required and optional metadata fields
- Field types and validation rules

### 2. Relationship Types

Relationships connect entities with semantic meaning:
- Defined source and target entity types
- Clear relationship semantics (e.g., `has_feature`, `depends_on`)
- Support for temporal tracking (valid_from, valid_to)

### 3. Temporal Awareness

All schemas leverage Graphiti's bi-temporal model:
- **Event time**: When something actually happened
- **Ingestion time**: When the knowledge was added
- Historical queries supported out of the box

## Creating Custom Schemas

To create your own domain schema:

1. **Define Entity Types**
   ```python
   # Identify the core "things" in your domain
   entity_types = [
       "customer",
       "product", 
       "order",
       "support_ticket"
   ]
   ```

2. **Define Relationships**
   ```python
   # Map how entities connect
   relationships = [
       ("customer", "placed", "order"),
       ("order", "contains", "product"),
       ("customer", "opened", "support_ticket")
   ]
   ```

3. **Specify Metadata**
   ```python
   # Add domain-specific attributes
   customer_metadata = {
       "tier": ["free", "pro", "enterprise"],
       "signup_date": "datetime",
       "lifetime_value": "float"
   }
   ```

4. **Document and Validate**
   - Create a markdown documentation file
   - Create a JSON Schema for validation
   - Provide example code

## Contributing Schemas

We welcome contributions of new domain schemas! Please:

1. Follow the existing structure (docs, JSON schema, examples)
2. Include comprehensive documentation
3. Provide working example code
4. Add tests if possible

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for general contribution guidelines.

## Related Documentation

- [Main Graphiti README](../../README.md)
- [API Documentation](../../server/README.md)
- [MCP Server](../../mcp_server/README.md)
