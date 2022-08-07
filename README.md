# Crudhex

[![PyPI version](https://badge.fury.io/py/crudhex.svg)](https://badge.fury.io/py/crudhex)

⚠️ **Warn: Alpha development stage**

---

CLI tool to generate Java CRUD classes from a spec file. The target for this code generation is a Hexagonal architecture.


## Motivation
Adding CRUD operation in a hexagonal project is quite a pain. You can take shortcuts that can be totally legit in cases of just CRUD operations, but most cases if there is already a rich domain/application layer for other use cases CRUD shortcuts can break the consistency of the project.

The target of this CLI is to ease ~~my life~~ and try to give a general solution to CRUD generations in Hexagonal architecture. There are some customizations you can make, but some aspects for now are closed to customization for now.

## Getting started

### Project config file
Project config file is used to know where things should go in the project. Usually contains a path to the sources folder (`src/main/java` in regular maven projects) and packages where things are located within that source folder.
Here is a basic example:
```yaml
src: src/main/java # Java source folder for single module apps (where your packages start)

domain-models-pkg: com.salpreh.baseapi.domain.models # domain models package
db-models-pkg: com.salpreh.baseapi.adapers.infrasturcture.db.models # db entities package
rest-models-pkg: com.salpreh.baseapi.adapters.api.models # rest api models
```

In case of multi-module project you will have to specify `src` path to each module (domain, rest adapter and db adapter). More examples of config can be found in (`doc/examples/config`).

The default name for this config file is `.crudhex-conf.yaml`, located in the root of the project (you can provide the path to config file by cli options, so you can place it anywhere you want)

### Spec file
This is the file where you specify the crud model. Class name, attributes and some meta data about DB structure (relations, PK field, column name alias, etc).

An example of spec file:
```yaml
Person: # Model name
  .meta:
    table-name: persons # OPTIONAL: Table name for entity
  id: # Field name
    type: Long
    id: sequence # PK marker. This field will be the primary key for the entity. 
                 # As value you specify generation strategy available in JPA with lower case.
  birthPlanet: # Field name
    type: Planet
    column: birth_planet # OPTIONAL: Column name alias
    relation: # OPTIONAL: DB relation meta data
      type: many-to-one # Relation type
      join-column: birth_planet_id # Join column for relation
  affiliations:
    type: Faction
    relation:
      type: many-to-many # In case of many-to-many we have a couple of more meta about DB setup
      join-table: person_affiliation 
      join-column: person_id
      inverse-join-column: faction_id
  backup:
    type: Person
    relation:
      type: one-to-one
      join-column: backup_id
  backing:
    type: Person
    relation:
      type: one-to-one
      mapped-by: backup # Mapping attribute for non-owning side of relation
```

Snippet config comments provide a overview of each relevant section in config. I'll dig further in config details in a dedicated section.
For now, you can find some aditional examples in `doc/examples/spec`.

### Installation

Package is published in Pypi public repositories. You can use [pip]() (or another convinient python dependency manager) to install the package:
```shell
pip install crudhex
```

Once installed you should be able to use it as CLI tool:
```shell
crudhex --help
```