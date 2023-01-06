# Crudhex

[![PyPI version](https://badge.fury.io/py/crudhex.svg)](https://badge.fury.io/py/crudhex)

⚠️ **Warn: Beta development stage**

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
src: src/main/java # General sources for single module apps, default to src/main/java (maven project)

domain-models-pkg: com.salpreh.baseapi.domain.models # domain models package
domain-commands-pkg: com.salpreh.baseapi.domain.models.commands # domain commands package
domain-in-ports-pkg: com.salpreh.baseapi.domain.ports.application # domain ports (in/driving/application)
domain-out-ports-pkg: com.salpreh.baseapi.domain.ports.infrastructure # domain ports (out/driven/infrastructure)
domain-use-cases-pkg: com.salpreh.baseapi.domain.services

db-adapters-pkg: com.salpreh.baseapi.adapters.infrastructure.db.adapters # db adapters (port implementations)
db-models-pkg: com.salpreh.baseapi.adapters.infrastructure.db.models # db entities package
db-repositories-pkg: com.salpreh.baseapi.adapters.infrastructure.db.repositories # db repositories package

db-mapper-class: com.salpreh.baseapi.adapters.infrastructure.db.mappers.DbMapper # mapper class to map db adapter entities to domain models (optional)

rest-models-pkg: com.salpreh.baseapi.application.api.models # rest models package
rest-controllers-pkg: com.salpreh.baseapi.application.api.controllers # rest controllers package
```

In case of multimodule project you will have to specify `src` path to each module (domain, rest adapter and db adapter). 
```yaml
# Source folder for each module
domain-src: domain/src/main/java # Domain java sources
db-adapter-src: infrastructure/datasource-adapter/src/main/java # DB adapter java sources
rest-adapter-src: application/web/src/main/java # Rest adapter java sources

# Packages config as previous example
```
More examples of config can be found in (`doc/examples/config`).

The default name for this config file is `.crudhex-conf.yaml`, located in the root of the project (you can provide the path to config file by cli options, so you can place it anywhere you want)

### Spec file
This is the file where you specify the crud model. Class name, attributes and some metadata about DB structure (relations, PK field, column name alias, etc).

An example of spec file:
```yaml
Person: # Model name
  .meta:
    table-name: persons # OPTIONAL: Table name for entity
  id: # Field name
    type: Long
    id: sequence # PK marker. This field will be the primary key for the entity. 
                 # As value, you specify generation strategy available in JPA with lower case.
  name: String # Field name and type
  birthPlanet: # Field name
    type: Planet
    column: birth_planet # OPTIONAL: Column name alias
    relation: # DB relation meta data in case of FK
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

# Here another model
Planet:
  .meta:
    table-name: planets
  id:
    type: Long
    id: # You can specify the generation strategy as map to use additional options. In this case we are giving a sequence name
      type: sequence 
      sequence: planet_pk_gen
  name: # Field name and type also can be specified as map to add column name metadata
    type: String 
    column: original_name
  affiliation:
    type: Faction
    relation:
      type: many-to-one
      join-column: affiliation_id
  relevantPersons:
    type: Person
    relation:
      type: one-to-many
      mapped-by: birthPlanet

```

Snippet config comments provide an overview of each relevant section in config. I'll dig further in config details in a dedicated section.
For now, you can find some additional examples in `doc/examples/spec`.

### Installation

Package is published in Pypi public repositories. You can use [pip]() (or another convenient python dependency manager) to install the package:
```shell
pip install crudhex
```

Once installed you should be able to use it as CLI tool:
```shell
crudhex --help
```

### Usage
Once installed, you can use the CLI tool to generate the code. You can use the `--help` option to see all available options:
```shell
crudhex --help
```

To generate the code you need to locate the shell in the root of the project and run the command:
```shell
crudhex -m mapstruct spec/crudhex.yaml
```
Here we are specifying mapstruct as mapper library and the path to the spec file. By default, will use the config file `.crudhex-conf.yaml` located in the root of the project.

If you want to use a different config file, you can specify it with the `-c` option:
```shell
crudhex -c .doc/config/cruhex-config.yaml spec/crudhex.yaml
```
