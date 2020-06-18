# frozen_string_literal: true

require 'pathname'
require 'singleton'

module UCD
  EmojiData = Pathname.new('unicode/emoji-data.txt').freeze
  EastAsianWidth = Pathname.new('unicode/EastAsianWidth.txt').freeze
end

class CodeRanges
  def initialize(ranges)
    @ranges = ranges
  end

  def include?(code)
    @ranges.bsearch { |r| r.max >= code }&.include?(code)
  end
end

module NonPrintable
  Ranges = CodeRanges.new(
    [
      (0x0000..0x001F),
      (0x007F..0x009F),
      (0x00AD..0x00AD),
      (0x070F..0x070F),
      (0x180B..0x180E),
      (0x200B..0x200F),
      (0x2028..0x202E),
      (0x206A..0x206F),
      (0xD800..0xDFFF),
      (0xFEFF..0xFEFF),
      (0xFFF9..0xFFFB),
      (0xFFFE..0xFFFF),
    ]
  )

  module_function

  def include?(char)
    Ranges.include?(char.code)
  end
end

module ZeroWidth
  EmojiModifiers = (0x1F3FB..0x1F3FF).freeze # rubocop:disable Naming/ConstantName

  ZERO_WIDTH_DATA_PROP = {
    Me: true,
    Mn: true,
    Cf: true
  }.freeze

  module_function

  def include?(char)
    ZERO_WIDTH_DATA_PROP.key?(char.data_prop) ||
      EmojiModifiers.include?(char.code)
  end
end

module SingleWidth
  Ranges = CodeRanges.new(
    [
      (0x24EB..0x24FF),
      (0x2500..0x254B),
      (0x2550..0x2573),
      (0x2580..0x258F),
      (0x2592..0x2595),
      (0x25A0..0x25A1),
      (0x25A3..0x25A9),
      (0xE0A0..0xE0D7),
    ]
  )

  module LatinLettersAndOthers
    module_function

    def include?(char)
      char.ambiguous? && char.code < 0x02B0
    end
  end

  module_function

  def include?(char)
    Ranges.include?(char.code) ||
      LatinLettersAndOthers.include?(char)
  end
end

class MatchData
  def to_emoji_range
    min = self[:min]
    max = self[:max] || min
    EmojiRange.new(min: min, max: max)
  end

  def to_chars
    min = self[:min].to_i(16)
    max = self[:max]&.to_i(16) || min
    props = {
      width_prop: self[:width_prop].to_sym,
      data_prop: self[:data_prop].to_sym,
      comment: self[:comment]
    }
    (min..max).map { |code| Char.new(code, **props) }
  end
end

class EmojiRanges
  include Singleton

  PATTERN = /
              ^
              (?<min>[0-9A-F]{4,6})
              (?:
                \.\.
                (?<max>[0-9A-F]{4,6})
              )?
              \s+;\s+Emoji\s+
              \#
            /x.freeze

  class << self
    def include?(char)
      instance.ranges.include?(char.code)
    end
  end

  def ranges
    @ranges ||= all
                .select(&:wide?)
                .each_with_object([], &method(:shrink))
                .then(&CodeRanges.method(:new))
  end

  private

  def all
    UCD::EmojiData.each_line.each_with_object([]) do |l, memo|
      next unless (m = l.match(PATTERN))

      memo << m.to_emoji_range
    end
  end

  def shrink(range, memo)
    if memo.last&.mergeable?(range)
      memo.last.merge!(range)
    else
      memo << range
    end
    memo
  end
end

class EmojiRange
  attr_reader :min, :max

  def initialize(min:, max:)
    @min = min.to_i(16)
    @max = max.to_i(16)
  end

  def mergeable?(other)
    max.next == other.min
  end

  def merge!(other)
    @max = other.max
    @range &&= nil
  end

  def wide?
    min >= 0x1F000
  end

  def include?(code)
    range.include?(code)
  end

  def range
    @range ||= (min..max)
  end
end

class Char
  attr_reader :code, :width_prop, :data_prop, :comment

  WIDTH_MAP = {
    N: 1,
    Na: 1,
    H: 1,
    A: 2,
    W: 2,
    F: 2
  }.freeze

  def initialize(code, width_prop:, data_prop:, comment:)
    @code = code
    @width_prop = width_prop
    @data_prop = data_prop
    @comment = comment
  end

  def well_known?
    code < 0x00A0
  end

  def ambiguous?
    width_prop == :A
  end

  def width
    @width ||= if soft_hyphen?      then 1
               elsif non_printable? then -1
               elsif zero_width?    then 0
               elsif single_width?  then 1
               elsif emoji?         then 2
               else                      WIDTH_MAP[width_prop]
               end
  end

  def soft_hyphen?
    code == 0x00AD
  end

  def reserved?
    comment.start_with?('<reserved-')
  end

  def double_width?
    width == 2
  end

  def non_printable?
    NonPrintable.include?(self)
  end

  def zero_width?
    ZeroWidth.include?(self)
  end

  def single_width?
    SingleWidth.include?(self)
  end

  def emoji?
    EmojiRanges.include?(self)
  end

  def mergeable?(other)
    code.next == other.code && width == other.width
  end
end

class Chars
  PATTERN = /
            ^
            (?<min>[0-9A-F]{4,6})
            (?:
              \.\.
              (?<max>[0-9A-F]{4,6})
            )?
            ;
            (?<width_prop>[^ ]+)
            \s+
            \#
            \ (?<data_prop>[^ ]+)
            \ (?:\s*\[\d+\])?
            \s+
            (?<comment>.+)
            /x.freeze

  def all
    @all ||= parse
  end

  def wcwidth9_ranges
    all
      .reject(&:well_known?)
      .then(&CharRange.method(:call))
  end

  def eaw_ranges
    all
      .reject(&:reserved?)
      .select(&:double_width?)
      .then(&CharRange.method(:call))
  end

  private

  def parse
    UCD::EastAsianWidth.each_line.each_with_object([]) do |l, memo|
      next unless (m = l.match(PATTERN))

      memo.push(*m.to_chars)
    end
  end
end

class CharRange
  attr_reader :min, :max, :width

  class << self
    def call(chars)
      chars.each_with_object([], &method(:shrink))
    end

    def shrink(char, memo)
      if memo.last&.mergeable?(char)
        memo.last.merge!(char)
      else
        memo << new(char)
      end
      memo
    end
  end

  def initialize(char)
    @min = char
    @max = char
    @width = char.width
  end

  def minmax
    [min, max]
  end

  def merge!(other)
    @max = other
  end

  def mergeable?(other)
    @max.mergeable?(other)
  end
end
