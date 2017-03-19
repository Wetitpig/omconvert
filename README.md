# omconvert

## What is omm?

omm is a special file format for OSM data, with '>'s and '<'s and '='s as the delimiters. This is kind of like csv file format.

It follows the following schema:

### First part -- Basic Attributes:

```

[type]>[id]>[visible]>[version]>[changeset]>[user]>[uid]>

```

Where:

type: type of object represented in integer value.

               0 for node
               
               1 for way
               
               2 for relation

visibility: whether the object is deleted or not.

                 0 for false
                 
                 1 for true
                 
### Second part -- Coordinates/Nodes/Members of object

For nodes:

```

[Lat]<[Lon]>

```

For ways:

```

[nd ref]<[nd ref]<[nd ref]...<[nd ref]>

```

For relations:

```

[member type]=[member id]=[member role]<[member type]=[member id]=[member role]<[member type]=[member id]=[member role]<...<[member type]=[member id]=[member role]>

```

### Third part -- tagging

```

[tag key]=[tag value]<[tag key]=[tag value]<...<[tag key]=[tag value]

```

## What is omc?

omc is a changeset version of omm. It is derived from omm, with minor modifications.

To denote modification acrion, a number with a colon is used.

For example, denoting <create> would be 3:

                                         <modify> would be 4:
                                         
                                         <delete> would be 5:
                                       
## Why omm and omc

It strikes a balance between compressed form and xml form.

### Compared to osm & osc

- Compact ( around ⅓ of the size )

### Compared to o5m & o5c & obf

- Human readable

- High compression ratio through different methods

## How to install

Prerequisites: python 3 interpreter with standard library
                          
No building is required. Just move the python scripts to your destination folder and ypu can run!

## License

It is released under the GNU LGPLv3 license.