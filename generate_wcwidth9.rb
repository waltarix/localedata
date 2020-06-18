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
    #ifndef WCWIDTH9_H
    #define WCWIDTH9_H

    #include <stdlib.h>
    #include <stdbool.h>

    struct wcwidth9_interval {
      long first;
      long last;
      int width;
    };

    #define WCWIDTH9_TABLE_MAX_INDEX #{ranges.size - 1}

    static const struct wcwidth9_interval wcwidth9_table[] = {
      #{table_rows.join("\n  ")}
    };

    static inline int wcwidth9_width(const struct wcwidth9_interval *table, int top, int c) {
      int mid, bot;

      if (c < table[0].first) {
        return 1;
      }

      bot = 0;
      while (top >= bot) {
        mid = (bot + top) / 2;

        if (table[mid].last < c) {
          bot = mid + 1;
        } else if (table[mid].first > c) {
          top = mid - 1;
        } else {
          return table[mid].width;
        }
      }

      return 1;
    }

    static inline int wcwidth9(int c) {
      if (c == 0) return 0;
      if (c < 0x20) return -1;
      if (c < 0x7F) return 1;
      if (c < 0xA0) return -1;
      if (c < 0 || c > 0x10ffff) return -1;

      return wcwidth9_width(wcwidth9_table, WCWIDTH9_TABLE_MAX_INDEX, c);
    }

    #endif /* WCWIDTH9_H */
  CODE
)
