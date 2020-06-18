# frozen_string_literal: true

require './lib'

ranges = Chars.new.wcwidth9_ranges

code_formatter = ->(char) { format('0x%<code>04X', code: char.code).rjust(8) }

table_rows = ranges.map do |range|
  min, max = range.minmax.map(&code_formatter)
  width = range.width.to_s.rjust(2)
  "{#{min}, #{max}, #{width}},"
end

puts(
  <<~CODE
    package runewidth

    var wcwidth9_table_length = #{ranges.size - 1}

    var wcwidth9_table = table {
      #{table_rows.join("\n  ")}
    }
  CODE
)
