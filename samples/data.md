# Working with placeholders
Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.


## How to use placeholders with build guides
- Make new folder `/tmp/testing_placeholders`;
- Go to `/tmp/testing_placeholders`;
- Create new file `hello.sh`;
- Add the following content to file `hello.sh`:
```
#!/bin/bash

echo "Hello, I am <real_name>! But you probably know me better by <first_name> <last_name>."
```
- Set permissions `744` to `hello.sh`;
- List files from `/tmp`.
- Run `./hello.sh`.
