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
domain-use-cases-pkg: com.salpreh.baseapi.domain.services # domain use cases implementation
domain-exceptions-pkg: com.salpreh.baseapi.domain.exceptions # domain exceptions

db-adapters-pkg: com.salpreh.baseapi.adapters.infrastructure.db.adapters # db adapters (port implementations)
db-models-pkg: com.salpreh.baseapi.adapters.infrastructure.db.models # db entities package
db-repositories-pkg: com.salpreh.baseapi.adapters.infrastructure.db.repositories # db repositories package

db-mapper-class: com.salpreh.baseapi.adapters.infrastructure.db.mappers.DbMapper # mapper class to map db adapter entities to domain models. Needed if no mapper option specified when running command (optional)
db-mapper-pkg: com.salpreh.baseapi.adapters.infrastructure.db.mappers # db mapper package.Needed when mapper option specified when running command (optional)

rest-models-pkg: com.salpreh.baseapi.application.api.models # rest models package
rest-controllers-pkg: com.salpreh.baseapi.application.api.controllers # rest controllers package
rest-exception-handler-pkg: com.salpreh.baseapi.application.api.config # rest exception handler package

rest-mapper-class: com.salpreh.baseapi.application.api.controllers.mappers.ApiMapper # mapper class to map domain models to api models. Needed if no mapper option specified when running command (optional)
rest-mapper-pkg: com.salpreh.baseapi.application.api.controllers.mappers # api mapper package. Needed when mapper option specified when running command (optional)
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
You can use the `--help` option to see all available options:
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

## Details
### Spec file options
#### Model
First level keys in spec file are the **model names**. Each model name is followed by a map with the model fields/attributes. 
```yaml
Person: # Model name
  id: Long # Field name
  name: String # Field name
  surname:  # Field name
    type: String
    column: last_name
  birthPlanet: # Field name with relation data
    type: Planet
    column: birth_planet
    relation:
      type: many-to-one
      join-column: birth_planet_id
```
There is a special key inside the model map called `.meta` that contains metadata about the model.

```yaml
Person: # Model name
  .meta:
    table-name: persons # Table name for entity
  id: Long # Field name
  name: String # Field name
# More fields
```
Current supported options in meta are:
- `table-name`: Table name for the entity. If not specified, will use the model name as table name.

#### Field
Fields in the model have many options depending on the type of field. The most basic field spec is just the field name and the type:
```yaml
Person: # Model name
  id: Long # Field name
  name: String # Field name
```

This structure can be expanded to specify additional options for the field. 
```yaml
Person: # Model name
  name: # Field name
    type: String # Field type
    column: original_name # Column name alias
    
  id:  # Field name
    type: Long # Field type
    id:
      type: sequence # PK generation strategy
      sequence: person_pk_gen # Sequence name
    
  birthPlanet: # Field name
    type: Planet # Field type
    column: birth_planet # Column name alias
    relation: # DB relation metadata
      type: many-to-one
      join-column: birth_planet_id
```

Options available are:
- `type`: Field type. Can contain a primitive, java type, custom class or another model.
- `column`: Column name alias. If not specified, will use the field name as column name.
- `id`: Marks the field as Primary key in DB. Also contains metadata for PK generation strategy. 
- `relation`: Contains metadata for DB relations.

Expanding on `type` options available here is an example with each one of the mentioned options:
```yaml
Person:
  id: 
    type: UUID # Java type
    id: auto
  age: int # Primitive type
  birthPlanet: 
    type: Planet # Model class
    relation:
      type: many-to-one
      join-column: birth_planet_id
  race: com.salpreh.baseapi.domain.models.RaceType # Custom class
```
For custom classes full package name is required (`race` field in example). For java types, currently not all types are supported, in case you need a not supported type you can use full package name to refer to it. There is a list of supported types in the annexes section [here](#annexes).

For regular fields most common option is to use type directly as value (first example), or a map with type and column name alias (second example). We will dig into `id` and `relation` options in the next sections.

#### Id fields
Id fields are marked with the `id` key. This key also contains metadata about the PK generation strategy.
```yaml
Person: # Model name
  id:  # Field name
    type: Long # Field type
    id: 
      type: sequence # PK generation strategy
      sequence: person_pk_gen # Sequence name
      
Spaceship: # Model name
  code: # Field name
    type: UUID # Field type
    column: ship_code # Column name alias
    id: auto # PK generation strategy
```

PK generation strategies are mapped to JPA generation strategies with lower case. Current supported strategies are:
- `none`: No generation strategy.
- `auto`: Auto generation strategy.
- `sequence`: Sequence generation strategy. Sequence name can be provided.
- `identity`: Identity generation strategy.

#### Relation fields
Relation fields are marked with the `relation` key. This key also contains metadata about the relation.
```yaml
Person:
  birthPlanet: # Field name
    type: Planet # Field type
    column: birth_planet
    relation: # DB relation metadata
      type: many-to-one # Relation type
      join-column: birth_planet_id # Join column for relation
  affiliations:
    type: Faction # Field type
    relation: # DB relation metadata
      type: many-to-many # Relation type
      join-table: person_affiliation # Join table for relation
      join-column: person_id # Join column for relation
      inverse-join-column: faction_id # Inverse join column for relation
  backup: # Field name
    type: Person # Field type
    relation: # DB relation metadata
      type: one-to-one # Relation type
      join-column: backup_id # Join column for relation
```
Options available are:
- `type`: Relation type. Supported options are:
  - `one-to-one`
  - `one-to-many`
  - `many-to-one`
  - `many-to-many`
- `join-column`: Join column for relation (owning side).
- `mapped-by`: Mapped by field for relation (inverse side).
- `inverse-join-column`: Inverse join column for relation (many-to-many relations).
- `join-table`: Join table for relation (many-to-many relations).

All of these options are mapped to JPA annotations and configurations. Explaining when to use each option and what it does is out of the scope of this document.

## Annexes
### Supported types
```yaml
# Java
'Collection': 'java.util.Collection'
'List': 'java.util.List'
'ArrayList': 'java.util.ArrayList'
'Set': 'java.util.Set'
'HashSet': 'java.util.HashSet'
'Map': 'java.util.Map'
'HashMap': 'java.util.HashMap'
'UUID': 'java.util.UUID'
'Optional': 'java.util.Optional'
'Stream': 'java.util.stream.Stream'
'String': 'java.lang.String'
'Double': 'java.lang.Double'
'Float': 'java.lang.Float'
'Integer': 'java.lang.Integer'
'Short': 'java.lang.Short'
'Long': 'java.lang.Long'
'Boolean': 'java.lang.Boolean'
'BigDecimal': 'java.math.BigDecimal'
'BigInteger': 'java.math.BigInteger'
# Spring data
'Page': 'org.springframework.data.domain.Page'
'Pageable': 'org.springframework.data.domain.Pageable'
```

### References
- [JPA Bidirectional relations](https://vladmihalcea.com/jpa-hibernate-synchronize-bidirectional-entity-associations/)
- [JPA many-to-many relations](https://www.jpa-buddy.com/blog/synchronization-methods-for-many-to-many-associations/)
- [JPA equals/hashCode](https://vladmihalcea.com/how-to-implement-equals-and-hashcode-using-the-jpa-entity-identifier/)
- [JPA many-to-many collections](https://vladmihalcea.com/the-best-way-to-use-the-manytomany-annotation-with-jpa-and-hibernate/)
