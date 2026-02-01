"""
Example: Populating AMG with Software Project Data

This example demonstrates how to use the Software Project Schema
to track a project like AgentForge in the AMG knowledge graph.
"""

import asyncio
from datetime import datetime
from typing import Optional

# Assuming graphiti_core is installed
# from graphiti_core import Graphiti


# =============================================================================
# Entity Definitions (Pydantic Models for Validation)
# =============================================================================

from pydantic import BaseModel, Field
from enum import Enum


class ProjectStatus(str, Enum):
    ACTIVE = "active"
    MAINTENANCE = "maintenance"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"


class FeatureStatus(str, Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    DEPRECATED = "deprecated"


class Priority(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ComponentType(str, Enum):
    SERVICE = "service"
    MODULE = "module"
    LIBRARY = "library"
    PACKAGE = "package"
    PLUGIN = "plugin"


class SoftwareProject(BaseModel):
    """Root entity for a software project."""
    name: str
    repo_url: Optional[str] = None
    language: Optional[str] = None
    framework: Optional[str] = None
    version: Optional[str] = None
    status: ProjectStatus = ProjectStatus.ACTIVE
    description: Optional[str] = None
    license: Optional[str] = None


class Feature(BaseModel):
    """A major capability or functional area."""
    name: str
    status: FeatureStatus = FeatureStatus.PLANNED
    priority: Optional[Priority] = None
    release_version: Optional[str] = None
    description: Optional[str] = None


class Component(BaseModel):
    """An architectural component, service, or module."""
    name: str
    type: Optional[ComponentType] = None
    path: Optional[str] = None
    language: Optional[str] = None
    dependencies: list[str] = Field(default_factory=list)
    description: Optional[str] = None


# =============================================================================
# Example Data for AgentForge
# =============================================================================

AGENTFORGE_PROJECT = SoftwareProject(
    name="AgentForge",
    repo_url="https://github.com/example/agent-forge",
    language="TypeScript",
    framework="Next.js",
    version="0.5.0",
    status=ProjectStatus.ACTIVE,
    description="AI agent workflow automation platform with visual builder",
    license="MIT"
)

AGENTFORGE_FEATURES = [
    Feature(
        name="Workflow Builder",
        status=FeatureStatus.COMPLETED,
        priority=Priority.HIGH,
        release_version="0.3.0",
        description="Visual drag-and-drop workflow creation interface"
    ),
    Feature(
        name="Feed System",
        status=FeatureStatus.COMPLETED,
        priority=Priority.MEDIUM,
        release_version="0.4.0",
        description="Real-time activity feed for agent events"
    ),
    Feature(
        name="Knowledge Graph Integration",
        status=FeatureStatus.IN_PROGRESS,
        priority=Priority.HIGH,
        description="Integration with AMG for persistent agent memory"
    ),
    Feature(
        name="Multi-Agent Orchestration",
        status=FeatureStatus.PLANNED,
        priority=Priority.CRITICAL,
        description="Coordinate multiple AI agents in complex workflows"
    ),
]

AGENTFORGE_COMPONENTS = [
    Component(
        name="Frontend App",
        type=ComponentType.MODULE,
        path="src/app/",
        language="TypeScript",
        dependencies=["React", "Next.js", "TailwindCSS"],
        description="Next.js frontend application"
    ),
    Component(
        name="API Routes",
        type=ComponentType.SERVICE,
        path="src/app/api/",
        language="TypeScript",
        dependencies=["Next.js", "Prisma"],
        description="Backend API endpoints"
    ),
    Component(
        name="Workflow Engine",
        type=ComponentType.MODULE,
        path="src/engine/",
        language="TypeScript",
        dependencies=["LangChain", "OpenAI"],
        description="Core execution engine for agent workflows"
    ),
    Component(
        name="MCP Integration",
        type=ComponentType.LIBRARY,
        path="src/lib/mcp/",
        language="TypeScript",
        dependencies=["@modelcontextprotocol/sdk"],
        description="Model Context Protocol integration layer"
    ),
]


# =============================================================================
# Functions to Populate AMG
# =============================================================================

async def populate_project(graphiti, project: SoftwareProject):
    """Add a software project to the knowledge graph."""
    await graphiti.add_entity(
        name=project.name,
        entity_type="software_project",
        summary=project.description,
        metadata=project.model_dump(exclude_none=True)
    )
    print(f"✅ Added project: {project.name}")


async def populate_features(graphiti, project_name: str, features: list[Feature]):
    """Add features and link them to the project."""
    for feature in features:
        # Add feature entity
        await graphiti.add_entity(
            name=feature.name,
            entity_type="feature",
            summary=feature.description,
            metadata=feature.model_dump(exclude_none=True)
        )
        
        # Create relationship to project
        await graphiti.add_relationship(
            source_entity=project_name,
            target_entity=feature.name,
            relationship_type="has_feature",
            fact=f"{project_name} includes the {feature.name} feature"
        )
        print(f"  ✅ Added feature: {feature.name}")


async def populate_components(graphiti, project_name: str, components: list[Component]):
    """Add components and link them to the project."""
    for component in components:
        # Add component entity
        await graphiti.add_entity(
            name=component.name,
            entity_type="component",
            summary=component.description,
            metadata=component.model_dump(exclude_none=True)
        )
        
        # Create relationship to project
        await graphiti.add_relationship(
            source_entity=project_name,
            target_entity=component.name,
            relationship_type="has_component",
            fact=f"{project_name} contains the {component.name} component"
        )
        print(f"  ✅ Added component: {component.name}")


async def add_component_dependencies(graphiti, components: list[Component]):
    """Create dependency relationships between components."""
    component_names = {c.name for c in components}
    
    for component in components:
        for dep in component.dependencies:
            # Only create internal dependency relationships
            if dep in component_names:
                await graphiti.add_relationship(
                    source_entity=component.name,
                    target_entity=dep,
                    relationship_type="depends_on",
                    fact=f"{component.name} depends on {dep}"
                )
                print(f"  🔗 {component.name} → depends_on → {dep}")


# =============================================================================
# Main Execution
# =============================================================================

async def main():
    """
    Main function to populate AMG with AgentForge data.
    
    Note: This is a demonstration. In production, you would:
    1. Initialize Graphiti with your Neo4j credentials
    2. Call the setup methods
    3. Handle errors appropriately
    """
    
    print("="*60)
    print("Software Project Schema - AgentForge Example")
    print("="*60)
    print()
    
    # In production, uncomment and configure:
    # graphiti = Graphiti(
    #     neo4j_uri="bolt://localhost:7687",
    #     neo4j_user="neo4j",
    #     neo4j_password="password"
    # )
    # await graphiti.build_indices_and_constraints()
    
    print("📦 Project Definition:")
    print(f"   Name: {AGENTFORGE_PROJECT.name}")
    print(f"   Language: {AGENTFORGE_PROJECT.language}")
    print(f"   Framework: {AGENTFORGE_PROJECT.framework}")
    print(f"   Version: {AGENTFORGE_PROJECT.version}")
    print()
    
    print("🎯 Features:")
    for f in AGENTFORGE_FEATURES:
        status_emoji = {
            FeatureStatus.COMPLETED: "✅",
            FeatureStatus.IN_PROGRESS: "🚧",
            FeatureStatus.PLANNED: "📋",
            FeatureStatus.DEPRECATED: "⚠️"
        }.get(f.status, "❓")
        print(f"   {status_emoji} {f.name} ({f.status.value})")
    print()
    
    print("🧩 Components:")
    for c in AGENTFORGE_COMPONENTS:
        print(f"   📁 {c.name} ({c.type.value if c.type else 'unknown'})")
        print(f"      Path: {c.path}")
        print(f"      Dependencies: {', '.join(c.dependencies)}")
    print()
    
    print("="*60)
    print("To populate AMG, uncomment the Graphiti initialization")
    print("and run the populate_* functions with your instance.")
    print("="*60)
    
    # Example population sequence:
    # await populate_project(graphiti, AGENTFORGE_PROJECT)
    # await populate_features(graphiti, AGENTFORGE_PROJECT.name, AGENTFORGE_FEATURES)
    # await populate_components(graphiti, AGENTFORGE_PROJECT.name, AGENTFORGE_COMPONENTS)
    # await add_component_dependencies(graphiti, AGENTFORGE_COMPONENTS)


if __name__ == "__main__":
    asyncio.run(main())
