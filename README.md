# Regex2MDFA
> Input a Regex, get its abstract syntax tree (AST), non-deterministic finite automata (NFA), deterministic finite automata (DFA) and finally its Minimized DFA

## ⚒️ Supported Rules<a name = "features"></a>

- [x] Alteration: A|B
- [x] Concatenation: AB
- [x] 1 or More: A+
- [x] 0 or More: A*
- [x] Optional - 0 or 1: A?
- [x] ORing: [abc], (a|b|c), [123], (1|2|3)
- [x] Ranges: [0-9] or [a-z]
- [x] Grouping using parentheses to control the order of operations (ABD)+
- [ ] Min and Max Number of repetitions of certain token (a{1,3}) and its different vairiants

## 🏁 Get started <a name = "Install"></a>
- Using the ` main.py ` file

```bash
git clone https://github.com/BigFish2086/Regex2MDFA
cd Regex2MDFA
python -m pip install -r requirements.txt
cd src
python ./main.py <REGEX>
```

- Or using the [notebook](./regex2mdfa.ipynb) provided here in the github link, however whenever changing the testcase/regex in hand,
make sure to re-run the whole notebook again, since it's just a compilation of all the files in the ` src ` folder
