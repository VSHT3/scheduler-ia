Dictionaries are structured data types used for **storing information** efficiently. 

- **Why use them?** They are much easier to manage and manipulate than parallel lists that rely on matching indexes.
- **Real-world use:** They are structurally identical to **JSON** (JavaScript Object Notation)

## Basic Syntax
Instead of indexes, dictionaries use a `key: value` pair system (often thought of as a label and its corresponding value).

```python
# General syntax format
variable_name = {"key": "value"}

# Practical example
contact = {
    "name": "Alice", 
    "phone": "12345"
}
```

## Accessing Values
To retrieve a specific piece of information, reference the dictionary variable followed by the `key` inside square brackets.

```python
contact["name"] # Returns: 'Alice'
```

## Lists of Dictionaries
You can combine lists (arrays) and dictionaries to store multiple structured records in a single variable.

```python
contacts = [
  {"name": "Alice", "phone": "12345"},
  {"name": "Bob",   "phone": "67890"}
]
```

### Accessing Nested Data
To retrieve data from a list of dictionaries, first target the list index, then target the dictionary key:

```python
contacts["name"] # Returns: 'Alice' (the name of the first contact)
```


