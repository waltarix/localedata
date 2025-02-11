export PYTHONPATH := src

PYTHON := poetry run python
CURL   := curl --progress-bar -L

BUILD_DIR := build
DIST_DIR  := dist

UNICODE_VERSION   := 16.0.0
DOWNLOAD_URL_BASE := https://www.unicode.org/Public/$(UNICODE_VERSION)/ucd

UNICODE_DIR   := unicode
DATA_FILES    := $(addprefix $(UNICODE_DIR)/, UnicodeData.txt EastAsianWidth.txt DerivedCoreProperties.txt HangulSyllableType.txt)
EMOJI_FILE    := $(UNICODE_DIR)/emoji-data.txt
UNICODE_FILES := $(DATA_FILES) $(EMOJI_FILE)

GLIBC_VERSION        := 2.41
UNICODE_GEN_URL_BASE := https://raw.githubusercontent.com/bminor/glibc/glibc-$(GLIBC_VERSION)/localedata/unicode-gen
UNICODE_GEN_FILES    := $(addprefix $(BUILD_DIR)/,utf8_gen.py unicode_utils.py)

UNICODE_WIDTH_VERSION := 0.1.13
TABLE_SCRIPT_URL      := https://raw.githubusercontent.com/unicode-rs/unicode-width/v$(UNICODE_WIDTH_VERSION)/scripts/unicode.py
TABLE_SCRIPT_FILE     := ./src/chars/tables/unicode.py

GENERATED_EAW_FILE  := $(DIST_DIR)/EastAsianWidth.txt
GENERATED_DEAW_FILE := $(DIST_DIR)/DerivedEastAsianWidth.txt
TARGET_FILES        := $(addprefix $(DIST_DIR)/, \
												UTF-8 \
												wcwidth9.h \
												wcwidth9.py \
												runewidth_table.go \
												lookup.rs \
												) $(GENERATED_EAW_FILE) $(GENERATED_DEAW_FILE)

CACHE_FILES := $(addprefix .cache/, eaw.pickle wcwidth9.pickle)

all: $(TARGET_FILES)

$(TARGET_FILES): | $(DIST_DIR)

$(DIST_DIR)/UTF-8: $(UNICODE_FILES) $(GENERATED_EAW_FILE) $(UNICODE_GEN_FILES)
	$(PYTHON) -B $(BUILD_DIR)/utf8_gen.py \
		-u $(UNICODE_DIR)/UnicodeData.txt \
		-d $(UNICODE_DIR)/DerivedCoreProperties.txt \
		-k $(UNICODE_DIR)/HangulSyllableType.txt \
		-e $(GENERATED_EAW_FILE) \
		--unicode_version $(UNICODE_VERSION)
	mv $(@F) $@

$(DIST_DIR)/wcwidth9.h: $(UNICODE_FILES) $(CACHE_FILES)
	$(PYTHON) -m generate.wcwidth9_h > $@

$(DIST_DIR)/wcwidth9.py: $(UNICODE_FILES) $(CACHE_FILES)
	$(PYTHON) -m generate.wcwidth9_py > $@

$(DIST_DIR)/runewidth_table.go: $(UNICODE_FILES) $(CACHE_FILES)
	$(PYTHON) -m generate.runewidth_table_go > $@

$(DIST_DIR)/lookup.rs: $(UNICODE_FILES) $(CACHE_FILES)
	$(PYTHON) -m generate.lookup_rs > $@

$(DATA_FILES):
	$(CURL) -o $@ $(DOWNLOAD_URL_BASE)/$(notdir $@)

$(EMOJI_FILE):
	$(CURL) -o $@ $(DOWNLOAD_URL_BASE)/emoji/$(notdir $@)

$(UNICODE_GEN_FILES): | $(BUILD_DIR)
	$(CURL) -o $@ $(UNICODE_GEN_URL_BASE)/$(@F)

$(TABLE_SCRIPT_FILE):
	$(CURL) $(TABLE_SCRIPT_URL) > $@

$(GENERATED_EAW_FILE): $(DATA_FILES) $(CACHE_FILES) | $(BUILD_DIR)
	$(PYTHON) -m generate.east_asian_width_txt > $@

$(GENERATED_DEAW_FILE): $(DATA_FILES) $(CACHE_FILES) | $(BUILD_DIR)
	AS_DERIVED=1 $(PYTHON) -m generate.east_asian_width_txt > $@

$(BUILD_DIR) $(DIST_DIR):
	mkdir -p $@

$(CACHE_FILES) &: $(DATA_FILES) $(TABLE_SCRIPT_FILE)
	$(PYTHON) -m generate.util.cache

clean: mostlyclean
	$(RM) -r $(UNICODE_FILES) $(UNICODE_GEN_FILES) $(TABLE_SCRIPT_FILE) $(CACHE_FILES) $(BUILD_DIR)

mostlyclean:
	$(RM) -r $(DIST_DIR)

.PHONY: all clean mostlyclean
