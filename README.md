# whitespace-language-converter
Provide a converter from our language to whitespace

## Installation and Usage

put `to_ws.py` to any location and type the following command

```bash
python to_ws.py readable.hws -o beautiful.ws
```


## QuickStart

Put one command per line as follows:

```
push 5
push -2
add
printi
end
```

You can use labels if you want:

```
push 0
push 10
loop:
  dup
  push 0
  swap
  store
  swap
  push 0
  retrieve
  add
  swap
  push 1
  sub
  dup
  jz end
  jmp loop
end:
swap
printi
end
```

The above code calculates 10 + 9 + ... + 1 and output it.


## Our Language

- `push <n>` (n: integer)
Push n to the top of the stack.

- `printi`
Print the top of the stack as an integer and discard it.

- `printc`
Print the top of the stack as an character and discard it.

- `readc`
Read a character from stdin and store the address pointed by the top of the stack and discard it.

- `readi`
Read an integer from stdin and store the address pointed by the top of the stack and discard it.

- `dup`
Duplicate the top of the stack.

- `swap`
Swap the top two elements of the stack.

- `drop`
Discard the top of the stack.

- `add`
Let X be the sum of the top two elements of the stack.
Discard these two elements and push X.

- `sub`
Let X be the second element minus the first element of the stack.
Discard these two elements and push X.

- `mul`
Let X be the first element multiplied by the second element of the stack.
Discard these two elements and push X.

- `div`
Let X be the floor of the second element divided by the first element of the stack.
Discard these two elements and push X.

- `mod`
Let X be the reminder of the second element divided by the first element of the stack.
Discard these two elements and push X.

- `store`
Store the top of the stack to the address pointed by the second element of the stack and discard them.

- `retrieve`
Retrieve a value from the address pointed by the top of the stack, discard it and push the value.

- `end`
Exit.

- `<label>:`
Set a label.

- `call <label>`
Call a subroutine starting from `<label>`.

- `jmp <label>`
Jump to `<label>`.

- `jz <label>`
Discard the top of the stack and if it's zero then jump to `<label>`.

- `jn <label>`
Discard the top of the stack and if it's negative then jump to `<label>`.

- `ret`
Exit the current subroutine.

- `#...`
Comments.

- `  ...`
Indents.

## Not Supported

- `copy <n>`
- `slide <n>`
