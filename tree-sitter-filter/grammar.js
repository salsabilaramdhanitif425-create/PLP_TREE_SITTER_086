export default grammar({
  name: 'filter',
  extras: $ => [/\s/],
  word: $ => $.identifier,
  rules: {
    query: $ => $._expr,
    _expr: $ => choice(
      $.comparison,
      $.in_expression,
      $.contains_expression,
      $.and_expression,
      $.or_expression,
      $.not_expression,
      $.parenthesized
    ),
    and_expression: $ => prec.left(2, seq(
      field('left', $._expr),
      'and',
      field('right', $._expr)
    )),
    or_expression: $ => prec.left(1, seq(
      field('left', $._expr),
      'or',
      field('right', $._expr)
    )),
    not_expression: $ => prec(3, seq(
      'not',
      field('operand', $._expr)
    )),
    parenthesized: $ => seq('(', $._expr, ')'),
    comparison: $ => seq(
      field('left', $.identifier),
      field('operator', choice('=', '!=', '>', '<', '>=', '<=')),
      field('right', $._value)
    ),
    in_expression: $ => seq(
      field('left', $.identifier),
      'in',
      field('right', $.list)
    ),
    contains_expression: $ => seq(
      field('left', $.identifier),
      'contains',
      field('right', $.string)
    ),
    list: $ => seq(
      '[',
      optional(seq($._value, repeat(seq(',', $._value)))),
      ']'
    ),
    _value: $ => choice($.string, $.number, $.boolean),
    identifier: $ => /[a-zA-Z_][a-zA-Z0-9_.]*/,
    string: $ => /"[^"]*"/,
    number: $ => /\d+(\.\d+)?/,
    boolean: $ => choice('true', 'false'),
  }
});