# Amish Assembly

Amish Assembly is an esolang made out of spite, curiosity, and boredom.
It was created in a moment of weakness when I asked myself the question: How the fuck do I make assembly worse? And I got my anwser

## What it is
Each line of code represents exactly one byte of memory aka 8 bits. If you have any C or low level coding experience you may realise what this 1 byte means, 1 char!

Aka 1 line = 1 character!

You don’t write characters or opcodes directly. You build them bit by bit using 3 commands:
1. `]` you move the cursor ONE space to the right
2. `1` you change the bit from a zero to a 1
3. `0<0` added for simplicity sake, represents a new line

A bonus keyword is the `0>0` keyword, which represents a space allowing you to develop assembly faster than ever

That's it. No variables, no pointers, no loops, no undo.
When you finish writing a line, the compiler reads those 8 bits as a byte, turns it into an ASCII character, and moves on to the next line.

Any other character is ignored allowing for the *revolutionary* feature of ✨COMMENTING✨!

## Examples
```
]1]1]]1]]]    h
]1]1]]]1]]1   e
]1]1]]1]1]]   l
]1]1]]1]1]]   l
]1]1]]1]1]1]1 o
0>0
]1]1]1]]1]1]1 w
]1]1]]1]1]1]1 o
]1]1]1]]]1]   r
]1]1]]1]1]]   l
]1]1]]]1]]    d
```

### Why is this hello world?

`hello world` in ASCII is  
`104 101 108 108 111 32 119 111 114 108 100`

In binary, that’s  
`01101000 01100101 01101100 01101100 01101111 00100000 01110111 01101111 01110010 01101100 01100100`

Each line of Amish Assembly literally builds one of those bytes.

Take the **h** for example.  
It starts with a 0, so we move right once, set a 1, move again, set another 1, and so on until the byte matches `01101000`.

So enjoy I suppose, don't feel like you would.
