# frozen_string_literal: true

require './lib'

ranges = Chars.new.eaw_ranges

code_formatter = ->(char) { format('%<code>04X', code: char.code) }

puts(
  ranges.map do |range|
    range_string = range.minmax.uniq.map(&code_formatter).join('..')
    "#{range_string};F"
  end
)
