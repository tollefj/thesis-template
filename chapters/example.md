# Example Chapter Using DMD Enhanced Syntax

This chapter demonstrates the new DMD (Document Markdown) enhanced syntax that makes writing academic documents cleaner and more intuitive.

## Enhanced Figure Syntax

Instead of the verbose standard markdown syntax:

```markdown
![Long caption with details about experimental setup...](images/plot.jpg){#fig:oldstyle width=50% short-caption="Experimental setup"}
```

You can now use the cleaner inline syntax:

![This figure shows the experimental setup with all components labeled. The system consists of multiple interconnected modules that process data in real-time.](images/part1-placeholder.jpg){#fig:newstyle width=60% short-caption="Experimental setup"}

The syntax is much more readable: `![Caption.`](path){#fig:id}

## Enhanced Cross-References

Reference figures naturally with @fig:newstyle, which transpiles to the correct pandoc syntax.

## Enhanced Table Syntax



| Method   | Accuracy | Speed    | Memory |
|----------|----------|----------|--------|
| Baseline | 85.3%    | Fast     | Low    |
| Method A | 92.1%    | Medium   | Medium |
| Method B | 88.7%    | Slow     | High   |
| Proposed | 95.2%    | Fast     | Low    |

: Performance comparison of different methods {#tbl:results}
: for the complete results. {#tbl:results}
Reference the table with 

## Semantic Callouts

::: {.bluebox title="Note"}
This is an important concept to remember. Notes are displayed in blue boxes.
:::

::: {.yellowbox title="Warning"}
Be careful when applying this technique. It may not work in all scenarios.
:::

::: {.graybox title="Tip"}
Pro tip: Always validate your results with multiple test cases.
:::

## Equations and References

When you have an equation:

$$
E = mc^2
$$ {#eq:einstein}

You can reference it with \eqref{eq:einstein} in the text.

## Mixed Syntax Support

DMD maintains 100% backward compatibility. Standard markdown still works:

![Standard syntax figure](images/part2-placeholder.jpg){#fig:standard width=40%}

You can freely mix both syntaxes in the same document. Reference @fig:standard and @fig:newstyle side by side.

## Benefits of DMD Syntax

1. **More readable**: `![Caption` vs `![Caption](path){#fig:id}`](path){#fig:id}
2. **Less typing**: Short attribute names like `w=50%` vs `width=50%`
3. **Unified references**: Always use `@type[label]` pattern
4. **Semantic callouts**: `::: {.bluebox title="Note"}
text
:::` instead of `::: {.bluebox title="Note"}`
5. **Backward compatible**: All existing markdown works unchanged

## Conclusion

The DMD transpiler converts this clean syntax to standard markdown that works with the existing Pandoc + Lua filter + XeLaTeX pipeline. You get a better writing experience without changing the build system.
